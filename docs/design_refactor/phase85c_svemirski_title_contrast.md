# Phase 85c — `svemirski_horizont` title contrast

## Scope

This phase fixes only the photograph-dependent blog-title failure from Phase
85a. The tagline already passed and remains transparent. Phase 85b card/action
inks, the star-field/Earth image, transparent cards, layout geometry and touch
sizing are unchanged.

An isolated migrated SQLite database used the same synthetic fixture as the
audit. Real-browser checks covered public blog and post-detail routes at 320,
390, 768 and 1440 px (eight states).

## Implementation

The title link receives a compact deep-space surface (`#081326`) directly
behind each rendered line. `box-decoration-break: clone` makes the treatment
safe when the title wraps at 320 px. A small matching outer edge and restrained
shadow blend it into the star field without covering the tagline or Earth
horizon. The title's existing pale ink remains unchanged.

## Measured results

| Target | Before, actual photo pixels | After, deterministic surface |
| --- | ---: | ---: |
| blog title | 1.51:1 minimum at 390; 3.73:1 at 320 | **17.05:1** |

The browser computed `rgb(239, 246, 255)` on `rgb(8, 19, 38)` in every blog
and detail state. The same 17.05:1 result therefore holds independently of the
underlying crop. Title rectangles and wrapping remain unchanged. The tagline
continues to use its transparent surface and unchanged ink.

Phase 85b remained active in all eight states: like and anonymous guidance use
`rgb(201, 219, 255)`, while calendar navigation uses `rgb(241, 246, 255)` on
`rgba(4, 12, 28, .72)`.

## Geometry and interaction

No visibly escaping non-Leaflet element appeared. Document-width differences
remain 0 px at 320/390/1440 and the known 2 px at 768. The existing tablet
calendar grid remains 169 px inside a 117 px client width; neither that P2 issue
nor post-action sizing changed.

Desktop and mobile visual inspection confirmed that the star field, Earth
horizon, transparent cards and overall composition remain recognizable. Safe
390 px navigation passed for “Otvori post” and previous month; no mutating
action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, the title-only
surface, wrapped-line contract and isolation from `zlatni_horizont`. Django
system checks, migration drift and the complete test suite are the final gate.

## Remaining work

- P2: 768 px calendar-grid overflow and shared post-action touch sizing.
