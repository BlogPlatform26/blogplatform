# Phase 83g — `staza_prema_vrhovima` contrast stabilization

## Scope

This narrow remediation covers the post author, post actions and comments that
Phase 83a found dependent on the mountain photograph. Interactive archive and
calendar controls were checked and receive the same stable surface. Existing
mobile and tablet touch-target contracts are unchanged.

## Change

- Post author and action rows use an opaque dark-earth surface with warm alpine
  text and links.
- Comment cards use the same opaque surface with explicit body and author-link
  colours at every viewport.
- Archive links, post-bearing calendar days and calendar navigation use the
  same mountain palette without changing their dimensions.

## Verification contract

Focused tests render blog and post-detail routes, assert the local surface and
link contract, and ensure an unrelated bespoke design does not receive it.
Browser verification uses an isolated database at 320, 390, 768 and 1440 px.

The baseline reproduced the generic blue author link and translucent action,
comment, calendar and archive surfaces. After the change, computed contrast was
12.13:1 for author/action/calendar/archive links and comment authors, and
12.97:1 for comment text. Both blog and post-detail retained zero document-level
horizontal overflow at all four widths.

Real, non-mutating clicks reached the canonical post-detail route and the
previous-month calendar query. No like or content mutation was performed.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 70/70 tests.

This does not complete the visual audit of all 37 designs.
