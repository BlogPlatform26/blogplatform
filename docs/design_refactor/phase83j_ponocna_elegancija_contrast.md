# Phase 83j — Ponoćna elegancija contrast

## Scope

This narrow remediation covers the borderline post-author contrast identified
by Phase 83a for `ponocna_elegancija`. Post actions, comments, archive and
calendar controls were checked on the same photographic background.

## Implementation

- Post author/action rows use an opaque midnight-blue surface with warm-gold
  links.
- Comments use the same opaque surface with pale text and gold author links.
- Archive links, post-bearing calendar days and month navigation use the stable
  midnight surface.
- Title treatment, layout geometry and existing mobile/tablet target rules are
  unchanged, preserving the nocturnal desktop identity.

## Verification

An isolated migrated database contained a synthetic author, reader, published
post and two comments. Blog and post-detail were checked at 320, 390, 768 and
1440 px. Every targeted surface computed opaque and each document had
`scrollWidth == clientWidth`.

Measured contrast is 14.49:1 for author/action/archive/calendar and
comment-author links, and 14.63:1 for comment text. Safe clicks opened the
canonical post-detail URL and previous-month query without like or content
mutation. The original database, media and port 8000 were not used.

Final gates:

- targeted contrast and mobile post-action contracts: pass;
- `manage.py check`: no issues;
- `makemigrations --check --dry-run`: no changes;
- full Django suite: 76/76 tests passed.
