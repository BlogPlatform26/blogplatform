# Phase 85a — `svemirski_horizont` audit

## Scope and fixture

`svemirski_horizont` is a registered `Profile.TEMPLATE_CHOICES` key and maps to
`blog/templates/blog/designs/svemirski_horizont.html`. This docs-only audit
covers the public blog and post-detail routes at 320, 390, 768 and 1440 px
(eight real-browser states).

The migrated SQLite fixture was isolated from the original database. A fresh
author with empty `UserBlogPreference.data`, one published post and one reader
comment prevented live-editor state from affecting the defaults. No source
data, media or mutating control was used.

Computed colours and alpha surfaces were checked in the browser. Because the
design deliberately places transparent content over
`svemirski_horizont.png`, contrast was measured again from nine points in each
real target rectangle, using the CSS `cover`/width crop, the declared black
gradient and the relevant translucent overlay. A flat computed background
alone is not an adequate result for this design.

## Contrast results

Minimum actual rendered-background ratios across the eight states:

| Target | Minimum ratio | Result |
| --- | ---: | --- |
| blog title | **1.51:1** | fail on the bright 390 px horizon crop |
| tagline | 12.72:1 | pass |
| post author | 12.86:1 | pass |
| post actions except like | 13.42:1 | pass |
| Bootstrap-blue like button | **4.35:1** | fail at 1440; 4.45 at 768 |
| comment text | 5.66:1 | pass |
| comment author | 5.18:1 | pass |
| anonymous comment hint | **1.23:1** | fail |
| calendar navigation | **4.25:1** | fail at 1440 |
| calendar post day | 4.78:1 | pass |
| archive link | 13.42:1 | pass |

The title uses computed `rgb(239, 246, 255)` on a transparent header. Actual
photo-zone sampling ranges from **1.51–12.58:1** at 390 px and
**3.73–18.08:1** at 320 px; at 768 and 1440 px the sampled ranges pass. The
desktop screenshot therefore cannot prove the responsive crop safe. The
tagline uses the same transparent treatment but remained above 12.72:1 in the
tested crops.

The like control is the exception to the design-local pale action ink: it
retains Bootstrap `rgb(13, 110, 253)`. The anonymous hint retains Bootstrap
`rgba(33, 37, 41, .75)` on the transparent post card and becomes nearly
invisible over black. The comment surface actually computes to translucent
white `rgba(255, 255, 255, .34)` through a later shared rule; its light comment
inks still pass, but only at 5.18–5.66:1.

## Geometry, touch and interaction

No visibly escaping non-Leaflet element was found at any checked width.
Document overflow was zero at 320, 390 and 1440 px. At 768 px it was 2 px;
the calendar grid also reported 168 px content width inside a 117 px client
width. Its excess is clipped within the 150 px sidebar, but this is a genuine
local tablet geometry defect rather than a colour issue.

At 320/390 px, like/comment/open-post controls, calendar navigation and archive
links are at least 44 px high. At 768 px calendar/archive targets remain at
least 44 px, while ordinary post actions are about 21 px and the like button
about 25 px. Desktop calendar navigation is 30 px and archive links about
34 px, consistent with the compact desktop layout. The known shared 768 px
post-action target problem therefore applies here too.

Safe 390 px navigation passed: “Otvori post” reached the slugged detail URL and
previous month reached the expected query. No like, comment, publish, save or
delete action was exercised. Visual inspection confirmed the star field,
Earth horizon and established desktop composition remain unchanged.

## Priority

### P0

None. Both public routes render, content remains reachable and safe navigation
works.

### P1

1. Add a restrained, crop-independent title treatment while preserving the
   unobstructed space/Earth composition; the worst actual photo sample is
   1.51:1.
2. Override the anonymous hint with a design-local pale ink; current contrast
   is 1.23:1.
3. Replace inherited Bootstrap blue on the like button with the existing pale
   action system; it reaches only 4.35:1.
4. Stabilize desktop calendar-navigation contrast; the worst actual photo
   sample is 4.25:1.

### P2

1. Resolve the 768 px calendar grid overflow (168 px inside 117 px) and the
   resulting 2 px document-width discrepancy.
2. Extend shared post-action touch sizing through 768 px.

## Suggested remediation order

1. One narrow design-local card/action patch for the anonymous hint, like
   button and calendar navigation, followed by the eight-state contrast check.
2. A separate compact hero treatment verified against actual image pixels at
   all four widths so the visual identity can be reviewed independently.
3. Keep tablet calendar/action geometry as a separate P2 phase shared with the
   already tracked scenic-design sizing work.
