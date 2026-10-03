# Phase 84f4a — `planine_u_magli` audit

## Scope and fixture

`planine_u_magli` is a registered `Profile.TEMPLATE_CHOICES` key and maps to
`blog/templates/blog/designs/planine_u_magli.html`. This docs-only audit covers
the blog and post-detail routes at 320, 390, 768 and 1440 px (eight real-browser
states).

The migrated SQLite fixture was isolated from the original database. A fresh
author with empty `UserBlogPreference.data`, one published post and one reader
comment prevented old live-editor customizations from contaminating the design
defaults. No source data, media or mutating control was used.

Contrast was calculated from computed foregrounds and composited card
background colours. The desktop photograph was inspected separately because a
flat CSS background calculation cannot represent individual photograph pixels.

## Results

Minimum ratios across blog/detail and all four widths:

| Target | Minimum ratio | Result |
| --- | ---: | --- |
| post author | **4.28:1** | fail |
| post actions, including like | **4.28:1** | fail |
| comment text | **4.44:1** | narrow fail at 320/390 |
| comment author | **3.02:1** | fail |
| unauthenticated comment hint | 6.60:1 | pass |
| calendar navigation | **4.07:1** | fail |
| calendar post day | 6.49:1 | pass |
| archive link | **3.70:1** | fail |

At 768/1440, comment text rises to 5.40:1 and comment-author links to only
3.67:1. The failures therefore are not caused solely by the mobile stacking
layout.

The blog title and tagline have no protective surface and sit directly over
`planine_u_magli.jpg`. In the checked desktop image their slate ink is visually
readable over the pale sky, but its effective contrast remains dependent on the
chosen crop and photograph pixels. The 5.22:1 value against the fallback body
colour is not proof of contrast over the image and must not be treated as a
stable guarantee.

## Geometry and interaction

At 320 and 390 px, post actions, calendar navigation/days and archive links are
at least 44 px high. At 768 px, calendar navigation/days and archive links
remain at least 44 px, while the ordinary post action is 21 px and the like
button about 25 px. Desktop returns to compact controls as expected.

No visible non-Leaflet element crossed the viewport in any checked state.
`scrollWidth - clientWidth` was zero at 320, 390 and 1440 px, but reported
32 px at 768 px on both routes. A focused DOM scan found no visible escaping
element, so this is a reproducible numeric anomaly rather than a confirmed
visible overflow defect; pseudo-elements and the map wrapper are the likely
next probe points.

Safe navigation passed at 390 px: “Otvori post” reached the slugged detail URL
and previous month reached the expected calendar query. No like, save, comment,
publish or delete action was exercised.

## Priority

### P0

None. Both routes render, all content is reachable and safe navigation works.

### P1

1. Give post-author anchors and every post action a darker design-local slate;
   inherited Bootstrap blue is only 4.28:1 on the light post surface.
2. Darken comment-author links; 3.02:1 on the mobile comment surface is the
   largest deterministic contrast failure.
3. Darken archive links and calendar navigation on their light cards (3.70:1
   and 4.07:1).
4. Darken mobile comment ink slightly; 4.44:1 misses the normal-text threshold
   and has no safety margin.
5. Add a restrained, photograph-independent title/tagline treatment that keeps
   the mountain panorama dominant. The current crop looks readable but is not
   deterministic.

### P2

1. Extend post-action touch sizing through 768 px; action/like heights fall to
   about 21/25 px at tablet width.
2. Isolate the 32 px tablet `scrollWidth` discrepancy before changing layout;
   no visible element currently identifies a safe fix target.

## Map for the next small phases

1. **Phase 84f4b — deterministic card contrast:** one design-scoped ink patch
   for author/action, comment/comment-author, archive and calendar navigation,
   with a narrow render-contract test and the eight-state browser matrix.
2. **Phase 84f4c — hero protection:** a separate visual change for the
   title/tagline surface, reviewed against both bright sky and darker mountain
   zones so the desktop photographic character is preserved.
3. Keep tablet target sizing and the unexplained numeric overflow as separate
   P2 geometry work; neither belongs in the contrast patch.

`nebeski_mir` remains the final unaudited design from the Phase 84f group.
