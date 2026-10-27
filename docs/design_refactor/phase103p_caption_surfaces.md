# Phase103p — Planine and Nebeski factory captions

The calendar month and archive captions in Planine u magli and Nebeski mir retained pale factory ink over photographic/translucent surfaces. The phone archive ink had already been corrected in Phase101k; this phase retains that ink and supplies a stable background.

Exact box_title_color guards (#6c7d8f and #8f96aa respectively) now apply #43566c / #475569 ink and opaque #f1f5fb to the caption containers. The actual month span receives the same ink. Custom palette values bypass these additions; this is not browser acceptance of custom palettes. No dimensions or fonts change. Backgrounds intentionally change on desktop as well as phone/tablet.

## Browser evidence

Sixteen paired states cover both designs, blog/detail, and 320/390/768/1440 viewport widths with Bootstrap loaded. Fixtures are qa100s_planine_u_magli/post30 and qa100y_nebeski_mir/post45. Every sampled caption, container and main-column rectangle and font matches its before value. Document excess is zero in all states. Final caption local excess is zero and opacity is one. Actual month child and archive fills are #43566c / #475569; both caption backgrounds resolve to opaque #f1f5fb. Calculated contrast is 6.889 / 6.926 respectively, not a rendered-pixel contrast claim.

Native day13 and day11 clicks reach canonical detail45 and detail30. The inspected screenshots are viewport captures: z/outputs/phase103p-captions-phone.png (390, Planine blog) and phase103p-captions-desktop.png (1440, Nebeski detail). Their raster dimensions differ from the viewport overrides; they are not full-page captures.

Raw evidence is in C:/Users/mario/Documents/Codex/2026-10-10/z/work/phase103p: before.json, after-final.json, local-final.json and safe-final.json. after.json is an intermediate rejected result: archive background overrides were still translucent. The final rule explicitly overrides those existing background declarations. See phase103p_caption_surfaces_measurements.json for the compact comparison.

Validation: Django check and migration drift check pass. The final full suite passes 224 tests in 64.852s (tests-final.txt); the earlier run preceded the final background override and is not the release evidence.

Calendar weekday/day ink, navigation targets, other photographic labels, authenticated profile actions, custom content and the broader acceptance ledger remain open.
