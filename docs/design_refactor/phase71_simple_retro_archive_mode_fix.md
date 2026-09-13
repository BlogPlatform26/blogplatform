# Phase 71 — Simple Retro archive mode fix

## Root cause and minimal correction

The `simple_retro` branch in `blog_right_sidebar.html` rendered its bespoke
calendar and archive list unconditionally. Other designs already respected
`blog_preferences.blog_archive_mode`, but this branch bypassed those guards, so
choosing `calendar` or `list` still displayed both widgets.

The correction stays inside the existing `simple_retro` branch:

- the calendar renders for `both` or `calendar`;
- the archive list renders for `both` or `list`.

No model, service, migration, route, stylesheet, or other design branch was
changed.

## Permanent regression coverage

The active-design render matrix now exercises `simple_retro` in all three
modes and asserts exact calendar/archive exclusivity. When present, the
calendar must retain its previous/next-month links and the archive list must
retain the user-blog `?year=` query route.

## Isolated browser verification

Verification used the migrated `db_browser_phase71.sqlite3`, a dedicated
`phase71retro` user and post, port 8047, and temporary in-app browser tabs. The
original database, media, and port 8000 were untouched.

At desktop size and 390×844:

- `both`: calendar and archive list visible;
- `calendar`: calendar visible, archive list absent;
- `list`: archive list visible, calendar absent;
- previous/next-month and archive query routes remained intact when their
  respective widgets were present;
- document/body horizontal overflow was 0;
- browser console contained no warnings or errors.

The temporary viewport override was reset and the browser tab/server were
closed after the check.

## Automated gates

- targeted active-design matrix: 8/8 passed;
- `python manage.py check`: 0 issues;
- `python manage.py makemigrations --check --dry-run`: no changes;
- complete available Django suite: 28/28 passed;
- `git diff --check`: clean.
