# Phase 86b — `zlatni_horizont` card/action contrast fix

## Scope

This phase fixes only the three deterministic action/guidance failures from
Phase 86a: Bootstrap like blue, anonymous guidance and calendar navigation.
All rules are local to `zlatni_horizont`. The photograph, header, post surface,
layout geometry and touch sizing are unchanged.

An isolated migrated SQLite fixture with empty design preferences, one post
and one reader comment was checked on public blog and post-detail at 320, 390,
768 and 1440 px.

## Implementation

- Like now uses the existing gold action ink `#ffd5ac` instead of Bootstrap
  blue.
- Anonymous comment guidance uses the same gold ink instead of inherited dark
  `text-muted`.
- Calendar arrows use `#ffe4c7` on a compact translucent deep-brown surface
  (`rgba(34, 14, 4, .78)`). Hover/focus states brighten without changing size.

No shared CSS or other design changed.

## Measured results

| Target | Before | After |
| --- | ---: | ---: |
| like button | 2.79:1 | **at least 6.36:1** |
| anonymous comment hint | 1.23:1 | **15.37:1** |
| calendar navigation | 2.78:1 | **at least 7.69:1** |

The like now reuses the action ink whose actual photo-zone minimum in the audit
was 6.36:1. The anonymous hint is positioned over the black lower page. For
calendar navigation, 7.69:1 is the conservative worst case calculated with the
declared surface composited over pure white; every sampled photograph pixel is
darker and therefore has additional margin.

The browser confirmed the intended computed colours and navigation surface in
all eight states. Phase86a's transparent header and post-title/body failures
remain unchanged and are not claimed as fixed here.

## Geometry and interaction

Document overflow remains zero at all four widths, with no visibly escaping
non-Leaflet element. The existing 768 px local calendar overflow remains 169 px
inside a 117 px grid, and post-action target heights remain approximately
21/25 px. Those P2 items are outside this colour phase.

Desktop visual inspection confirmed that the orange sunset, water reflection,
transparent cards and compact three-column layout retain their identity. Safe
390 px navigation passed for “Otvori post” and previous month; no mutating
action was exercised.

## Automated verification

A narrow render-contract test covers blog/detail output, all three selectors,
the stable calendar surface and isolation from `iznad_oblaka`. Django system
checks, migration drift and the complete test suite are the final gate.

## Remaining work

- P1: photograph-independent title/tagline protection.
- P1: stable post-title and post-body treatment across the bright horizon and
  sun reflection.
- P2: tablet calendar local overflow and shared post-action touch sizing.
