# Forest and polar archive headings over photographs

The factory archive captions remained transparent over photographic body pseudo-elements at tablet and desktop widths. Browser baseline records the actual foreground, font, opacity and ancestor/pseudo-element backing layers at 320/390/768/1440 for both themes. Adjacent desktop raster samples measured approximately 3.419:1 for forest and 3.702–3.754:1 for polar text; these samples are not a full glyph reconstruction or whole-theme contrast proof.

The existing exact box-title-color guards remain: forest #66755b and polar #d6efff only. Forest at >=576px now uses #354b32 on opaque #d4e3c4 (7.071:1); polar extends its existing #123047 on #f1fbff reading surface to every width (12.980:1). Nonmatching custom colors do not enter these branches. Phone appearance is unchanged. Tablet/desktop caption color and backing changes are intentional; dimensions and fonts are preserved.

Eight paired blog states cover both themes at all four widths. All16 sampled title/link rectangles match the baseline; local overflow0 and positive document overflow0. The raw document delta is -15 because it subtracts innerWidth including the scrollbar. No title/link overlap exists: link starts below the title in every sample. Native Enter on each October archive link reaches the correct year=2026&month=10 route and Back returns to the blog.

Evidence on durable disk: z/work/archive-photo-baseline.json, archive-photo-after.json, archive-photo-navigation.json; archive-polarna-pixel-analysis.txt. Inspected screenshots: outputs/archive-sumska-desktop-before.png, archive-polarna-desktop.png and archive-polarna-desktop-after.png (desktop viewport captures, not full pages). Final screenshot raster is1425x891 from the1440x900 override.

QA server87692 stopped; guest tab6 closed and viewport reset. This closes factory archive caption backing for these two themes on the measured blog route. Other photographic calendar/profile zones, custom palettes, post-detail coverage, desktop link targets and the full U01-U12 acceptance matrix remain separate requirements.

Validation: check clean; migration dry-run no changes; full250 tests53.798s passed. Raw z/work/archive-photo-suite.txt.
