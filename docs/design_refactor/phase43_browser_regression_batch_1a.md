# Phase 43 — browser regression batch 1A

## Identitet provjere

- commit: `10daed26df5a67879db5889d79b1f5731a436555`
- timestamp: `2026-09-12T01:09:42+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch1-smoke-author/`
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni template marker |
|---|---:|---:|---|
| `default` | PASS | PASS | body background `rgb(255, 255, 255)` |
| `dark` | PASS | PASS | body background `rgb(17, 17, 17)` |
| `classic` | PASS | PASS | body background `rgb(246, 246, 244)` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv `.blog-page-title`
- vidljiv `.blog-post-entry` i njegov `h4`
- post meta s autorom, `#batch1-smoke-body`, `.post-actions` i `[id^="comments-"]`
- oba glavna sidebar stupca, `.calendar-box` i `.archive-box`
- očekivani computed body background kao različit aktivni marker svakog templatea

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na `default`
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Batch 1A obuhvaća samo `default`, `dark` i `classic`. Desni layouti, Simple dizajni i ostali aktivni dizajni ostaju za zasebne serijske batch-eve.
