# Factory Default date contrast

The saved browser baseline covers blog/detail at 320, 390, 768 and 1440px for true factory fixture 2680. Its 24 visible years use yellow #ffd200 at opacity .72 on opaque white, giving calculated contrast 1.324:1 (unrounded alpha composition). Hidden inline variants are excluded. Day/month use a purple-to-yellow text gradient; endpoint calculations are not rendered-pixel proof.

Default now substitutes #755600 for the gradient secondary color and makes year/separator text opaque, only when both exact factory colors (#7a2cff/#ffd200) and the gradient effect match. Primary purple remains. Custom primary, secondary, solid and duo configurations retain their existing styles; the render test exercises all five branches. This intentionally changes date colors on desktop as well as mobile.

Eight paired final states have identical sampled date rectangles and fonts, document excess 0 and date local excess 0. Actual year fill is rgb(117,86,0), opacity 1, calculated white contrast 6.802:1. Actual day/month gradients use the new secondary; primary endpoint contrast is 5.782:1. These calculations do not constitute raster gradient acceptance. Enter on the phone blog's Open post link reaches canonical post272. Full keyboard acceptance remains open.

Raw artifacts: C:/Users/mario/Documents/Codex/2026-10-10/z/work/factory-default/date-before.json, date-baseline-verification.json, date-after.json and date-suite.txt. Inspected screenshot C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/default-date-phone.png is a 390px viewport, not a full page. No new baseline capture was needed. No content, preference or email mutation.

238 tests pass in 52.972s, including custom-date guard coverage. Django check and migration dry-run pass. QA server stopped and measurement tab closed; viewport reset. This closes the confirmed factory year contrast problem, not the entire Default or 37-design acceptance scope.
