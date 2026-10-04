# Phase 86a — `zlatni_horizont` audit

## Scope and fixture

`zlatni_horizont` is a registered design backed by
`blog/templates/blog/designs/zlatni_horizont.html`. This docs-only audit covers
public blog and post-detail at 320, 390, 768 and 1440 px (eight real-browser
states).

The migrated SQLite fixture was isolated from the original database and used a
fresh author with empty `UserBlogPreference.data`, one published post and one
reader comment. No project data, media or mutating control was used.

Computed colours were recorded in the browser. Because the header, post,
calendar and archive surfaces are transparent, effective contrast was also
sampled at nine points per real target rectangle from
`zlatni_horizont.jpg`, applying its responsive crop, declared warm-to-black
gradient and each translucent child surface. Computed transparent backgrounds
alone are not treated as proof of contrast.

## Effective contrast

Minimum photo/composited ratios across the eight states:

| Target | Minimum | Result |
| --- | ---: | --- |
| blog title | **2.06:1** | fail; also 2.51 at 320 and 3.42 at 768 |
| tagline | **1.45:1** | fail on mobile; 2.26 at 768 and 4.02 at 1440 |
| post title | **1.90:1** | fail at 768; 2.79 at 1440 |
| post body text | **1.46:1** | fail at 768; 2.58 at 1440 |
| post author / pale actions | 6.36:1 | pass |
| Bootstrap-blue like button | **2.79:1** | fail; 3.52 at 768 |
| comment text | 4.97:1 | pass |
| comment author | 5.02:1 | pass |
| anonymous comment hint | **1.23:1** | fail |
| calendar navigation | **2.78:1** | fail at every breakpoint |
| calendar post day | 5.09:1 | pass |
| archive link | 13.94:1 | pass |

The title and tagline cross bright sky/sun zones on narrow crops. At wider
sizes the post title and body sit directly over the bright reflection and warm
horizon, so their pale computed colours fail despite looking suitable against
the black body fallback. The desktop screenshot visibly confirms low post-card
contrast around the sun reflection.

The like control inherits Bootstrap `rgb(13, 110, 253)` instead of the local
gold action ink. Anonymous guidance inherits dark
`rgba(33, 37, 41, .75)` over the black lower page. Calendar arrows combine
warm text with a translucent white surface over the photograph and do not reach
4.5:1 in any tested layout.

## Geometry and touch targets

Document overflow was zero in all eight states and no visible non-Leaflet
element escaped the viewport. At 768 px, however, the calendar retains a local
geometry defect: 169 px grid content inside a 117 px client width, and 185 px
calendar content inside a 149 px client width. The overflow does not currently
increase document width, but it is the same structural 25%-sidebar/touch-target
collision identified in the preceding scenic design.

At 320/390 px, like/comment/open-post controls, calendar navigation and archive
links are at least 44 px high. At 768 px calendar and archive targets remain at
least 44 px, while ordinary post actions are about 21 px and the like button
about 25 px. Desktop controls retain compact sizing.

Safe navigation at 390 px passed: “Otvori post” reached the slugged detail URL
and previous month reached the expected query. No like, comment, publish, save
or delete action was exercised.

Visual inspection confirmed the established orange sunset, reflection,
transparent cards and desktop three-column composition. This audit makes no
visual or code change.

## Priority

### P0

None. Both public routes render and navigation remains usable.

### P1

1. Add restrained photo-independent protection for the header title/tagline;
   sampled minima are 2.06:1 and 1.45:1.
2. Stabilize the transparent post surface or its ink across the bright horizon
   and reflection; post-title/body minima are 1.90:1 and 1.46:1.
3. Replace Bootstrap blue on the like button and dark anonymous guidance with
   local readable ink; minima are 2.79:1 and 1.23:1.
4. Give calendar navigation a stable dark gold-compatible surface/ink; current
   minimum is 2.78:1.

### P2

1. Resolve the 768 px calendar local overflow without shrinking 44 px linked
   day targets or hiding the excess.
2. Extend shared scenic post-action touch sizing through 768 px.

## Suggested remediation order

1. A local card/action contrast patch for like, anonymous guidance and calendar
   navigation.
2. A separate post-surface treatment reviewed against the actual sunset and
   reflection.
3. A separate compact header treatment so the sunset identity can be reviewed
   independently.
4. Tablet calendar geometry, keeping shared post-action sizing as its own P2.

The remaining registered designs have not implicitly passed this audit and
must be measured independently.
