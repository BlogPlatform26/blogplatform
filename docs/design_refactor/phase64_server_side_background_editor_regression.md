# Phase 64 — Server-side background editor regression

## Scope

Added persistent Django coverage for the background branch of the existing
`design_live_editor_titles` view. Production code, models, migrations, and the
real SQLite database were not changed.

## Covered contracts

- The background editor is available only for `simple_pattern`,
  `simple_retro`, and `simple_image`; a non-simple design is redirected to the
  title section and does not create a preference row.
- `simple_pattern` and `simple_retro` persist their allowed gradient/pattern
  modes, colors, pattern, direction, content background, and box background.
- Their header is intentionally normalized to one color: the view stores
  `header_background_mode=color` and the same value in both header colors.
- `simple_image` persists a selected system image without changing another
  template's customization.
- A valid uploaded image is stored under the profile and switches the active
  mode to `upload_image`.
- Delete removes the uploaded profile file, while reset-all restores the
  active `simple_image` background defaults and preserves another template's
  customization.
- Upload tests use a temporary `MEDIA_ROOT`; the original media and
  `db.sqlite3` are untouched.

## Verification

- Targeted workflow tests: 10/10 passed.
- `python manage.py check`: passed.
- `python manage.py makemigrations --check --dry-run`: no changes.
- Full Django suite: passed.

Browser live-preview verification remains a separate phase: `simple_pattern`
will cover pattern/gradient behavior and `simple_image` will cover system and
uploaded image behavior.
