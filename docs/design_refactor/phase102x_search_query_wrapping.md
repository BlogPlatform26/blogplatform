# Phase102x: unbroken search query containment

Baseline8301004. A180-character unbroken query (LongQuery repeated20 times) was visibly clipped. Document overflow and the generic sampled local-overflow probe were both0, yet the actual strong text rectangle exceeded its parent by1431.958/1361.958/1408.583/1088.625px at320/390/768/1440. This is another case where document overflow0 does not prove containment.

The query summary receives a search-query class and overflow-wrap:anywhere at all widths. Actual query rectangle excess is now0 at all four widths; all182 rendered characters including quotation marks remain present. The additional height is intentional for a long unbroken query. Four ordinaryqa/posts control states have identical sampled rectangles and actual fill to102w. No general post-title/body or theme styles changed.

Browser scope switch to users preserved the complete query and contained text. Screenshot z/outputs/phase102x-long-query-phone.png is the initial320px viewport, not a full page. Raw phase102x_measurements.json contains before/after, direct text/parent rectangles, actual fill and the safe navigation URL. The isolated QA server was restarted after changing the cached template.

This closes long query-summary clipping, not all long-content scenarios. Populated long post titles/content/tags/user names, following-owner/featured states, inactive-filter contrast and keyboard order remain open U01 work. No37-design re-audit. Original database/media/port8000 untouched.

Check and migration check passed; full216 tests passed97.700s. QA server/tab closed and viewport reset.
