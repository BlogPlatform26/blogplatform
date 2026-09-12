# Phase 62 — browser editor title/date workflow

## Scope and isolation

The active live editor was exercised in a real browser for the representative
`default_right` design at desktop `1440x900` and mobile `390x844` viewports.
The run used a temporary migrated SQLite database,
`db_browser_phase62_fc2b768.sqlite3`, and a dedicated test user. The original
`db.sqlite3` was not used or modified.

The temporary profile contained a published post, left and right user boxes,
and a sentinel customization for `classic`. This made the iframe content and
cross-template preservation observable.

## Live preview before save

The following representative values were changed through the visible editor
controls:

- blog title: Arial, `#123456`, `61px`;
- post title: Verdana, `#234567`, `37px`;
- box title: Garamond, `#345678`, `19px`;
- post date: `ribbon`, `duo`, `#456789`, `#56789a`, `123%`.

Before saving, the iframe's `html` and `body` received the corresponding
`--blog-title-*`, `--post-title-*`, `--box-title-*` and `--post-date-*` CSS
variables. Computed styles on the visible blog, post and calendar titles
matched the selected colors, fonts and sizes. The date shell immediately used
`blog-date-style-ribbon` and `blog-date-effect-duo`.

## Save and reload persistence

Clicking **Spremi promjene** produced the expected POST `302`, followed by GET
of `?section=naslovi`. All 14 controls retained their values after reload. The
iframe and public blog render also retained the CSS variables and matching
computed styles. Desktop iframe document and body horizontal overflow were
both zero.

The isolated `UserBlogPreference` contained the values under
`data.design_customizations.default_right`. The separately seeded `classic`
key remained unchanged.

## Individual reset

The blog-title controls were temporarily changed to Tahoma, `#abcdef` and
`80px`. Clicking that card's `data-reset-card="blog"` button:

- kept the current URL and did not cause a server POST;
- restored only that card to Georgia, `#3f3128` and `32px`;
- left the customized post title and date controls unchanged;
- immediately restored the iframe variables and computed blog-title styles.

After clicking **Spremi promjene**, the reset blog-title defaults and the other
customized cards remained persistent through the POST/redirect/reload cycle.

## Server reset-all

Clicking **Vrati sve naslove** produced another POST `302` and reload. All
active title/date values returned to the normalized `default_right` defaults:

- title fonts Georgia, colors `#3f3128` / `#111827` / `#3f3128`, sizes
  `32px` / `24px` / `13px`;
- date `classic_vertical`, `gradient`, `#7a2cff`, `#ffd200`, `100%`.

The isolated database confirmed that the active values matched their defaults
and the sentinel `classic` colors remained `#a1b2c3` and `#b1c2d3`.

## Responsive and runtime checks

At `390x844`, the editor form and scaled preview iframe remained visible. The
outer editor document, iframe document and iframe body all reported zero
horizontal overflow. Blog title, post title, box title and date remained
visible. The iframe internally retained its desktop rendering width and was
scaled into a `341px`-wide shell as intended.

No browser console warnings or errors were recorded. All editor, iframe and
static asset requests used successful `200`/`302` responses; the server log
showed exactly the expected three editor POSTs (initial save, save after the
individual client reset, and reset-all). The temporary browser tab was closed,
the viewport override was reset, the development server was stopped, and the
temporary database was removed.

## Result

PASS. No functional defect was found in the representative
`default_right` title/date workflow. Background-editor branches and bespoke
special-design selector families remain outside this phase.
