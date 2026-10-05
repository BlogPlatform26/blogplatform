# Phase 88e — Šumska i Polarna svjetlost: tabletni kalendar

## Opseg

Phase 88e uklanja samo lokalni 768 px overflow calendar/grid elemenata u
`sumska_svjetlost` i `polarna_svjetlost`. Ne mijenja P1 kontrast ugovore iz
Phase88b/c/d niti P2 post-action mete.

## Uzrok i promjena

Globalni mobilni `44px !important` minimum dana s objavom nije stao u postojeći
tabletni `col-md-3` sidebar. Lokalni media query (768–991,98 px) smanjuje
unutarnji rub, postavlja nav naslov u tri kontrolirane grid kolone i koristi
sedam shrink-safe `minmax(0, 1fr)` kolona. Strelice ostaju 44 × 44 px.

## Stvarni preglednik

Prije Phase88e audit je izmjerio kalendare `176/150` (Šumska) i `184/150 px`
(Polarna), uz gridove `160/117` i `168/117 px`. Nakon promjene oba dizajna na
blog/detail pri 768 px imaju kalendar `149/149 px` i grid `133/133 px`.
Document overflow ostaje `0 px` na 320, 390, 768 i 1440 px, ukupno 16 stanja.

Mobilni 320/390 i desktop 1440 raspored nisu promijenjeni. Na 768 px dan s
objavom je oko 18 × 35 px, dok navigacija ostaje 44 × 44 px: dani su klikabilni,
ali veće tabletne touch mete ostaju zaseban P2 zadatak. Sigurni klikovi
prethodnog i sljedećeg mjeseca prošli su za oba dizajna bez mutacije podataka.

## Regresijska zaštita

`blog/test_phase88e_forest_polar_calendar_fit.py` potvrđuje lokalni ugovor za
oba dizajna i izolaciju od drugog dizajna.
