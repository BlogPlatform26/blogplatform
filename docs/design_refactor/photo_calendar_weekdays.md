# Photographic calendar weekday readability

Vodopad u magli, Planine u magli, Nebeski mir and Iznad oblaka used partially transparent11px weekday text over photographs at wider widths. Actual browser fill alpha was0.78/0.76/0.70/0.62. Adjacent backing samples from tablet/desktop screenshots yielded composed ratios2.325–4.275; these are bounded raster samples, not full glyph reconstruction.

At >=576px each fixed theme weekday row now has opaque existing RGB ink and an opaque matching canvas-color strip. Measured child foreground and parent backing produce ratios: Vodopad7.472, Planine5.117, Nebeski9.819, Iznad5.309. This intentionally changes tablet/desktop weekday color/backing. No custom caption-color variable is overridden; these weekday colors were fixed theme rules already.

Sixteen paired blog states (four themes ×320/390/768/1440) retain every sampled calendar rectangle and font. The complete sampled phone records are identical before/after. Positive document overflow0; row cells remain separated with no dimensions changed. Existing local scroll regions and narrow tablet Iznad layout are not newly certified by this contrast patch. Native Enter on Previous month reaches each author's year2026/month10 route.

Durable raw: z/work/photo-calendar-baseline.json and photo-calendar-pixel-analysis.json (prior photographic backing); weekday-before.json, weekday-after.json, weekday-navigation.json. Inspected final screenshot outputs/weekday-iznad-desktop.png is a desktop viewport capture, not full page. QA server76602 stopped; guest tab9 closed and viewport reset.

Scope is weekday text on measured guest blog routes. Date numbers, today/active/hover states, arrow contrast and desktop targets, post-detail routes and full U01-U12 acceptance remain open. No whole-calendar or whole-theme acceptance claim.

Validation: check clean; migration dry-run no changes; full250 tests67.005s passed. Raw z/work/weekday-suite.txt.
