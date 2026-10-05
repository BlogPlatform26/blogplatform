# Phase 87d — Iznad oblaka: kontrast objave i komentara

## Opseg

Phase 87d foto-neovisno popravlja samo tijelo objave, autora, post-action
kontrole i autora komentara u dizajnu `iznad_oblaka`. Ne dira kalendarski
raspored, shared CSS, podatke ni postojeće Phase87b/c naslovne i sidebar
površine.

## Promjena

Mete koriste tamnu lokalnu tintu `#514956` na punoj pastelnoj površini
`#fff7fc`, s malim zaobljenjem i diskretnim unutarnjim rubom. Površina je
neprozirna, pa čitljivost ne ovisi o svijetlom ili tamnom dijelu fotografije.
Hover i focus-visible stanja autora i akcija ostaju na istoj površini s još
tamnijom tintom.

## Kontrast i stvarni preglednik

Phase87a je za ovaj skup zabilježio 3,84–4,24:1 za autora i post-action
kontrole te 3,63:1 za autora komentara. Nakon Phase87d tijelo objave, autor,
like, komentari, `Otvori post` i autor komentara imaju **8,19:1**.

Blog i detail prikaz provjereni su na 320, 390, 768 i 1440 px, ukupno osam
stanja. Fizički document overflow ostaje `0 px`. Vizualni pregled na 390 i
1440 px potvrdio je da pastelna fotografija ostaje dominantna, a desktop
identitet i Phase87b naslovne površine ostaju očuvani. Postojeće lokalno
prelijevanje kalendarske mreže na 768 px ostaje (`160/118 px` scroll/client)
jer geometrija nije dio ovoga opsega.

Sigurni klikovi `Prethodni mjesec` i `Otvori post` doveli su do očekivanih
ruta bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase87d_iznad_oblaka_post_contrast.py` potvrđuje:

- lokalni CSS ugovor na blog i detail rutama;
- tintu i punu pastelnu površinu za tijelo, autora, akcije i autora komentara;
- izolaciju od dizajna `zlatni_horizont`.

## Preostali nalazi

Phase87d namjerno ne rješava P2 kalendarski overflow na 768 px, tabletne i
desktop touch mete te krhku širinu naslova posta na 320 px.
