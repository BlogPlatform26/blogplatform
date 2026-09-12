# Phase 57 — Nebeska klasika browser regression

## Identitet provjere

- commit: `3207af745468968105a96d9b0a736e9cfd50b538`
- timestamp: `2026-09-12T11:42:11+02:00`
- dizajn: `nebeska_klasika`
- template: `blog/designs/nebeska_klasika.html`
- baza: izolirana SQLite kopija lokalne baze
- public URL: `/blog/phase57-smoke-author/`
- rezultat: **PASS — 2/2 viewporta**

## Viewporti i layout

| Viewport | `.nk-layout` | Post | Sidebar card | Overflow `documentElement` / `body` |
|---|---|---:|---:|---:|
| 1440×900 | grid `658px 250px` | 658 px | 250 px | 0 / 0 |
| 390×844 | jedna kolona `346.67px` | 346.67 px | 346.67 px | 0 / 0 |

## Theme i funkcionalni gateovi

Na oba viewporta potvrđeni su:

- `.nk-theme` full-custom marker i vidljiv `.nk-title`
- computed body `rgb(236, 231, 220)`
- lokalni `nebeska_klasika.jpg` body background i HTTP 200 za asset
- poluprozirni post i sidebar card background `rgba(250, 247, 240, 0.84)` te pripadajući border
- HTTP 200 javne stranice, bez error stranice i browser console grešaka
- `documentElement` i `body` horizontalni overflow `0`
- vidljivi post title, meta, `#phase57-smoke-body`, actions i comments
- vidljiv `.nk-side-stack`, calendar grid i archive list prema očekivanom layoutu

## Zaključena prva posebna skupina

Prva skupina special/full-custom dizajna sada je browser-potvrđena:

- `soho` — Phase 55, nakon uskog mobile column popravka
- `magazin` — Phase 56, nakon uskog horizontal overflow popravka
- `nebeska_klasika` — Phase 57, PASS bez dodatne izmjene koda

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- izolirana baza je uklonjena
- razvojni server je ugašen
- viewport je resetiran i probni browser tab zatvoren
- nije mijenjan produkcijski kod u ovoj fazi
