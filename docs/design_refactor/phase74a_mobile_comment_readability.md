# Phase 74a — mobile comment readability and actions

## Scope and implementation

The shared comment component now exposes edit/delete controls without hover on narrow or hoverless devices. The controls are 44 × 44 px and flow above the comment header instead of covering it. At widths up to 576 px, comment text and textareas use 16 px, while the existing 12 px desktop comment typography remains unchanged.

The former translucent mobile comment surface inherited each design's foreground through `color-mix`. That was insufficient over photographs and for some low-contrast gradients. Six measured exceptions now receive design-specific, opaque comment surfaces and matching ink/link colours: `jedro_u_suton`, `stara_aleja`, `nebeski_mir`, `sumska_svjetlost`, `polarna_svjetlost`, and `zlatno_polje`. The change targets comment cards only; page/post headings and other desktop styling are untouched.

## Browser evidence

The browser ran against a disposable workspace copy of the synthetic `mobile_trial.sqlite3` database on port 8056, never against the original `db.sqlite3` or media. One synthetic post and comment were present in each of the 37 registered designs.

- All 37 post-detail pages at 320 px rendered a 16 px comment body without document-level horizontal overflow.
- Six targeted designs at both 320 and 390 px rendered the expected solid background and text colours, with no document-level overflow. Calculated text/background WCAG ratios were 17.69, 14.42, 9.42, 9.88, 15.35, and 10.95 respectively in the design order listed above. Author-link ratios were 7.59, 13.07, 10.85, 7.95, 13.80, and 9.67 respectively. These ratios apply to the solid cards, not the whole page or photograph.
- `jedro_u_suton` was checked on both post detail and user blog; the same solid card and 16 px text appeared on each. Before the fix, its forced near-black text over a translucent photographic surface was visibly hard to read.
- As the synthetic comment owner on a 390 px `jedro_u_suton` post, Edit was visible and clickable with a 44 × 44 px target. It opened the editing form; Cancel restored the comment. No edit or deletion was submitted.
- At 1440 px, representative `default`, `dark`, `stara_aleja`, and `jedro_u_suton` posts retained 12 px comment text and their pre-existing desktop surfaces.

This is not a pixel-level WCAG audit of every background position in all 37 designs. The 31 non-exception designs were checked for computed mobile size and overflow; photographic regions and all desktop comment contrast combinations remain separate review work.

## Automated gates

- New targeted regression tests: 3/3 passed.
- Full Django suite: 34/34 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.

No database migration or production operation is part of this phase.
