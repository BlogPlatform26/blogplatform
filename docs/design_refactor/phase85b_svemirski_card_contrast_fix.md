# Phase 85b — `svemirski_horizont` card/action contrast fix

## Scope

This phase fixes only the three deterministic card/action failures from Phase
85a: anonymous guidance, the like button and calendar navigation. All rules are
local to `svemirski_horizont`. The photograph, transparent title/tagline,
layout geometry and touch sizing are unchanged; hero protection remains Phase
85c.

An isolated migrated SQLite database used the same synthetic fixture shape as
the audit: a fresh author with empty design preferences, one published post and
one reader comment. Real-browser checks covered blog and post-detail at 320,
390, 768 and 1440 px.

## Implementation

- The like button now uses the existing space-theme action ink `#c9dbff`
  instead of inherited Bootstrap blue.
- Anonymous guidance inside the comments region uses the same pale ink instead
  of inherited dark `text-muted`.
- Calendar navigation uses `#f1f6ff` on a compact translucent deep-space
  surface. The circular controls and desktop sizing are preserved.

Hover/focus states brighten to white. No shared CSS or other design changed.

## Measured results

Actual photo/composited-background minima across the eight states:

| Target | Before | After |
| --- | ---: | ---: |
| like button | 4.35:1 | **14.22:1** |
| anonymous comment hint | 1.23:1 | **15.06:1** |
| calendar navigation | 4.25:1 | **16.13:1** |

The browser confirmed the intended computed colours and navigation surface in
every state. The transparent title remains `rgb(239, 246, 255)` with unchanged
geometry, deliberately leaving its photograph-dependent 1.51:1 minimum for
Phase 85c.

## Geometry and interaction

No visibly escaping non-Leaflet element appeared. With the same audit fixture,
document-width differences remain 0 px at 320/390/1440 and the existing 2 px
at 768. The known tablet calendar grid remains 169 px inside a 117 px client
width; this patch does not claim to resolve that P2 issue. Post-action target
heights are likewise unchanged.

Desktop visual inspection confirmed that the star field, Earth horizon,
transparent cards and compact circular calendar controls retain their design
character. Safe navigation at 390 px passed for “Otvori post” and previous
month; no mutating action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, all three selectors,
the stable calendar surface and isolation from `zlatni_horizont`. Django system
checks, migration drift and the complete test suite are the final gate.

## Remaining work

- Phase 85c: crop-independent title protection, measured against real photo
  pixels while preserving the space/Earth composition.
- P2: 768 px calendar-grid overflow and shared post-action touch sizing.
