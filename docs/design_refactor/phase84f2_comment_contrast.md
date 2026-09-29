# Phase 84f2 — Litica/Podvodna comment contrast

## Scope

This phase fixes the two P1 findings confirmed by Phase 84f1 without changing
the photographic identity or styling outside the comment area:

- `podvodna_tisina` desktop comment-author contrast;
- unauthenticated comment guidance in `litica_noci` and `podvodna_tisina`.

## Implementation

The guidance selector is limited to a direct `.small.text-muted` child of the
`comments-*` container and uses muted blue `#b8c9e5`. `podvodna_tisina` alone
uses its existing body-text blue `#d5e5ff` for comment-author links from 768 px
up. Mobile author styling is unchanged.

## Verification

An isolated migrated SQLite copy supplied one post and comment per design.
Edge rendered blog and post-detail at 320, 390, 768 and 1440 px (16 states).

- Litica guidance improved from 1.36:1 to 12.52:1.
- Podvodna guidance improved from 1.31:1 to 12.10:1.
- Podvodna comment-author remains 4.52:1 at 320/390 and improves from 1.52:1
  to 5.37:1 at 768/1440.
- Every state has `scrollWidth == clientWidth`.

Safe post-detail and previous-month clicks succeeded for both designs; no
mutating control was used. The focused tests, `manage.py check`, migration drift
check and complete Django suite all pass.
