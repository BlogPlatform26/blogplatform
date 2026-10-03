# Phase 84f3b — `vodopad_u_magli` contrast fix

## Scope

This phase resolves the three deterministic contrast failures recorded in
Phase 84f3a and the photograph-dependent desktop blog heading. The change is
local to `vodopad_u_magli`; it does not alter the source photograph, shared
layouts or other designs.

An isolated migrated SQLite copy contained one author, one published post and
one reader comment. Real-browser checks covered blog and post-detail at 320,
390, 768 and 1440 px. The original database and media were not touched.

## Implementation

- Post-author links and all post actions (including the like button) use the
  darker design green `#43513e` on the existing light card surfaces.
- Comment text uses `#465042` on the existing comment card.
- At desktop widths (992 px and above), the existing central header column
  receives an opaque mist-coloured `#eef0e9` surface, a restrained border,
  radius and shadow. This makes title/tagline contrast independent of both the
  bright waterfall and dark forest pixels while leaving the photograph visible
  around the compact title card.

## Browser evidence

Minimum contrast before/after across the eight checked states:

| Target | Before | After |
| --- | ---: | ---: |
| post author | 4.09:1 | 7.68:1 |
| post actions | 4.09:1 | 7.68:1 |
| comment text | 4.46:1 | 6.43:1 |
| desktop title/tagline | photo-dependent | 7.32:1 |

At 768 and 1440 px, comment contrast rises to 7.94:1. Mobile title/tagline
remain 7.44:1 on the existing non-photographic mobile presentation. All author
and action controls resolve to the same darker green, including “Sviđa mi se”,
“Komentari” and “Otvori post”.

No visible non-Leaflet element crossed the viewport in any state. The already
documented 4 px `scrollWidth - clientWidth` discrepancy at 768 px remains,
without a visible escaping element; this fix neither causes nor enlarges it.
At 320, 390 and 1440 px the difference is zero.

Safe navigation at 390 px passed: “Otvori post” reached the slugged detail URL
and previous month reached the expected calendar query. No mutating UI control
was exercised. Desktop visual inspection confirmed that the photograph remains
the dominant composition around the compact header card.

## Automated verification

A focused render-contract test covers blog/detail output, the author child
anchor, like-button/action selector, comment ink, desktop surface and
cross-design isolation. Django system checks, migration drift and the complete
test suite are run as the final gate.

## Remaining work

The Phase 84f audits for `planine_u_magli` and `nebeski_mir` remain open. The
tablet 4 px numeric discrepancy and 768 px post-action touch height remain the
separate P2 items from Phase 84f3a.
