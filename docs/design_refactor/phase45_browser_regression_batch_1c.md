# Phase 45 — browser regression batch 1C

## Identitet provjere

- commit: `3fa9df88dde7af12f1f5935af7506083276bf392`
- timestamp: `2026-09-12T01:21:22+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch1c-smoke-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni template markeri |
|---|---:|---:|---|
| `simple_pattern` | PASS | PASS | Simple header/posts klase; computed header gradient |
| `simple_image` | PASS | PASS | Simple header/posts klase; `bookshelf.png` na `body::before` i `body::after` |
| `simple_retro` | PASS | PASS | `--simple-retro` header, posts i layout-row klase |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv `.blog-page-title`
- vidljiv `.blog-post-entry`, njegov `h4`, post meta s autorom, `#batch1c-smoke-body`, `.post-actions` i `[id^="comments-"]`
- vidljivi sidebar, calendar i archive elementi prema stvarnom layoutu
- razlikovni computed/DOM marker aktivnog Simple templatea, ne samo zajednički HTTP odgovor

`simple_image` pozadinska slika namjerno je postavljena na oba body pseudo-elementa; computed URL za oba završava s `/static/blog/images/design-backgrounds/bookshelf.png`.

`simple_retro` sadrži skrivenu lijevu i vidljivu desnu sidebar granu. Konačni gate zato koristi `.blog-main-right-column .calendar-box` i `.blog-main-right-column .archive-box`, koji su vidljivi na oba viewporta.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na `simple_pattern`
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Core i Simple Batch 1 sada su pokriveni. Preostaju shared tematski i special/full-custom dizajni u zasebnim serijskim batch-evima.
