# Phase 65 — Simple Pattern background editor workflow

## Scope

Browser smoke-test of the existing background editor for `simple_pattern` only.
No application code, migration, original database, or media file was changed.
`simple_retro` was used only as a seeded non-active customization key to verify
isolation during reset.

## Environment

- Starting commit: `3c82997528bf7ffe053e266525316eab51f96909`
- Isolated SQLite database: `db_browser_phase65_3c82997.sqlite3`
- Isolated local server: `127.0.0.1:8042`
- Desktop viewport: 1440 x 900
- Mobile viewport: 390 x 844

The isolated database, server, and browser tab were removed after verification.
The original `db.sqlite3` and media directory were not touched.

## Desktop live preview

The editor was opened directly with `?section=pozadine`. Switching the outer
background to a gradient immediately produced the computed iframe body value
`linear-gradient(to right, rgb(17, 34, 51), rgb(68, 85, 102))`.

The following controls immediately changed real preview elements:

- header `#778899` -> `.blog-header-main--simple` (`rgb(119, 136, 153)`)
- content `#ddeeff` -> `.blog-post-entry` (`rgb(221, 238, 255)`)
- boxes `#fedcba` -> calendar, archive, and sidebar boxes
  (`rgb(254, 220, 186)`)

Switching to pattern mode and selecting `stars` immediately changed the iframe
body to `pattern-stars.svg`, with computed size `135px 135px`. The asset request
returned HTTP 200 with `image/svg+xml`.

## Save and reload

The browser controller activated the background submit button twice, but it did
not dispatch a form POST; the server log contained no POST request. This is a
controller limitation for this form, not a failed Django response.

The documented fallback used the same `design_live_editor_titles` URL/view and
the same form payload through Django's client against the isolated database.
The response was HTTP 302 to `?section=pozadine`. A real browser reload then
confirmed the saved control values and public computed render:

- outer mode `pattern`, color `#112233`, pattern `stars`
- retained secondary color `#445566` and direction `to right`
- header `#778899`, content `#ddeeff`, boxes `#fedcba`
- body uses `pattern-stars.svg`; header, post, calendar, archive, and sidebar
  boxes all use the saved colors

The seeded `simple_retro` customization remained `color` / `#0a0b0c`.

## Reset

The controller showed the same submit limitation for reset. The same URL/view
fallback returned HTTP 302. Browser reload confirmed the `simple_pattern`
defaults and their public computed render:

- mode `pattern`, pattern `paper`
- colors `#efe4c9` / `#e1d0ac`
- direction `to bottom`
- header `#d98a37`
- content and boxes `#fffefb`

The seeded `simple_retro` key still remained `color` / `#0a0b0c`.

## Responsive and error gates

At 390 x 844, the editor form and iframe were visible. Editor document-element
and body horizontal overflow were both 0. The iframe's header, post, calendar,
archive, and sidebar boxes were visible and its document-element/body overflow
were both 0. The public blog at the real 390 px viewport showed the same
elements with document-element/body overflow both 0.

The browser console had no warnings or errors. Observed application and asset
requests returned expected HTTP 200/302 responses, with no page errors.

## Automated gates

- `python manage.py check`: passed, 0 issues
- `python manage.py makemigrations --check --dry-run`: no changes detected
- `python manage.py test`: 26/26 passed
