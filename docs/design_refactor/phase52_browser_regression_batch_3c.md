# Phase 52 — browser regression batch 3C

## Identitet provjere

- commit: `d2170eeb7f93fb801f786297874cf823668560b7`
- timestamp: `2026-09-12T06:40:24+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch3c-smoke-author/`
- rezultat: **PASS — 4/4 design/viewport kombinacije**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `polje_lavande` | PASS | PASS | body `rgb(217, 176, 238)`; `polje_lavande.jpg` + gradijent na `body::before` |
| `carobna_ljubicasta` | PASS | PASS | body `rgb(84, 43, 126)`; `carobna_ljubicasta.jpg` + linearni/radijalni gradijenti na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- HTTP 200 za odgovarajući lokalni background asset
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch3c-smoke-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i lokalni tematski pseudo-background/gradient
- završni stop pseudo-overlaya odgovara computed body boji

## Provjera vidljivosti layouta

Vidljivost nije zaključena samo iz DOM prisutnosti. Za lijevu i desnu kolonu te calendar/archive provjereni su computed `display`, `visibility`, `opacity` i nenulte dimenzije. Svaka od četiri kombinacije imala je stvarno vidljivu instancu svakog traženog elementa.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na početni `polje_lavande` ključ
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Preostali shared tematski i special/full-custom dizajni ostaju za zasebne serijske batch-eve.
