# Phase 46 — fix Litica body CSS cascade

## Kvar

Browser Regression Batch 2A na commitu `9db657b5747283112eae4d9926bac0eb4d50d314` zaustavljen je na `litica_noci`: specifični rule deklarirao je crni body i ispravan `litica_noci.png` pseudo-overlay, ali kasniji generički fallback ponovno je postavljao bijeli body i tamni Default tekst. Full-page prikaz pokazao je bijelu podlogu izvan i ispod tematskog sloja.

## Uzrok

Završni Dark/Classic/Default blok u `blog_design_styles.html` koristio je neograničeni `{% else %}`. Zato se cijeli Default CSS emitirao za svaki template koji nije Dark ili Classic, uključujući Simple i shared tematske dizajne koji već imaju vlastite body ruleove.

## Popravak

- završni Default branch sada je eksplicitno ograničen na `default` i `default_right`
- Dark/Dark Plus i Classic/Classic Plus zadržavaju postojeće branch-eve
- Simple i shared tematske obitelji zadržavaju vlastite ranije ili lokalne CSS ruleove
- nije dodan `!important`

## Trajna regresija

Registry render test dodatno potvrđuje:

- `litica_noci` sadrži deklarirani crni body i ne sadrži kasni Default fallback
- `default` i dalje dobiva bijeli fallback
- `dark` i `classic` dobivaju svoje body ruleove i ne dobivaju Default fallback

## Browser potvrda

- timestamp: `2026-09-12T01:30:28+02:00`
- `litica_noci` 1440×900: PASS
- `litica_noci` 390×844: PASS
- computed body background: `rgb(0, 0, 0)`
- `body::before`: lokalni `litica_noci.png` i gradijentni overlay prisutni
- nema bijelog dna, horizontalnog overflowa, console/page grešaka ni nedostajućih ključnih DOM elemenata
- reprezentativni `default`: computed bijeli body, ključni DOM i overflow PASS
- reprezentativni `dark`: computed `rgb(17, 17, 17)`, dark title marker, ključni DOM i overflow PASS

## Izolacija

Originalni `db.sqlite3` i backup nisu mijenjani. Probni profil vraćen je na `litica_noci`, izolirana baza je uklonjena, viewport resetiran i lokalni server ugašen.

`podvodna_tisina` i `vodopad_u_magli` nisu nastavljeni u ovom koraku.
