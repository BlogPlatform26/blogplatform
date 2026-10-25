# Phase103i: Jedro subtitle, date and profile surfaces

Baseline aec21c7. Isolated QA database and localhost8017,2026-10-25.

The subtitle and guest profile panel now use opaque #fff7e9; the date shell uses opaque #2d1f18. Existing ink, typography and layout declarations are retained. Desktop backgrounds intentionally change; photograph remains around these local text surfaces.

Eight blog/detail states at320/390/768/1440 retain all sampled rectangles, font, color and fill exactly, with document overflow0. Actual visible date day/month/year fill is #f6d0ae, unlike its dark container fill; final backing therefore uses dark brown. An initial light date surface was rejected during screenshot review and is not the final result. Raw after.json records that rejected intermediate state; after-final.json is authoritative. Profile actual child fills include dark text and blue author link, with opaque panel backing. All sampled actual-child local overflow0.

Computed opaque contrasts: subtitle/profile text 17.692, profile link 7.586, date children 11.018. These use actual computed fill and stable opaque surfaces, not a claim to have sampled photograph pixels. Header, profile section caption, calendar/archive captions and other photo-null cases remain open. Guest profile verification does not prove all authenticated action states.

Safe calendar20 click resolves canonical post174. Desktop1440 and phone390 viewport screenshots are z/outputs/phase103i-jedro-desktop.png and -phone.png; visually inspected, not full pages. Raw evidence z/work/phase103i. Browser REPL reset once; before evidence survived on disk and final after was recaptured.

Validation: Django check and migration dry-run passed. Final full suite:223 tests pass61.059s. No new test for background-only CSS. Server30062 stopped; tab7 closed; viewport reset.
