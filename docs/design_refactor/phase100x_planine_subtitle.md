# Phase100x — Planine desktop subtitle

The 100s candidate is confirmed: the actual subtitle is a plain paragraph, no child override, 17.568px weight400, foreground rgb(67,86,108), opacity0.82 over an opaque rgb(237,241,244) heading card at1440. Effective contrast is4.34723:1. The existing desktop-only theme rule now sets subtitle opacity1, producing6.63577:1 without changing color, card or geometry. Below992 and Vodopad remain unchanged.

[Raw evidence](phase100x_subtitle_measurements.json) contains16 before/after states (both themes, blog/detail320/390/768/1440), Bootstrap, two comments, computed subtitle ancestry and numerical contrast results. All sampled rectangles, dimensions, colors/backgrounds and overflow are unchanged; document overflow0. Main-column textContent includes embedded CSS and therefore changes as source text; geometry comparison excludes that field. This does not close unrelated photographic zones.

Safe post-open clicks on both themes reach canonical posts29/30 with two comments. A desktop screenshot was visually inspected. Django check/migration passed;214 tests OK in51.437s, exit0, existing staticfiles warning only. Server/tab stopped, viewport reset, DB retained.

The pending100w Vodopad keyboard observation is also closed: native Right on the focused calendar region at320 yields settled scrollLeft40, client201/scroll348. The prior immediate zero was an incomplete observation, not evidence of broken scrolling. No calendar code change was needed.
