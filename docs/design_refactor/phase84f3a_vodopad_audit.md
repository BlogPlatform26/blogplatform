# Phase 84f3a — `vodopad_u_magli` audit

## Scope and method

Because the weekly execution allowance had only 8% remaining, this is the
smallest complete slice permitted by the Phase 84f3 brief: one design rather
than an incomplete three-design audit. It covers `vodopad_u_magli` on the blog
and post-detail routes at 320, 390, 768 and 1440 px (eight real-browser states).
`planine_u_magli` and `nebeski_mir` remain explicitly open.

The fixture lived in an isolated, migrated SQLite copy and contained one
author, one published post and one reader comment. The original database and
media were not touched. Contrast was calculated from computed foregrounds and
composited rendered background colours. A desktop screenshot was inspected to
identify content that sits directly on the photographic backdrop rather than
on the design's opaque/translucent cards.

## Results

The minimum measured ratios across both routes and all widths were:

| Target | Minimum ratio | Surface dependence |
| --- | ---: | --- |
| post author | **4.09:1** | defined light post surface |
| post action link | **4.09:1** | defined light post surface |
| comment text | **4.46:1** | defined comment surface |
| comment author | 4.90:1 | defined comment surface |
| unauthenticated comment hint | 6.43:1 | defined light post surface |
| calendar navigation | 4.93:1 | defined calendar surface |
| calendar post day | 9.52:1 | defined calendar surface |
| archive link | 6.00:1 | defined archive surface |

The desktop blog title and tagline are different: dark green text is rendered
without a protective surface directly over `vodopad_u_magli.png`. In the
checked 1440 px render it crosses both bright waterfall mist and darker forest,
so its effective contrast is photograph-pixel-dependent and is visibly weak in
parts. A single flat computed-background ratio would be misleading here.

At 320 and 390 px, post-action links, calendar navigation/days and archive rows
are at least 44 px high. At 768 px, calendar and archive controls remain at
least 44 px, while the post action is 21 px high. Desktop controls intentionally
return to compact dimensions (post action 21 px, calendar navigation 30 px,
post day about 35 px and archive row about 33 px).

No visible content component escaped its container. Leaflet tiles extend past
their internal map viewport as expected but remain clipped by the map. At
768 px the document reported a small 4 px `scrollWidth - clientWidth`
difference even though no visible non-Leaflet element crossed the viewport;
record this as a low-priority numeric anomaly for a focused follow-up rather
than a confirmed user-visible overflow defect.

Safe navigation passed at 390 px: “Otvori post” reached the slugged detail URL,
and the previous-month control reached the expected calendar query. No like,
save, publish, comment-submit or delete action was exercised.

## Priority

### P0

None. Both routes rendered, content remained reachable and safe navigation
worked at every checked breakpoint.

### P1

1. Protect the desktop blog title/tagline from the photographic background
   with a localized readable surface, text shadow or other deterministic
   treatment; current contrast depends on the underlying photo pixels.
2. Replace the inherited Bootstrap blue for post-author and post-action links
   on this design's light post surface; 4.09:1 misses the 4.5:1 normal-text
   threshold.
3. Darken the comment ink slightly; the measured 4.46:1 is narrowly below the
   4.5:1 threshold and has no safety margin.

### P2

1. Extend shared post-action touch sizing through the 768 px breakpoint; the
   action link falls from 44 px on phones to 21 px on tablet.
2. Recheck the reproducible 4 px tablet `scrollWidth` discrepancy with a
   focused pseudo-element/map containment probe before changing layout CSS.

## Smallest next fix

Start with a design-scoped darker link colour for the post author and post
actions, backed by a narrow render-contract test. It is deterministic, affects
only two known selectors on an already-defined surface and does not alter the
photographic composition. Handle the hero title/tagline protection separately
because it requires visual judgment across the full image.

## Remaining Phase 84f work

Complete the same eight-state audit independently for `planine_u_magli`, then
for `nebeski_mir`. This phase intentionally did not begin either audit, so no
partial measurements need to be reconciled later.
