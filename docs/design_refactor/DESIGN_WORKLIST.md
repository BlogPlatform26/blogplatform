# DESIGN WORKLIST

Izrađeno: 2026-07-03 10:29:06

## Cilj

Ovaj dokument određuje koje dizajne radimo sada, koje kasnije i koje za sada ne diramo.
Cilj je da ne popravljamo dizajne napamet i da ne trošimo vrijeme na dizajne koji možda nisu stvarno ponuđeni korisnicima.

## Pravila rada

- Ne mijenjati izgled ako cilj faze nije vizualni bugfix.
- Ne dodavati CSS na dno kao krpanje ako postoji konkretno pravilo koje treba zamijeniti.
- Prvo raditi dizajne koji koriste zajednički layout i stvarno su ponuđeni korisnicima.
- Posebne dizajne raditi jedan po jedan.
- Nejasne/template-only dizajne ne dirati dok se ručno ne potvrdi da su ponuđeni korisnicima.
- Navbar je globalni dio platforme i blog dizajni ga ne bi smjeli mijenjati.

## RADIMO SADA

Ovo su dizajni koje prvo ima smisla sređivati jer koriste zajedničku strukturu ili su sigurniji za refaktor korisničkih postavki.

### osnovni_i_right_sidebar

- `default`
- `default_right`
- `dark`
- `dark_right`
- `classic`
- `classic_right`

### simple

- `simple`
- `simple_image`
- `simple_pattern`
- `simple_retro`

### tematski_zajednicki_layout

- `podvodna_tisina`
- `vodopad_u_magli`
- `planine_u_magli`
- `nebeski_mir`
- `iznad_oblaka`
- `sumska_svjetlost`
- `polarna_svjetlost`
- `zlatno_polje`
- `neonski_grad`
- `polje_lavande`
- `carobna_ljubicasta`
- `kraljevska_pozornica`
- `litica_noci`
- `svemirski_horizont`
- `zlatni_horizont`
- `morski_prijelaz`

### gradijentni_zajednicki_layout

- `dimni_akordi`
- `sjene_ulice`
- `mjesecev_ples`
- `asfaltni_plamen`

## RADIMO KASNIJE OPREZNO

Ovi dizajni su vjerojatno ponuđeni korisnicima, ali imaju posebnu strukturu. Ne prebacivati ih sve odjednom.

### posebni_single_sidebar

- `jedro_u_suton`
- `misticno_jezero`
- `nebeska_klasika`
- `ponocna_elegancija`
- `ruzicasti_vrt`
- `stara_aleja`
- `staza_prema_vrhovima`

### posebni_hero

- `magazin`

## PROVJERITI RUČNO PRIJE RADA

Ovo audit vidi u kodu, ali treba ručno potvrditi da se stvarno vidi u postavkama prije nego se radi.

- `nebesko_polje`

## ZA SADA NE DIRAMO

Ovo ne diramo dok se ne odluči treba li ostati u ponudi.

- `studio`
- `vecer_uz_jezero`
- `vecer_zaljubljenih`

## Sljedeće faze

### Faza 14 — audit navbar CSS-a u dizajnima

Cilj: Pronaći blog dizajne koji direktno mijenjaju globalni navbar, pretragu, obavijesti ili badge font.

Tip: audit only

### Faza 15 — neutralizirati navbar iz dizajna

Cilj: Ukloniti ili ograničiti pravila koja mijenjaju globalni navbar, bez promjene izgleda blog sadržaja.

Tip: small code change after audit

### Faza 16 — customization layer za zajedničke dizajne

Cilj: Srediti da korisničke postavke stabilno rade na sigurnijim dizajnima iz liste Radimo sada.

Tip: controlled refactor

## Napomena za `zlatno_polje`

`zlatno_polje` je potvrđen kao dizajn koji korisnik ima u izboru i ostaje u grupi koju radimo sada.

## Napomena za navbar

Navbar, tražilica, obavijesti i badge brojevi su globalni dio platforme. Blog dizajni ne bi smjeli mijenjati njihov font, boju ili raspored.
Ako audit pronađe takva pravila u dizajnima, prvo ih treba dokumentirati, a tek onda uklanjati ili ograničiti.
