# Phase 83i — Nebeska klasika contrast

## Scope

This narrow remediation covers the post author and action contrast identified
by Phase 83a for `nebeska_klasika`. Comment, archive and calendar contrast was
verified at the same time without repeating touch-target work.

## Implementation

- Post author/action rows, archive links and month navigation use an opaque
  warm-white surface with a darker celestial-blue action color.
- Comment cards use the same opaque surface; comment text and author links no
  longer depend on the fixed background photograph.
- Post-bearing calendar days use a darker celestial-blue surface with white
  text.
- Layout dimensions, title/hero treatment and shared mobile/tablet target rules
  remain unchanged.

## Verification

An isolated migrated database contained a synthetic author, reader, published
post and two comments. Browser checks covered blog and post-detail at 320, 390,
768 and 1440 px, with no document overflow at any width. All remediated light
surfaces computed opaque. Measured contrast is 6.79:1 for celestial-blue
author/action/archive/comment-author links, 7.87:1 for comment text and 5.72:1
for post-bearing calendar days.

Safe clicks opened the canonical post-detail URL and previous-month calendar
query without like or content mutation. The original database, media and port
8000 were not used.

Final gates:

- targeted contrast and mobile post-action contracts: pass;
- `manage.py check`: no issues;
- `makemigrations --check --dry-run`: no changes;
- full Django suite: 74/74 tests passed.
