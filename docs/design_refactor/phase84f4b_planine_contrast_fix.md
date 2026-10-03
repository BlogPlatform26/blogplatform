# Phase 84f4b — `planine_u_magli` card contrast fix

## Scope

This phase fixes only the deterministic card-surface contrast failures from
Phase 84f4a. The rules are local to `planine_u_magli`; the photographic hero,
desktop layout, tablet touch sizing and tablet numeric overflow investigation
remain unchanged.

An isolated migrated SQLite database used a fresh author with empty design
preferences, one published post and one reader comment. Real-browser checks
covered blog and post-detail at 320, 390, 768 and 1440 px.

## Implementation

- `#43566c` is the common dark mountain-slate ink for the actual post-author
  anchor, like button and all post actions, comment-author link, archive link
  and calendar navigation.
- `#4a5663` is the comment-body ink.
- Hover states use the darker `#304256`.

No card geometry, photographic layer or shared design CSS was changed.

## Measured results

Minimum contrast across the eight states:

| Target | Before | After |
| --- | ---: | ---: |
| post author | 4.28:1 | 7.17:1 |
| post actions / like | 4.28:1 | 7.17:1 |
| comment text | 4.44:1 | 5.96:1 |
| comment author | 3.02:1 | 6.00:1 |
| calendar navigation | 4.07:1 | 7.26:1 |
| archive link | 3.70:1 | 7.34:1 |

At 768/1440, comment text and author rise to 7.25:1 and 7.29:1. No visible
non-Leaflet element crossed the viewport. The fresh fixture still produced a
small numeric tablet discrepancy (`scrollWidth - clientWidth` 10 px) without a
visible escaping element; Phase 84f4a's broader fixture reported 32 px. This
remains an explicitly separate P2 investigation rather than part of the colour
fix.

Safe navigation at 390 px passed for “Otvori post” and previous month. Desktop
visual inspection confirmed that the panoramic mountain photograph, glass-card
layout, spacing and header remain unchanged.

## Automated verification

A narrow render-contract test checks blog/detail output, the real child author
anchor, like/action selector, comment, archive and calendar-navigation rules,
plus isolation from `nebeski_mir`. Django system checks, migration drift and
the full test suite are the final gate.

## Remaining work

- Phase 84f4c: photograph-independent title/tagline protection that preserves
  the panoramic hero.
- P2: post-action touch targets at 768 px and the unexplained tablet numeric
  width discrepancy.
- Phase 84f audit: `nebeski_mir` remains unaudited.
