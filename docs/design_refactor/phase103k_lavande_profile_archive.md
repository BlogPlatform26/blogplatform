# Phase103k — Lavande profile and desktop archive surfaces

The guest profile panel was transparent over the photograph. It now uses the existing #f5e6fa theme surface. The factory archive caption already had that backing below992px; the existing #6a3c84 color guard now supplies the backing at desktop widths too. Phone/tablet caption ink is unchanged, and custom caption colors retain their prior behavior. Archive links were already protected and were not changed.

## Evidence

Eight paired blog/detail states320/390/768/1440 use isolated author2531 qa101v_polje_lavande/post109. Every sampled rectangle/font/fill/local-excess value matches, all sampled child fill/font/opacity/background values match, document excess0. The blog view count changed1 to2 after detail navigation; text-content identity is not claimed. Profile actual #5a3271 has calculated8.257 contrast; its secondary label retains opacity0.8, composed contrast4.987 on #f5e6fa. Desktop archive caption #6a3c84 gives6.782. Current390 detail ancestor checks show opacity1/filter none/blend normal. These computed-color calculations are not raster-pixel minimum measurements.

Native calendar day18 opened canonical post109. Phone390 scrolled profile and desktop1440 detail viewport screenshots were visually inspected: profile text is readable on light lavender and desktop archive caption has a light rectangular backing. Desktop background appearance intentionally changes while photograph and measured column geometry remain. Screens are z/outputs/phase103k-lavande-phone.png and phase103k-lavande-desktop.png; they are not full-page captures.

Raw z/work/phase103k/before.json and after.json are bundled in phase103k_measurements.json; safe.txt records navigation, tests.txt records full-suite output.

## Scope remaining

Authenticated profile actions, optional profile content/custom palettes, other photographic zones, default design/calendar targets and user workflows remain in remaining_verification_scope.md. This does not assert acceptance of all37 designs. No previously closed calendar/header ink was changed.

Validation: Django check and migration check passed;224 tests passed76.836s. Git diff --check passed.
