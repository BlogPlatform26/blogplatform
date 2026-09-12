# Phase 47 — browser regression batch 2A

## Identitet provjere

- commit: `1185e6e6b22cda8d5be41b07c215d5a50e6ceb43`
- timestamp: `2026-09-12T06:12:39+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch2a-pass-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `litica_noci` | PASS | PASS | body `rgb(0, 0, 0)`; `litica_noci.png` + gradijent na `body::before` |
| `podvodna_tisina` | PASS | PASS | body `rgb(1, 6, 17)`; `podvodna_tisina.png` + gradijent na `body::before` |
| `vodopad_u_magli` | PASS | PASS | body `rgb(242, 241, 237)`; `vodopad_u_magli.png` + gradijent na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch2a-pass-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i lokalni tematski pseudo-background/overlay
- body pozadina odgovara završnoj boji overlaya, bez bijelog dna

## Litica regresija

Raniji bijeli body/dno više se ne pojavljuje. `litica_noci` na oba viewporta završava s computed crnim bodyjem, dok lokalni image/overlay ostaje aktivan.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na `litica_noci`
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Ostali shared tematski i special/full-custom dizajni ostaju za zasebne serijske batch-eve.
