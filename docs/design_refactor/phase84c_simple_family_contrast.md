# Phase 84c — simple-family contrast

## Scope

This phase corrects the Phase 84a P1 contrast findings for `simple_pattern`,
`simple_image` and `simple_retro`. It changes only foreground/accent colours on
existing opaque content and calendar surfaces. The photographic background,
desktop identity, responsive layout and interaction geometry are unchanged.

## Implementation

- Pattern and Image use `#3d6d86` for ordinary author, action, comment-author
  and post-bearing calendar links on their warm light surfaces.
- Their active calendar day keeps the established orange identity, darkened to
  `#a15e18` so white day text meets normal-text contrast.
- Retro uses `#2f6870`, a darker version of its existing teal, for the same
  links and active calendar surface. The change is scoped to the existing
  Retro columns and therefore does not affect other designs.

## Verification

An isolated migrated SQLite copy contained one synthetic blog, post and comment
for each design. Both blog and post-detail pages were rendered in Edge at 320,
390, 768 and 1440 px. Minimum measured foreground/background ratios were:

| Design | Author / action / comment author | Active calendar day |
| --- | ---: | ---: |
| `simple_pattern` | 5.58:1 | 5.09:1 |
| `simple_image` | 5.58:1 | 5.09:1 |
| `simple_retro` | 6.03:1 | 6.30:1 |

All relevant normal text therefore exceeds 4.5:1. Every page and viewport had
`scrollWidth == clientWidth`. Safe post-detail and previous-month navigation
clicks succeeded for all three designs; no mutating control was used.

Django verification: the focused contract tests, `manage.py check`, migration
drift check and complete test suite all pass.
