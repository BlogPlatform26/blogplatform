# Phase 53 — browser regression batch 4A

## Identitet provjere

- commit: `18a9d01641a135b4b0392daf3c731d604bd29d74`
- timestamp: `2026-09-12T06:44:53+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch4a-smoke-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `kraljevska_pozornica` | PASS | PASS | body `rgb(22, 7, 11)`; lokalni JPG i višestruki gradijenti na `body::before`; dekorativni `body::after` |
| `dimni_akordi` | PASS | PASS | body `rgb(33, 19, 13)`; lokalni PNG + gradijent na `body::before` |
| `sjene_ulice` | PASS | PASS | body `rgb(22, 18, 16)`; lokalni PNG + gradijent na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- HTTP 200 za odgovarajući lokalni background asset
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch4a-smoke-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i aktivni tematski pseudo-background/gradient
- završni stop pseudo-overlaya odgovara computed body boji

## Pseudo slojevi i mrežna izolacija

Za sva tri dizajna `body::before` je aktivan s očekivanim lokalnim background assetom i gradijentima. `kraljevska_pozornica` dodatno ima aktivan zasebni `body::after` dekorativni sloj. `dimni_akordi` i `sjene_ulice` namjerno nemaju `body::after` background. URL-ovi pronađeni u pseudo slojevima vode isključivo na lokalni `/static/` origin; vanjska mreža nije korištena.

## Provjera vidljivosti layouta

Vidljivost nije zaključena samo iz DOM prisutnosti. Za lijevu i desnu kolonu te calendar/archive provjereni su computed `display`, `visibility`, `opacity` i nenulte dimenzije. Svaka od šest kombinacija imala je stvarno vidljivu instancu svakog traženog elementa.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na početni `kraljevska_pozornica` ključ
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Preostali shared tematski i special/full-custom dizajni ostaju za zasebne serijske batch-eve.
