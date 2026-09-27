# Phase 83d — `ruzicasti_vrt` contrast stabilization

## Scope

This narrow remediation covers the post author, post actions/open-post link,
comment authors and comment text identified by Phase 83a. Archive and calendar
links were included because their translucent surfaces had the same dependency
on the photograph. Tablet touch-target dimensions remain a separate phase.

## Change

- Post author and action rows use an opaque blush surface with dark berry text.
- Comment cards use an opaque blush surface with explicit body and author-link
  colours at every viewport.
- Sidebar cards, archive links, active calendar days and calendar navigation use
  stable pale-rose surfaces while preserving the garden's pink identity.

## Verification contract

The focused regression tests render the blog and post-detail routes, check the
local contrast contract, and ensure another bespoke design does not receive the
rules. Browser verification uses an isolated database and covers 320, 390, 768
and 1440 px.

The browser run recorded the original translucent/photographic state first,
then repeated both blog and post-detail at every viewport. Final computed
opaque-surface contrast was 9.21:1 for author/action/archive/calendar links,
10.62:1 for comment text and 8.61:1 for comment-author links. A real `Otvori
post` click reached the canonical detail route. No viewport produced
document-level horizontal overflow.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 66/66 tests.

This does not complete the visual audit of all 37 designs.
