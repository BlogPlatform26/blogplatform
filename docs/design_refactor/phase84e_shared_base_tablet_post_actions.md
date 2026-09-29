# Phase 84e — shared-base tablet post actions

## Scope

This phase extends the existing 44 px mobile post-action target contract through
the tablet layout for the nine shared-base designs audited in Phase 84a:
`default`, `dark`, `classic`, their right-column variants, `simple_pattern`,
`simple_image` and `simple_retro`.

## Implementation

A design-gated rule applies only from 576 through 991.98 px. Direct post-action
links and the like form button use the same flex centring and 44 px minimum
height as the established mobile contract. The rule does not render for bespoke
designs and does not apply at 1440 px, so their geometry and desktop density are
unchanged.

## Verification

An isolated migrated SQLite copy contained a synthetic blog and post for every
shared-base key. Edge rendered blog and post-detail at 320, 390, 768 and 1440
px (72 states). Before the change, visible direct post-action links measured 44
px at 320/390 and 21 px at 768/1440 in the current branch. After the change:

- all nine designs retain 44 px links at 320/390;
- links and the like button measure at least 44 px at 768;
- 1440 remains unchanged: 21 px links and 25.3 px like buttons;
- every page and viewport has `scrollWidth == clientWidth`.

Each design's non-mutating “Otvori post” link was clicked at 768 px and reached
the canonical post-detail route. A real `nebesko_polje` comparison did not
render the Phase 84e rule, remained at its existing 21 px tablet link height and
had no overflow, confirming that bespoke designs are outside this phase.

The focused tests, `manage.py check`, migration drift check and complete Django
suite all pass.
