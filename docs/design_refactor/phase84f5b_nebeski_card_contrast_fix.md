# Phase 84f5b — `nebeski_mir` card contrast fix

## Scope

This phase fixes only the deterministic pale-card contrast failures from Phase
84f5a. All rules are local to `nebeski_mir`. The photograph, title/tagline,
layout geometry and touch sizing are unchanged; hero protection remains Phase
84f5c.

An isolated migrated SQLite database used a fresh author with empty design
preferences, one published post and one reader comment. Real-browser checks
covered blog and post-detail at 320, 390, 768 and 1440 px.

## Implementation

- `#315f8d` is the darker sky-blue ink for the real post-author anchor, like
  button, every post action and calendar navigation.
- `#334155` stabilizes comment text across narrow and wide layout cascades.
- Interactive hover ink is `#254766`.

No shared CSS, card geometry or hero rule was changed.

## Measured results

Minimum contrast across the eight states:

| Target | Before | After |
| --- | ---: | ---: |
| post author | 4.45:1 | 6.59:1 |
| post actions / like | 4.45:1 | 6.59:1 |
| calendar navigation | 2.93:1 | 6.61:1 |
| comment text | 4.37:1 | 9.42:1 |

At 768/1440, comment contrast is 10.28:1. No visible non-Leaflet element
crossed the viewport. The isolated fixture reported a 3 px numeric
`scrollWidth - clientWidth` difference at 768 px without a visible escaping
element; all other widths were zero. The known tablet geometry investigation
remains separate from this colour fix.

The title retained its original computed colour at every breakpoint, proving
that Phase 84f5c's hero scope was not pulled into this change. Desktop visual
inspection confirmed that the dove, sky, glass cards and overall layout remain
unchanged. Safe navigation at 390 px passed for “Otvori post” and previous
month; no mutating action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, the real child author
anchor, like/action selector, calendar navigation, comment ink and isolation
from `planine_u_magli`. Django system checks, migration drift and the complete
test suite are the final gate.

## Remaining work

- Phase 84f5c: photograph-independent title/tagline protection; actual photo
  samples remain 2.61–2.97:1.
- P2: shared post-action touch sizing at 768 px and the small numeric-width
  anomalies already tracked across this design group.
