# Phase 54 — browser regression batch 4B

## Identitet provjere

- commit: `1b2793fb5091d6008b61033bd1b0ff92206a8acf`
- timestamp: `2026-09-12T11:21:47+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch4b-smoke-author/`
- rezultat: **PASS — 4/4 design/viewport kombinacije**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni theme markeri |
|---|---:|---:|---|
| `mjesecev_ples` | PASS | PASS | body `rgb(21, 17, 15)`; lokalni `mjesecev_ples.png` + gradijent na `body::before` |
| `asfaltni_plamen` | PASS | PASS | body `rgb(23, 17, 13)`; lokalni `asfaltni_plamen.png` + gradijent na `body::before` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- HTTP 200 za odgovarajući lokalni background asset
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv blog title
- vidljiv post card, post title, meta, `#batch4b-smoke-body`, actions i comments
- stvarno vidljivi lijevi/desni sidebar te calendar/archive elementi
- odgovarajuća computed body boja i aktivni tematski pseudo-background/gradient
- završni stop pseudo-overlaya odgovara computed body boji

## Pseudo slojevi i asseti

Za oba dizajna `body::before` je aktivan s očekivanim lokalnim PNG assetom i gradijentom. Theme asset URL-ovi vode isključivo na lokalni `/static/` origin i oba su potvrđena HTTP 200. Zaseban `body::after` background nije definiran za ova dva dizajna.

## Provjera vidljivosti layouta

Vidljivost nije zaključena samo iz DOM prisutnosti. Za lijevu i desnu kolonu te calendar/archive provjereni su computed `display`, `visibility`, `opacity` i nenulte dimenzije. Svaka od četiri kombinacije imala je stvarno vidljivu instancu svakog traženog elementa.

## Dovršena standard/shared matrica

Ovim batch-em svih **28 standard/shared aktivnih design ključeva** browser-provjereno je kroz Phase 43–54 na desktop i mobile viewportima. Special/full-custom dizajni ostaju zasebna matrica.

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na početni `mjesecev_ples` ključ
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable
