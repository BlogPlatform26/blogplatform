# Phase 55 — Soho mobile column fix

## Problem

Browser Regression Batch 5A na commitu `ebe07848fa1975ab8a4c34a9a6d360c27df4a731` otkrio je stvarni responsive kvar za `soho` (`studio.html`). Na viewportu 390×844 desktop pravila s `!important` zadržavala su sidebar na 286 px i sadržaj na `calc(100% - 286px)`. Post je pao na približno 61 px, a naslov, body, actions i comments na computed širinu 0 px.

## Uski popravak

Postojeći Soho media query `max-width: 991.98px` sada za lijevu i sadržajnu kolonu eksplicitno postavlja:

- `flex: 0 0 100% !important`
- `max-width: 100% !important`
- `width: 100% !important`

Time mobile pravilo nadjačava samo ranija fiksna Soho desktop pravila. Desktop raspored i vizualni identitet nisu promijenjeni.

## Trajna regresija

Dodan je Django render test koji potvrđuje:

- da se ključ `soho` razrješava u `blog/designs/studio.html`
- da renderirani responsive CSS sadrži sva tri obvezna 100% mobile overridea s `!important`

## Browser verifikacija

- baza: izolirana SQLite kopija lokalne baze
- public URL: `/blog/soho-fix-smoke-author/`
- rezultat: **PASS — 2/2 viewporta**

| Viewport | Sidebar / content | Post | Body / actions / comments | Rezultat |
|---|---|---:|---:|---:|
| 1440×900 | 286 px / 1066.67 px | 820 px | 758.67 px | PASS |
| 390×844 | 350.67 px / 350.67 px | 314.67 px | 253.33 px | PASS |

Na oba viewporta potvrđeni su:

- HTTP 200 za javnu stranicu i lokalni `soho_sunrise.jpg`
- `soho-main-shell` marker, body `rgb(236, 231, 223)` i lokalni hero asset
- bez page/console grešaka
- `documentElement` i `body` horizontalni overflow `0`
- vidljivi naslov bloga, post title/meta/body/actions/comments
- vidljivi Soho sidebar, calendar i archive

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- izolirana baza je uklonjena
- razvojni server je ugašen
- viewport je resetiran i probni browser tab zatvoren
- `magazin` i `nebeska_klasika` nisu uključeni u ovu fazu
