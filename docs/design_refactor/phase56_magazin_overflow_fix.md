# Phase 56 — Magazin horizontal overflow fix

## Problem

Prvi pokušaj Phase 56 browser provjere na commitu `a061b01e236f8b086a601e6f2a7ae38929f0c65e` otkrio je 7 px horizontalnog `body` overflowa u full-custom `magazin` layoutu na desktop i mobile viewportu. `overflow-x: hidden` skrivao je simptom, ali nije uklanjao uzrok.

Na mobile viewportu 390×844 dokument je imao client širinu 375 px, dok su `.container-fluid.mt-3` i `.blog-main-layout-row` koristili `width: 100vw` (390 px) uz `calc(50% - 50vw)` margine. Kontejner je zato bio pomaknut na približno −7,67 px, a `body.scrollWidth` bio je 382 naspram `body.clientWidth` 375.

## Uski popravak

Samo u `magazin.html`:

- full-width kontejner i oba layout-row pravila koriste `width: 100%` umjesto `100vw`
- centrirajući negativni `calc(50% - 50vw)` margini zamijenjeni su nulom

Layout i dalje zauzima cijelu raspoloživu client širinu, ali više ne uključuje širinu vertikalnog scrollbara. Desktop 290 px sidebar, mobile stacking i vizualni identitet ostaju nepromijenjeni.

## Trajna regresija

Dodan je Django render test koji potvrđuje:

- da `magazin` renderira `blog/designs/magazin.html`
- da template više ne sadrži `width: 100vw !important` ni `calc(50% - 50vw)`
- da full-width kontejner koristi `width: 100%` i nulte horizontalne margine

## Browser verifikacija

- baza: izolirana SQLite kopija lokalne baze
- public URL: `/blog/magazin-fix-author/`
- rezultat: **PASS — 2/2 viewporta**

| Viewport | Client širina | Kontejner | Post | `documentElement` / `body` overflow |
|---|---:|---:|---:|---:|
| 1440×900 | 1425 px | 1424.67 px | 760 px | 0 / 0 |
| 390×844 | 375 px | 374.67 px | 346.67 px | 0 / 0 |

Na oba viewporta potvrđeni su:

- HTTP 200 za javnu stranicu i lokalni `soho_sunrise_valley.jpg`
- `.magazin-main-shell`, body `rgb(220, 233, 227)` i lokalni hero asset
- bez page/console grešaka
- vidljivi blog title, post title/meta/body/actions/comments
- vidljivi Magazin sidebar, calendar i archive

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- izolirana baza je uklonjena
- razvojni server je ugašen
- viewport je resetiran i probni browser tab zatvoren
- `nebeska_klasika` nije uključena u ovu fazu
