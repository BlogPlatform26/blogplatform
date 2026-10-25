# Phase103e: anonymous following filter

Date: 2026-10-25. Baseline 5192feb. Isolated .qa100e.sqlite3, localhost8017.

## Problem and change
Anonymous `?filter=following` rendered public all-post results below the personal followed-post heading. Before evidence at320/390/768/1440 contains posts221–225 and page1/46. This was a label/filter mismatch, not private-data exposure.

An unavailable anonymous personal filter now uses the existing public default, featured, just like an unrecognized filter. The URL is not redirected; rendered filter, heading, tag and pagination links consistently use featured. Authenticated filtering is unchanged. No template/CSS changes.

## Evidence
- Four anonymous after states render Istaknuti postovi, document overflow0.
- Four direct featured controls exactly match sampled filter rectangles/fill and title text/links/rectangles in the anonymous fallback at each width.
- Native next navigation reaches featured page2 with posts227/228.
- Reader2672 login succeeds; four following states retain the personal heading and five first-page title links, document overflow0. Reader follows author2671. Logged out afterward.
- Four new regression tests cover guest default, followed-author inclusion/unfollowed exclusion, empty owner feed excluding own posts, and all-feed inclusion. Targeted4 tests pass1.262s; check and migration check pass.
- Browser owner-empty remains unverified: previously summarized author credential fails; read-only DB check confirms owner has no follows and that credential does not match. Reader credential does match. No credentials changed. Empty-owner behavior is proved by an isolated server test only.

Before raw doc delta used scrollWidth-innerWidth=-15 (scrollbar allowance); this is not negative overflow. After uses nonnegative scrollWidth-clientWidth. Before/after different feeds intentionally have different card geometry; no universal geometry claim.

Screenshot: z/outputs/phase103e-guest-following.png is a320px viewport, not a full page; inspected and shows the active featured filter/heading and synthetic long title. Raw data: z/work/following-audit. Screenshot is not new gradient pixel-contrast proof.

Initial full suite failed15 tests during sandbox temp-directory cleanup (WinError5); rerun uses TEMP/TMP inside the writable workspace. Rerun: all223 tests pass in64.364s. No app changes between runs. QA server stopped; browser test tab closed and viewport reset.

## Remaining
Empty-owner browser workflow, desktop long author clamp, gradient native-hover/pixel evidence and all remaining acceptance ledger items stay open. This does not close U01 as a whole.
