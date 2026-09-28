# Phase 83k — Magazin contrast

## Scope

This phase addresses the two P1 findings from Phase 83a for `magazin`: the
borderline post-author/action treatment and the blog tagline disappearing over
light areas of the hero photograph. Comments, archive and calendar contrast
were checked in the same isolated run.

## Implementation

- The hero tagline receives a compact opaque editorial caption with pale text.
- Post author/action rows, archive links and month navigation use opaque warm
  paper with a darker brown action color.
- Comments use the same opaque paper family, while post-bearing calendar days
  use a darker editorial brown with white text.
- The desktop column proportions, hero photograph and shared mobile/tablet
  target rules are unchanged.

## Sidebar overflow

The Phase 83a local `+5 px` sidebar overflow did not reproduce. At 320 px the
sidebar ended at exactly 320 px, its sections ended at 302 px, and document
`scrollWidth` equalled `clientWidth`. No speculative layout change was made.

## Verification

An isolated migrated database contained a synthetic author, reader, published
post and two comments, using the registered `soho_sunrise_valley` system hero.
Blog and post-detail were checked at 320, 390, 768 and 1440 px. Every remediated
surface computed opaque and every document had `scrollWidth == clientWidth`.

Measured contrast is 14.15:1 for the hero tagline, 8.01:1 for author/action,
archive and comment-author links, 7.49:1 for comment text, and 6.49:1 for the
post-bearing calendar day. Safe clicks opened the canonical post-detail URL and
previous-month query without like or content mutation. The original database,
media and port 8000 were not used.

Final gates:

- targeted contrast and mobile post-action contracts: pass;
- `manage.py check`: no issues;
- `makemigrations --check --dry-run`: no changes;
- full Django suite: 78/78 tests passed.
