# Phase 85d — `svemirski_horizont` tablet calendar geometry

## Scope and root cause

This phase fixes only the confirmed 768 px calendar-grid overflow from Phase
85a/c. The isolated before state had 169 px of grid content inside a 117 px
client width and a 2 px document-width difference.

Browser inspection identified the real cause: Bootstrap's three-column tablet
layout left the calendar in a 172 px column, while the current linked day
correctly retained the shared 44 px touch minimum. CSS Grid expanded that one
track from about 15 px to 44 px, forcing the full grid past its container. This
was not a generic scrollbar problem, so no `overflow: hidden` workaround was
used and the touch target was not reduced.

## Implementation

Only between 768 and 991.98 px, `svemirski_horizont` now places the main post
column on a full row and the two sidebars on the following half-width row. The
calendar uses the real width of its left tablet column, 8 px internal padding
and a 1 px grid gap. The selected-day scale transform is removed at this
breakpoint while retaining its one-pixel vertical emphasis.

Mobile below 768 px and desktop from 992 px retain their existing layouts and
calendar spacing. No shared CSS or other design changed.

## Browser measurements

Public blog and post-detail were checked at 320, 390, 768 and 1440 px using an
isolated migrated SQLite fixture.

| Measurement at 768 px | Before | After |
| --- | ---: | ---: |
| calendar grid scroll/client width | 169 / 117 px | **317 / 317 px** |
| calendar box scroll/client width | 185 / 149 px | **333 / 333 px** |
| document scroll/client width | 755 / 753 px | **753 / 753 px** |
| linked calendar target | about 46×46 px with scale | **44×44 px** |

Document-width differences remain zero at 320, 390 and 1440 px. No visible
non-Leaflet element escaped at any width. The mobile and desktop calendar
geometry is unchanged.

The Phase85b/85c contract remained active in every state: title ink/surface is
`rgb(239, 246, 255)` on `rgb(8, 19, 38)`, like and anonymous guidance use
`rgb(201, 219, 255)`, and calendar navigation keeps its pale ink on the stable
deep-space surface.

Visual inspection confirmed that the 768 px post remains dominant, with the
calendar and profile grouped below it, while the star-field/Earth composition
and transparent cards are preserved. Safe 390 px navigation passed for “Otvori
post” and previous month; no mutating action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, the tablet-only media
query, full-width content row, widened calendar and compact grid, plus isolation
from `zlatni_horizont`. Django system checks, migration drift and the complete
test suite are the final gate.

## Remaining work

- P2: shared tablet post-action targets remain approximately 21/25 px and are
  intentionally outside this calendar phase.
