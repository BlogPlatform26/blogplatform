# Phase 69 — Primary date style runtime fix

## Corrected diagnosis

Phase 68 correctly added one semantic primary-date marker per post card, but it
misidentified the visible duplication. The author timestamp is intentional and
has been restored. The defect was inside a single `blog-date-shell`: special
templates rendered both `.blog-date-main` and `.blog-date-inline` because they
did not receive the shared display/style contract from
`blog_design_styles.html`.

Before the fix, browser computed styles for Magazin, Soho/Studio, and Nebeska
klasika all reported `classic_vertical`, `mainDisplay=block`,
`inlineDisplay=block`, and no shared date stylesheet marker. At large gradient
scales this produced the reported competing date representations.

## Centralized fix

The complete reusable date runtime was extracted unchanged to
`blog/components/blog_date_styles.html` and is included once from the common
`base.html` head. Special templates now receive only the date contract—not all
standard theme CSS—and standard templates no longer duplicate those rules in
`blog_design_styles.html`.

The extracted contract preserves:

- `classic_vertical`, `slim_vertical`, `card`, `minimal_inline`, `split`,
  `ribbon`, `boxed_number`, `corner_tag`, `soft`, and `newspaper`;
- `solid`, `duo`, and `gradient` effects;
- the `--post-date-scale` calculation and all existing style-specific sizing;
- the mobile alignment rules for inline styles.

The full `d.m.Y H:i` timestamp is again present after the author in
`post_actions.html`. The primary card date and author metadata have separate
semantic purposes.

## Permanent regression coverage

The registry-driven render matrix now checks all 37 active designs for exactly
one primary-date marker and exactly one centralized stylesheet contract. It
also requires the author timestamp. A focused contract test asserts all ten
style families, all three effects, scaling, vertical/inline visibility rules,
and the row-style selector family. The complete suite now contains 27 tests.

## Browser verification

The run used a fresh migrated `db_browser_phase69.sqlite3`, dedicated user and
post, port 8045, and a temporary in-app browser tab. The original database,
media, legacy data, and port 8000 were untouched.

Before the change, Magazin, Soho, and Nebeska each showed both internal
representations as `block`. After a fresh server start:

- `classic_vertical`: main `flex`, inline `none`;
- `minimal_inline`, `ribbon`, `corner_tag`: main `none`, inline `flex`;
- `split`: main `flex` in row direction, inline `none`;
- gradient effect remained active;
- 70% and 170% scales produced calculated factors `0.7` and `1.7` and day
  sizes 23.8 px and 57.8 px in the tested row style;
- the inactive representation had a zero bounding rectangle, so it could not
  overlap the active representation.

The Nebeska live editor dropdown changed the actual iframe classes and computed
visibility. A real UI save returned the expected POST/302/GET cycle; reload
retained ribbon + gradient + 170%. UI reset-all returned to
classic_vertical + solid + 100%, with main visible and inline hidden.

Public renders for Magazin, Soho/Studio, and Nebeska retained the timestamp,
loaded one stylesheet contract, and showed only the correct representation.
All three also passed at 390×844 with a visible date and document/body
horizontal overflow `0 / 0`. The browser console contained no warnings or
errors. No independent editor defect or Phase 70 gap was found.

## Automated gates

- targeted active-design matrix: 7/7 passed;
- `python manage.py check`: 0 issues;
- `python manage.py makemigrations --check --dry-run`: no changes;
- complete available Django suite: 27/27 passed;
- `git diff --check`: clean.
