# Phase 48 — browser regression batch 2B

## Identitet provjere

- commit: `0c4bd16371d20bd1157a1d510cb4d4629b3640fe`
- timestamp: `2026-09-12T06:24:24+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch2b-smoke-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `planine_u_magli` | PASS | PASS | body `rgb(246, 245, 242)`; `planine_u_magli.jpg` + gradijent na `body::before` |
| `nebeski_mir` | PASS | PASS | body `rgb(246, 249, 255)`; `nebeski_mir.jpg` + gradijent na `body::before` |
| `svemirski_horizont` | PASS | PASS | body `rgb(0, 0, 0)`; `svemirski_horizont.png` + gradijent na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch2b-smoke-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i lokalni tematski pseudo-background/overlay
- body pozadina odgovara završnoj boji overlaya, bez bijelog ili pogrešno obojenog dna

## Background asseti i cascade regresija

Za sva tri dizajna development server vratio je HTTP 200 za odgovarajući lokalni asset. `body::before` zadržava sliku i gradijent, a njegov završni stop odgovara computed boji `body` elementa. Time je potvrđeno da kasni generički fallback nakon cascade popravka više ne pregazi tematsku završnu boju.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na `planine_u_magli`
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Preostali shared tematski i special/full-custom dizajni ostaju za zasebne serijske batch-eve.
