# Phase100t — Vodopad / Planine comment dates

Baseline a148242; before evidence is Phase100s. Local rule only for vodopad_u_magli and planine_u_magli gives comment timestamps opaque #eef0e9, foreground #43513e and opacity1, with2px corner radius and no padding/layout changes. This closes the confirmed3.42–3.96:1 timestamp failures, and removes photo dependence for those timestamps. Other comment/photographic surfaces are unchanged.

## Verification

Both themes, blog/detail320/390/768/1440, synthetic authors2431/2432/posts29/30 with two comments:16states,32timestamps. Bootstrap loaded. Raw final measurements are phase100t_comment_time_after.json.

All timestamps compute rgb(67,81,62) on opaque rgb(238,240,233), element and ancestor opacity1, giving7.354005:1, including first desktop comments in photo zones. Every sampled element rectangle and local overflow equals the Phase100s baseline exactly. Document overflow0 throughout. Existing title/comment/calendar local overflow remains open, not hidden or counted as fixed.

Safe post-open clicks at390 reached both canonical posts and retained both comments. No mutations through like/comment controls. Desktop screenshot phase100t-comment-dates.jpg inspected: small light date surface, legible text and unchanged comment layout. Screenshot coordinates are not used for contrast calculations.

Django check: no issues; migration check: no changes. Full suite:214 tests OK in177.717s, exit0. Windows WMI/platform diagnostic0x8007000e appeared but execution continued and all tests passed; existing missing-staticfiles warning also appeared. Browser closed, viewport reset and QAserver8017 stopped; isolated fixtures retained. Original repo/DB/media/port8000/main/deployment untouched.

## Remaining scope

Next confirmed work is narrow-phone title/comment overflow and tablet calendars, with dense-week verification and44px targets. Confirm Planine subtitle font/child styling before its candidate contrast fix. Other photographic evidence, desktop targets, remaining22 special designs, full factory Default and user pages remain incomplete. Coverage15/37 is not15 passing designs.
