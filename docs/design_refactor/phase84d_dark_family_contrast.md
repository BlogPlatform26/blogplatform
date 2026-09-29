# Phase 84d — dark-family contrast

## Scope

This phase corrects the Phase 84a P1 contrast findings shared by `dark` and
`dark_right`: the desktop comment-author link and active calendar day. It does
not change layout, spacing, responsive ordering or the dark visual identity.

## Implementation

- At 768 px and wider, the comment-author link uses pale blue `#d9ecff` on the
  existing translucent comment surface. The already compliant mobile colour is
  left unchanged.
- The active calendar day keeps its red accent, darkened from `#ff3b3b` to
  `#c92f2f` so white day text meets normal-text contrast at every viewport.

## Verification

An isolated migrated SQLite copy contained one synthetic blog, post and comment
for each variant. Both blog and post-detail pages were rendered in Edge at 320,
390, 768 and 1440 px. Before the change, the desktop comment-author minimum was
2.33:1 and the active day was 3.53:1. After the change:

- comment-author contrast is 7.26:1 at 320/390 and 5.06:1 at 768/1440;
- active-day contrast is 5.34:1 at every tested width;
- the same values hold for `dark` and `dark_right`, on blog and detail pages;
- every state has `scrollWidth == clientWidth`.

Safe post-detail and previous-month navigation clicks succeeded for both
variants; no mutating control was used. The focused tests, `manage.py check`,
migration drift check and complete Django suite all pass.
