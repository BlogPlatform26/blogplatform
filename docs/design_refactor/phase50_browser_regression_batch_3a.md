# Phase 50 — browser regression batch 3A

## Identitet provjere

- commit: `235ea07350abb6fc35ecc115ff216ae3805ddd85`
- timestamp: `2026-09-12T06:32:39+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch3a-smoke-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `iznad_oblaka` | PASS | PASS | body `rgb(247, 244, 246)`; `iznad_oblaka.jpg` + gradijent na `body::before` |
| `sumska_svjetlost` | PASS | PASS | body `rgb(212, 227, 196)`; `sumska_svjetlost.jpg` + gradijent na `body::before` |
| `polarna_svjetlost` | PASS | PASS | body `rgb(78, 127, 190)`; `polarna_svjetlost.jpg` + gradijent na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- HTTP 200 za odgovarajući lokalni background asset
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch3a-smoke-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i lokalni tematski pseudo-background/overlay
- završni stop pseudo-overlaya odgovara computed body boji

## Provjera vidljivosti layouta

Element nije prihvaćen samo zato što postoji u DOM-u. Za lijevu i desnu kolonu te calendar/archive provjereni su computed `display`, `visibility`, `opacity` i nenulte dimenzije. Na svih šest kombinacija pronađena je po jedna stvarno vidljiva instanca svakog traženog elementa; skriveni layout duplikat nije korišten za PASS.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na početni `iznad_oblaka` ključ
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Preostali shared tematski i special/full-custom dizajni ostaju za zasebne serijske batch-eve.
