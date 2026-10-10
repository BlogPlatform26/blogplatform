# Phase100j - Magazin photographic title contrast evidence

## Result

On application commit `28af9a6`, the factory white Magazin blog title over the selected system `soho_sunrise_valley` photograph has confirmed low-contrast locations. This closes the measurement gap from Phase100g; it does **not** close the defect. No application code changed.

## Method

Isolated `.qa100e.sqlite3`, synthetic author2402, post12, existing two comments. Blog and detail at 320/390/768/1440, Bootstrap loaded. Computed title: white, Georgia 32px/35.2px, weight500, black shadow alpha0.20 offset0/8px blur22px. Photograph loaded. This large title requires at least3:1; target the eventual fix above4.5:1 with margin.

Captured paired viewport JPEG screenshots with the original title and an NBSP title in the synthetic database. NBSP retains the line height while removing glyphs and their shadow. Image bounds, title height and scroll position were identical in every pair. Original `QA magazin` title restored and verified in the browser, with both comments present. No original data/media changed.

Full-page screenshot attempts changed captured responsive layout and were discarded. Final evidence uses viewport screenshots only, with 540px scroll for 320/390/768 and zero for1440. For each original title rectangle, selected pixels whose original RGB channels were all >=240 and each at least20 brighter than the paired background. These interior white-glyph candidates yield 220-231 samples per state. Used WCAG sRGB relative luminance and nominal white foreground against the photographed/gradient-composited background. JPEG sampling makes these approximate measurements, not exact exhaustive glyph minima.

## Results (blog and detail agree)

| Width | Samples per route | Lowest sampled ratio | Samples below3:1 | Conservative ratio with full20% black shadow at lowest point |
| ---: | ---: | ---: | ---: | ---: |
|320|225|1.48|132|2.34|
|390|230|1.44|139|2.27|
|768|220|1.74|57|2.72|
|1440|231|1.51|90|2.37|

The last column deliberately applies the maximum shadow alpha uniformly at the sampled background point. Actual blurred shadow cannot supply more darkness. Even this favorable upper-bound contrast stays below3:1. Together with numerous failing interior samples and visual inspection, the margin is sufficient to establish a defect despite JPEG quantization and pixel rounding. This does not claim exact antialias-edge contrast or complete coverage of every photograph and title.

## Next implementation

Preserve the photographic hero and factory white title, but add a localized reliable dark contrast surface behind the title, consistent with the existing dark tagline caption. Preserve explicit user palette choices. Verify the resulting title surface on blog/detail at all four widths, including long wrapping titles and existing comments, before committing application changes. Do not treat a stronger translucent whole-hero gradient alone as proof for arbitrary images.

Remaining: other26 special designs need current final matrix; factory Default needs a complete nonlegacy pass; desktop touch targets and historical local overflow remain open. All37 are not complete.

## Validation

Documentation-only phase. `git diff --check` passed. Last full application validation remains Phase100i: check/migration and214 tests passed on unchanged application code. QA server8017 and temporary browser closed; isolated fixture restored. No main/merge/deploy or source repository changes.
