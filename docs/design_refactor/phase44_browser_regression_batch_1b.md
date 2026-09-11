# Phase 44 — browser regression batch 1B

## Identitet provjere

- commit: `5bfc042dbf96ec71326f6756aac7ceb39b2e3edf`
- timestamp: `2026-09-12T01:15:51+02:00`
- baza: izolirana SQLite kopija lokalne baze
- fixture: jedan probni autor, jedan objavljeni post i jedan komentar
- public URL: `/blog/batch1b-smoke-author/`
- desni layout: podržani `right_box_columns='1'` način s calendar/archive sadržajem u desnom sidebaru
- rezultat: **PASS — 6/6 design/viewport kombinacija**

## Dizajni i viewporti

| Ključ | 1440×900 | 390×844 | Aktivni template markeri |
|---|---:|---:|---|
| `default_right` | PASS | PASS | `blog-posts-shell--wide`; body `rgb(255, 255, 255)` |
| `dark_right` | PASS | PASS | `blog-posts-shell--wide`; body `rgb(17, 17, 17)` |
| `classic_right` | PASS | PASS | `blog-posts-shell--wide`; body `rgb(246, 246, 244)` |

## Gates

Na svakoj kombinaciji potvrđeni su:

- uspješan public-page load bez error stranice; lokalni server vraća HTTP 200
- nema browser console error zapisa
- `documentElement` i `body` horizontalni overflow iznose `0`
- vidljiv `.blog-page-title`
- vidljiv `.blog-post-entry`, njegov `h4`, post meta s autorom, `#batch1b-smoke-body`, `.post-actions` i `[id^="comments-"]`
- vidljiv `.blog-main-right-column` s `.calendar-box` i `.archive-box`
- desktop: desni sidebar nalazi se desno od glavnog sadržaja
- mobile: desni sidebar pravilno je složen nakon glavnog sadržaja
- aktivni `blog-posts-shell--wide` marker i očekivani computed body background

## Izolacija i cleanup

- originalni `db.sqlite3` nije mijenjan
- probni profil vraćen je na `default_right`
- izolirana probna baza uklonjena je nakon provjere
- privremeni viewport override je resetiran
- lokalni development server je ugašen
- browser nije ostavljen kao deliverable

## Preostalo

Simple dizajni i ostali aktivni dizajni ostaju za zasebne serijske batch-eve.
