# Phase 63c — Nebeska klasika editor contract fix

## Scope

Minimal local fix for `nebeska_klasika`: no service, model, migration, or global
CSS changes.

## Changes

- The blog heading now exposes `blog-page-title`.
- The post heading now exposes `blog-post-title`.
- Author, calendar, archive, and custom box headings expose `box-title`.
- Local theme declarations consume the shared title variables while retaining
  the previous Nebeska values as CSS fallbacks.
- The special post card now uses the standard `blog-date-shell` main/inline
  structure and date style/effect hooks.
- A render-contract regression test covers the semantic targets, date markup,
  and local variable fallbacks.

## Browser verification

An isolated SQLite database and local server were used. The original
`db.sqlite3` was not opened or changed.

Through the actual live-editor UI UI, the following values were applied and
saved: Arial / `#123456` / 61 px for the blog title; Verdana / `#234567`
/ 37 px for the post title; Tahoma / `#345678` / 19 px for box titles; and a
123% two-col date ribbon using `#456789` and `#56789a`.

The POST completed with a 302 PRG redirect and success message. After reload,
computed styles matched all values for the blog title, post title, author,
calendar, archive, and date shell. A custom box was also rendered through the
same semantic class. Reset-all completed through the UI and restored the
Nebeska defaults (Georgia and original colors/sizes; classic solid date at
100%). At a 390 x 844 viewport, the blog title, post title, date, sidebar
titles, and custom box remained present in the rendered accessibility tree.

## Automated verification

- `python manage.py check`: passed (0 issues)
- `python manage.py makemigrations --check --dry-run`: no changes
- `python manage.py test`: 22/22 passed

One first full-suite attempt was aborted by a transient Windows memory error
while the browser server and other Django checks were running concurrently.
After those processes were stopped, the full suite was rerun alone and passed.
