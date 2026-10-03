# Phase 84f5a — `nebeski_mir` audit

## Scope and fixture

`nebeski_mir` is a registered `Profile.TEMPLATE_CHOICES` key and maps to
`blog/templates/blog/designs/nebeski_mir.html`. This docs-only audit covers the
public blog and post-detail routes at 320, 390, 768 and 1440 px (eight
real-browser states).

The migrated SQLite fixture was isolated from the original database. A fresh
author with empty `UserBlogPreference.data`, one published post and one reader
comment prevented live-editor state from contaminating design defaults. No
source data, media or mutating control was used.

Card contrast was calculated from computed foregrounds and composited rendered
background colours. Hero contrast was measured separately from pixels in the
actual `nebeski_mir.jpg` crop with the design's CSS gradient applied; the flat
computed fallback is reported only to show why it is insufficient.

## Contrast results

Minimum card-surface ratios across blog/detail and all widths:

| Target | Minimum ratio | Result |
| --- | ---: | --- |
| post author | **4.45:1** | narrow fail |
| post actions, including like | **4.45:1** | narrow fail |
| comment text | **4.37:1** | fail at 768/1440 |
| comment author | 10.85:1 | pass |
| anonymous comment hint | 6.74:1 | pass |
| calendar navigation | **2.93:1** | fail |
| calendar post day | 14.14:1 | pass |
| archive link | 14.55:1 | pass |

Comment text is 9.42:1 at 320/390 but falls to 4.37:1 when the wider-layout
cascade changes its ink. Author/action Bootstrap blue remains 4.45:1 at every
width, just below the normal-text threshold.

### Hero: computed versus photograph pixels

The browser reports title/tagline ink `rgb(129, 135, 154)` and a 3.39:1 ratio
against the fallback `#f6f9ff`. That value does **not** describe text over the
photograph because the header surface is transparent.

For the 1440 px render, nine points were sampled inside each text rectangle
from the actual 1536×1024 background image, using the CSS `cover` crop and the
declared vertical gradient:

- title: **2.66–2.79:1**;
- tagline: **2.61–2.97:1**.

The screenshot agrees with the measurements: grey text is visibly faint over
the bright pastel sky. Mobile and tablet retain the same transparent header;
their flat 3.39:1 fallback value already fails, while their precise result also
depends on each photographic crop. This is a confirmed P1, not a stable
computed-colour pass.

## Geometry and interaction

No document or visible local-component overflow was found at any checked width;
`scrollWidth - clientWidth` was zero in all eight states. Leaflet internals were
excluded from local overflow reporting because their tiles are intentionally
clipped by the map viewport.

At 320 and 390 px, post actions, calendar navigation/days and archive links are
at least 44 px high. At 768 px, calendar and archive controls remain at least
44 px, while ordinary post actions are 21 px and the like button about 25 px.
Desktop controls return to compact dimensions.

Safe navigation passed at 390 px: “Otvori post” reached the slugged detail URL
and previous month reached the expected query. No like, save, comment, publish
or delete action was exercised. The desktop photographic composition remains
unchanged by this audit.

## Priority

### P0

None. Both public routes render, content remains reachable and safe navigation
works.

### P1

1. Add a restrained, photograph-independent title/tagline treatment. Actual
   desktop photo samples are only 2.61–2.97:1.
2. Give calendar navigation a darker design-local ink; current contrast is
   2.93:1 on its pale card.
3. Replace inherited Bootstrap blue for the real post-author anchor and all
   post actions; 4.45:1 narrowly misses the threshold.
4. Stabilize comment ink across layouts; the wider cascade falls to 4.37:1.

### P2

1. Extend post-action touch sizing through 768 px; action/like heights fall to
   approximately 21/25 px.

## Map for subsequent phases

1. **Phase 84f5b — deterministic card contrast:** locally fix calendar
   navigation, author/actions and comment ink, with a narrow render contract and
   the eight-state browser matrix.
2. **Phase 84f5c — hero protection:** separately introduce a compact stable
   title/tagline surface or equivalent treatment and verify actual photo-zone
   contrast while preserving the dove/sky composition.
3. Keep the shared 768 px action-target concern as separate P2 geometry work,
   alongside the already open Planine/Vodopad tablet items.
