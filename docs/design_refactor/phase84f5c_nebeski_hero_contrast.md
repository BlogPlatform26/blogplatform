# Phase 84f5c — `nebeski_mir` hero contrast fix

## Scope

This phase fixes only the photograph-dependent contrast of the blog title and
tagline identified in Phase 84f5a. The change is local to `nebeski_mir`; it
does not change shared CSS, the sky/dove image, card styling or another design.

An isolated migrated SQLite database used a fresh author with empty design
preferences, one published post and one reader comment. Real-browser checks
covered blog and post-detail at 320, 390, 768 and 1440 px.

## Implementation

The existing header receives a restrained opaque mist surface (`#f1f5fb`), a
soft blue border and shadow. Title ink is `#2f435c`; tagline ink is `#334155`.
Text shadows are removed because contrast now comes from a deterministic solid
surface rather than the variable photograph crop.

The surface remains inside the established header geometry at every tested
breakpoint. Desktop visual inspection confirmed that the dove, sky, glass-card
language and overall composition remain recognizable and intact.

## Measured results

| Target | Before, actual photo pixels | After, solid surface |
| --- | ---: | ---: |
| blog title | 2.66–2.79:1 | 9.24:1 |
| tagline | 2.61–2.97:1 | 9.46:1 |

The after values were identical in all eight blog/detail and breakpoint states
and exceed the 4.5:1 target. Phase 84f5b ink remained intact: author contrast
uses `#315f8d`, while comment text remains `#39445b` at 320/390 and `#334155`
at 768/1440.

No visible non-Leaflet element crossed the viewport. Numeric
`scrollWidth - clientWidth` was zero at 320, 390 and 1440 px; the isolated
fixture retained a 20 px difference at 768 px without a visible escaping
element. That known P2 tablet geometry issue remains outside this colour fix.
Safe 390 px navigation passed for “Otvori post” and previous month; no mutating
action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, the deterministic
surface and ink, plus isolation from `planine_u_magli`. Django system checks,
migration drift and the complete test suite are the final gate.

## Remaining work

- P2: shared post-action touch sizing at 768 px and the tracked numeric tablet
  width anomaly.
