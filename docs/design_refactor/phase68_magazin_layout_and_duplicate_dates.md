# Phase 68 — Magazin layout and duplicate dates

## Scope and isolation

This phase addresses two related regressions reported after the Phase 67
completion audit:

1. the Magazin main/hero column could wrap below a tall left sidebar on desktop;
2. posts showed a primary styled date and repeated the full timestamp in the
   shared author/actions line.

The browser pass used a fresh migrated `db_browser_phase68.sqlite3`, a dedicated
user and post, six deliberately tall left/right boxes, port `8044`, and a
temporary in-app browser tab. The original `db.sqlite3`, media, legacy data, and
the user's server on port 8000 were not touched.

## Root causes and minimal fixes

### Magazin desktop wrapping

Magazin gave its 290 px sidebar a fixed flex basis and its main column
`calc(100vw - 290px)`. The row's available content width can be narrower than
`100vw` because the viewport includes the vertical scrollbar. The two columns
therefore exceeded the row and Bootstrap's wrapping flex row moved the main
column below the complete sidebar.

Only Magazin's main-column calculation changed: `100vw` became `100%`. The
column now consumes the row remainder rather than the viewport remainder. Its
existing mobile 100% rule and visual design remain unchanged.

### Duplicate dates

A static review of the authoritative render paths found that every one of the
37 active registry designs already renders a primary date in its post card:

- the 28 standard/shared designs use `components/post_card.html`;
- the 9 special designs use their specific post-card partial (Soho resolves to
  the Studio card).

Every path also includes `components/post_actions.html`, which repeated
`publication_datetime` after the author. The shared action line was therefore
the single duplicate root cause. The secondary timestamp was removed there,
without changing the author, views, like, comments, or open-post actions. Each
active primary date now exposes the neutral `data-post-primary-date` render
contract so registry-driven tests can prevent missing or repeated primary date
containers without flattening special-design markup.

Inactive legacy `vecer_uz_jezero` and `vecer_zaljubljenih` cards were not
changed; they are not registry paths and no broader cleanup was needed.

## Permanent regression coverage

`ActiveDesignRenderMatrixTests` now verifies for every authoritative registry
key that:

- one and only one `data-post-primary-date` exists for the fixture post;
- the full publication timestamp is absent from the shared author line;
- the author line and all prior post/body/comments/calendar/archive contracts
  still render.

The Magazin CSS regression additionally rejects `calc(100vw - 290px)` and
requires both width declarations to use `calc(100% - 290px)`.

## Browser evidence

At 1440×900 with the tall-sidebar fixture:

- left column: top `54.1875`, left `0`, width `290` px;
- main column: top `54.1875`, left `290`, width `1134.67` px;
- hero: top `54.1875`, left `290`, width `1134.67` px;
- document/body horizontal overflow: `0 / 0`;
- one primary date; author line: `Autor by phase68magazin`.

The equal top coordinates prove that the hero no longer waits for the sidebar.

At 390×844, Magazin retained the intended stack: the main column begins after
the tall sidebar, both columns fit the 374.67 px content width, the post is
346.67 px wide, and document/body overflow remains `0 / 0`.

Desktop date smoke checks passed for Magazin, Soho/Studio, and Nebeska
klasika. Representative additional special checks passed for Jedro u suton on
desktop and Mistično jezero at 390×844. Each rendered exactly one primary date,
kept the author-only shared line, and had zero horizontal overflow. The browser
console contained no warnings or errors; observed page, analytics, and local
asset requests returned successful responses.

## Automated gates

- targeted active-design matrix: 6/6 passed;
- `python manage.py check`: 0 issues;
- `python manage.py makemigrations --check --dry-run`: no changes;
- complete available Django suite: 26/26 passed.
