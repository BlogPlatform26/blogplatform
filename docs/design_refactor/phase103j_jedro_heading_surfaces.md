# Phase103j — Jedro factory heading surfaces

The factory blog title and section captions were light text over the photograph. They now receive an opaque #2d1f18 background. Independent template guards apply only while blog_title_color is #fff7ee and box_title_color is #fff5ea, respectively. Customized heading colors retain their previous surface behavior; arbitrary custom palettes are not accepted by this change.

## Browser evidence

Isolated .qa100e.sqlite3, author2612 qa102g_jedro_u_suton, published post174. Eight paired blog/detail states at320/390/768/1440 retain every sampled rectangle, font, fill and local-overflow value. After document scrollWidth equals clientWidth. The earlier blog raw doc field was scrollWidth minus innerWidth (-15 from the scrollbar), not a negative overflow claim.

Actual title fill #fff7ee and caption fill #fff5ea on actual opaque #2d1f18 give calculated contrast14.984 and14.765. Heading nodes contain direct text, with no differing child fill. These are computed-color contrast calculations supported by inspected screenshots, not a raster-pixel minimum measurement. Backgrounds intentionally change on desktop too; photograph and sampled layout remain.

Safe native calendar day20 navigation reached post174 and its canonical detail URL. The independent-color test exercises both routes with factory/factory, custom/factory, factory/custom and custom/custom colors.

Viewport screenshots: C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase103j-jedro-phone.png (390 detail) and phase103j-jedro-desktop.png (1440 blog). Both visually inspected: title readable on brown; desktop profile/calendar/archive captions have brown bars. These are viewport captures, not full-page or 1:1 DOM-to-raster evidence.

Raw evidence: z/work/phase103j/before-blog.json, before-detail.json, after-blog.json, after-detail.json, safe.txt, tests.txt. The committed phase103j_measurements.json bundles measurements. Earlier PENDING.md is superseded by this report.

## Remaining scope

Authenticated profile actions, arbitrary customized palettes, optional user-box content, other photo zones (including Lavande profile/archive), calendar targets/default design and user workflows remain in the ledger. No new all37 audit was performed.

## Validation

Django check and makemigrations --check --dry-run passed; full suite224 tests79.639s passed. Git diff --check passed.
