# Phase103g: empty following feed for a published author

2026-10-25. Baseline757d539. Verification only; no application code changes.

Created synthetic owner2673 qa103g_empty_owner and published post229 in isolated .qa100e.sqlite3. The owner follows nobody. Existing author2671 credentials were neither changed nor retried. New fixture remains for later QA.

Native login succeeds. Clicking Samo oni koje pratim renders the personal heading and Nema postova., without post links in the main column at320/390/768/1440. Document and sampled local overflow are0. Filter rectangles do not overlap each other; heading and empty message follow without overlap. Actual heading/message fill is rgb(33,37,41), with transparent local surfaces over white body; inactive filters remain #595959 and active black. These are computed-style observations, not a new rendered-pixel contrast claim.

Native Svi postovi navigation reaches ?filter=all and displays the owner's published post229. Returning through the following filter restores the empty state. Native logout verified by the Prijava link. This distinguishes empty following from no published content and closes the previously server-only owner-empty browser check.

Screenshot z/outputs/phase103g-empty-owner.png is the320px viewport, not a full page. Visually inspected: active following filter, wrapping personal heading, empty message and support below. getScreenshot failed; supported tab.screenshot succeeded. Raw files live in z/work/phase103g; measurements accompany this report.

No CSS/template/runtime code changed, so the prior223-test green run49.363s from103f remains the latest full suite; it was not rerun for this documentation-only phase. QA server98150 stopped, tab5 closed, viewport reset.

Gradient native-hover/rendered-pixel evidence, full-name preview usability and all other open ledger items remain. This does not close U01 or the overall goal.
