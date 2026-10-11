# Phase100r — Podvodna first desktop comment: analytical photo bound

Application commit78064be, 2026-10-11. No application change. Read-only audit of blog and canonical detail for synthetic author2412/post14 at1440x900. Safe post-open navigation succeeded. Both routes have the same geometry, colors and layers; document overflow0.

## Current browser evidence

First author y813.96875, first text y839.302124. Body and photo width1424.666748 CSS px; photo height864, position0/0, image sized100% auto and positioned center -40px. Gradient uses the constant RGB(1,6,17) with alpha .52 at80%,1 at100%. No filter, transform or blend mode. Comment body is white at alpha .34. Author, actual word spans and their ancestors have opacity1; foreground RGB(213,229,255), no text shadow or filters. Raw observations are phase100r_photo_observations.json.

## Conservative calculation from the actual asset

The source is blog/static/blog/images/design-backgrounds/podvodna_tisina.png,1536x1024; SHA256 recorded in phase100r_photo_bounds.json. This uses the photograph, not the flat fallback.

Map each element's top to source row `(y+40)/(bodyWidth/1536)`. Include an extra16 source rows above and the ENTIRE image width and all remaining lower rows, deliberately including more than the text footprint. Both bands have per-channel maxima(61,62,67). Add another16 intensity levels per channel as a resampling allowance, giving(77,78,83). Use the weakest gradient opacity at the top of the element, then composite the white34% comment surface. The resulting upper background bounds are(94.331,97.264,103.974) for author and(90.801,93.920,100.908) for body. Relative luminance yields modeled lower contrast bounds:

| Route | Author | Body |
| --- | --- | --- |
| blog |4.8489:1|5.1047:1|
| detail |4.8489:1|5.1047:1|

Below864px the photo disappears into the same darker solid body, which does not weaken this bound. Foreground is opaque and lighter than every bounded background channel.

## Interpretation and limitations

These are analytical bounds for the observed asset, geometry and standard alpha-compositing model, with explicit16-row/16-level margins. They are NOT direct rendered-pixel measurements or a proof of every browser resampling implementation. They support leaving author/body styling unchanged in this fixture rather than introducing an unconfirmed visual fix. Final rendered-pixel validation remains open until a trustworthy capture coordinate system is available. The rejected Phase100p screenshot mapping is not reused.

This result cannot be transferred to shorter posts, other widths, different photos, custom colors or another theme. Other header/calendar/post photo zones still need their own evidence. Coverage13/37 remains incomplete, and no whole-design pass is claimed.

## Cleanup and validation

No template or DB changes; no duplicate application tests. Phase100q's check/migration/214 passing tests remains the latest application validation. QA server8017 stopped, browser closed, viewport reset. Original repo/DB/media/port8000/main/deployment untouched. Numerical source and browser observations are retained with this audit.
