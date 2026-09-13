# Phase 72 — Bespoke date editor contracts

## Root cause and scope

Six bespoke post-card templates exposed only a fixed `d.m.Y` primary date even
though the editor stored the shared date style, effect, colors, and scale:

- `ponocna_elegancija`;
- `ruzicasti_vrt`;
- `stara_aleja`;
- `staza_prema_vrhovima`;
- `jedro_u_suton`;
- `misticno_jezero`.

Each card now includes one small `bespoke_post_date.html` partial. The partial
uses the centralized Phase 69 `blog-date-shell` contract while each caller
retains its existing `pe/rv/sa/spv/jus/mj-post-date` wrapper class, position,
spacing, and design-specific fallback identity. Magazin, Studio, Nebeska, the
service layer, models, routes, and migrations were not changed. The complete
timestamp beside the author remains present.

## Permanent regression coverage

Focused render coverage sends every bespoke design through all 10 registered
date styles. The three effects are rotated across every design and scale values
are varied from 70% to 165%. Every response must contain exactly one primary
shell, the expected design wrapper/style/effect classes, both shared internal
representations, and the persisted scale variable.

The live-editor workflow test separately verifies that a bespoke template:

- saves style, effect, both colors, and scale;
- resets those fields to that template's defaults;
- leaves another bespoke template's values unchanged through save and reset.

The existing 37-design registry test continues to require one primary date and
the author-line timestamp for every active design.

## Isolated editor and browser verification

Verification used a fresh migrated `db_browser_phase72.sqlite3`, dedicated
users/posts, port 8048, and a temporary in-app browser tab. The original
database, media, and port 8000 were untouched.

The real editor UI changed Ponoćna elegancija to ribbon + gradient, colors
`#123456` / `#abcdef`, and 145%. The iframe updated immediately, the inactive
main representation measured 0×0, and the inline representation was visible.
A real save completed its POST/redirect/reload flow; a direct read of the
isolated database confirmed all five persisted values. Jedro u suton separately
proved the split row live preview: main direction `row`, inline 0×0, gradient
colors active, and 135% scale.

The public-browser sweep covered all six designs in both default
`classic_vertical`/solid/100% and styled ribbon-or-split/gradient/145% states,
at 1440×900 and 390×844. All 24 renders had:

- exactly one visible primary shell;
- exactly one visible internal representation and a 0×0 inactive one;
- no representation overlap;
- the expected effect and scale;
- the full timestamp beside the author;
- document/body horizontal overflow `0 / 0`;
- no browser console warnings or errors.

The viewport override was reset, the browser tab and server were closed, and
the isolated database was removed after verification.

## Automated gates

- focused render and live-editor modules: 20/20 passed;
- `python manage.py check`: 0 issues;
- `python manage.py makemigrations --check --dry-run`: no changes;
- complete available Django suite: 30/30 passed;
- `git diff --check`: clean.
