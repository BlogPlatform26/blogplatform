# Phase 66 — Simple Image background editor workflow

## Scope and isolation

This final background-editor browser pass covered `simple_image` only. It began
at `8aaf25aa6d05fec545a185b7a924ebe37bbf25cd` and used:

- an isolated SQLite database, `db_browser_phase66_8aaf25a.sqlite3`;
- an isolated `tmp_phase66_media` directory selected through a temporary test
  settings module;
- an isolated user whose active template was `simple_image`;
- a seeded `simple_pattern` customization (`color` / `#0d0e0f`) as the
  non-active isolation sentinel;
- a local server on `127.0.0.1:8043` and a temporary browser tab.

The original `db.sqlite3` and real media directory were not used or modified.
All temporary Phase 66 runtime artifacts were removed after verification.

## System-image live preview

At a 1440 x 900 viewport, the background editor opened directly with
`?section=pozadine`. Changing the system image from the initial asset to
`navy_coffee` immediately updated both computed body background layers:

- `body::before`: `navy_coffee.png`
- `body::after`: `navy_coffee.png`

The asset returned HTTP 200 with `image/png`. Live color controls also updated
the real rendered elements:

- header `#1a2b3c` -> `.blog-header-main--simple`;
- content `#d1e2f3` -> `.blog-post-entry`;
- boxes `#f3e2d1` -> calendar, archive, and sidebar boxes.

## Save and reload persistence

The browser controller activated the background submit button, but did not
dispatch a form POST; the page stayed unchanged and the server log contained no
POST request. This is the same controller limitation documented in Phase 65,
not a failed Django response.

The fallback exercised the same `design_live_editor_titles` URL/view with the
same form payload through Django's client against the isolated database. It
returned HTTP 302 to `?section=pozadine`. A real browser reload then confirmed:

- mode `system_image`, asset `navy_coffee`;
- outer colors `#102030` / `#405060` and direction `to right`;
- header `#1a2b3c`, content `#d1e2f3`, boxes `#f3e2d1`;
- both computed public body layers referenced `navy_coffee.png`;
- all controls displayed the persisted values.

The seeded `simple_pattern` key remained `color` / `#0d0e0f`.

## Upload and deletion

A valid small JPEG was posted through the same real multipart view contract.
The response returned HTTP 302, stored mode `upload_image`, and saved a processed
2,385-byte file as `design_backgrounds/custom/phase66-small.jpg` inside the
isolated media root. Browser reload showed that URL in both public body layers,
and the media URL returned HTTP 200 with `image/jpeg`.

Deletion used the same view contract and returned HTTP 302. The profile file
field became empty, the physical file was removed, and browser reload confirmed
that the deleted upload URL no longer appeared in the HTML or computed body
layers. No file in the real media directory was involved.

## Reset and responsive gates

Reset-all through the same URL/view returned HTTP 302. Browser reload confirmed
the `simple_image` defaults:

- mode `system_image`, asset `bookshelf`;
- outer colors `#f5efe6` / `#e8dccf`;
- header `#c8b16b`;
- content and boxes `#fffefb`.

Both computed body layers referenced `bookshelf.png`, which returned HTTP 200.
The seeded `simple_pattern` key still remained `color` / `#0d0e0f`.

At 390 x 844, the editor form and iframe were visible. The editor's document
element and body both had zero horizontal overflow. Inside the iframe, the
header, post, calendar, archive, and sidebar boxes were visible, with zero
document/body overflow. The public blog at the real 390 px viewport showed the
same elements and also had zero document/body overflow.

The browser console contained no warnings or errors. Observed application,
static-asset, and media requests returned expected HTTP 200/302/304 responses;
there were no page or HTTP error responses.

## Automated gates

- `python manage.py check`: passed, 0 issues
- `python manage.py makemigrations --check --dry-run`: no changes detected
- `python manage.py test`: 26/26 passed
