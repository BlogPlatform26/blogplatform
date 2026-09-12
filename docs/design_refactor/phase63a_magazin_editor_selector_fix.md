# Phase 63a — Magazin editor selector fix

## Confirmed defect

The live editor correctly updated the shared title/date CSS variables for
`magazin`, and the post title and date reacted. The concrete
`.magazin-blog-title`, `.magazin-section-title` and
`.magazin-calendar-title` elements did not react to blog/box font, color or
size changes.

The cause was not the Magazin theme variables. Those already represented the
saved font and color values. The affected elements were missing from the
shared semantic selector contract used by both the live-editor runtime and the
persisted base CSS. Size customization therefore also did not apply after a
normal public render.

## Minimal fix

The Magazin markup now identifies existing elements with the established
semantic classes:

- `.magazin-blog-title` also has `.blog-page-title`;
- calendar, archive, month and user-box title elements also have `.box-title`.

No global selector or other design template was changed. Magazin keeps its
layout, typography fallbacks, casing, spacing and visual identity while the
existing editor contract can target these elements.

## Permanent regression

`ActiveDesignRenderMatrixTests` now asserts that the rendered Magazin blog
contains the shared semantic classes on the concrete blog, calendar, month and
archive title elements.

## Browser and persistence evidence

The real live editor was exercised at `1440x900` with an isolated migrated
SQLite database and a dedicated `magazin` user. Before saving, the following
computed styles were observed on the actual Magazin DOM:

- `.magazin-blog-title`: Arial, `#123456`, `61px`;
- `.magazin-post-entry h4`: Verdana, `#234567`, `37px`;
- `.magazin-section-title`, `.magazin-calendar-title` and the concrete user-box
  title: Tahoma, `#345678`, `19px`;
- `.blog-date-shell`: `ribbon` and `duo`, using `#456789`, `#56789a` and
  scale `123` through the shared date variables.

The current browser-control build focused and activated the visible submit
button but did not execute its native default submit action: the URL stayed
unchanged and the development-server log contained no POST. This is recorded
as a test-tool limitation, not reported as a successful UI click.

To complete the application-level persistence proof, the same Django URL/view
was submitted against the same isolated database with the complete payload.
It returned `302` to `?section=naslovi`. Reloading the real browser editor and
iframe then showed the saved control values and the same computed styles on
the actual Magazin elements. The server reset-all POST likewise returned
`302`; a subsequent real public browser render showed the normalized Magazin
defaults again.

At `390x844`, blog title, post title, calendar/month/box titles and date were
visible. Both document-element and body horizontal overflow were zero. Browser
console warnings/errors were zero.

The temporary tab was closed, its viewport override reset, the development
server stopped, and the isolated database removed. The original `db.sqlite3`
was not used or modified.

## Result

PASS for the application selector, live-preview, persistence and reset
contracts. Nebeska klasika remains intentionally outside Phase 63a.
