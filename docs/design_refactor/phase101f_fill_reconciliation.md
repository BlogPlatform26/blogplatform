# Phase101f - actual text-fill reconciliation

Read-only application audit on101e. Existing19 theme fixtures, blog/detail320/390/768/1440:152 states. Captures actual -webkit-text-fill-color with getPropertyValue, month/archive labels and weekday cells as well as previously sampled content/comments/actions. This is targeted reconciliation, not a complete19-theme acceptance matrix. Photo-null remains unresolved. No new fixtures or application changes.

100 sampled elements differ between color and fill. Differences concentrate in calendar arrows and Nebeski/Planine header ink. Magazin arrows still8.741:1; Svemirski tablet arrows16.630. Planine desktop title/subtitle actual5.009, correcting earlier6.636 color-only estimate but still passing. Nebeski subtitle actual2.543 across widths is a confirmed P1. Its title3.272 is not automatically a failure: assess large-text font threshold and anchor descendants. Other differences over photos stay null.

Additional solid-surface results below4.5 (font/descendant verification required where container selection could hide differing child styles):

- qa100e_dark .calendar-weekdays > div 1440:4.217, 320:4.217, 390:4.217, 768:4.217
- qa100e_classic .calendar-weekdays > div 1440:4.074, 320:4.074, 390:4.074, 768:4.074
- qa100e_dark_right .calendar-weekdays > div 1440:4.217, 320:4.217, 390:4.217, 768:4.217
- qa100e_classic_right .calendar-weekdays > div 1440:4.074, 320:4.074, 390:4.074, 768:4.074
- qa100e_simple_pattern .calendar-weekdays > div 1440:3.362, 320:3.362, 390:3.362, 768:3.362
- qa100e_simple_image .calendar-weekdays > div 1440:3.362, 320:3.362, 390:3.362, 768:3.362
- qa100e_simple_retro .calendar-weekdays > div 1440:3.247, 1440:3.791, 320:3.247, 320:3.791, 390:3.247, 390:3.791, 768:3.247, 768:3.791
- qa100s_vodopad_u_magli .calendar-weekdays > div 320:4.406, 390:4.406
- qa100s_planine_u_magli .archive-title 320:4.022, 390:4.022
- qa100s_planine_u_magli .calendar-weekdays > div 320:3.253, 390:3.253
- qa100y_nebeski_mir .archive-title 320:2.931, 390:2.931
- qa100y_nebeski_mir .calendar-weekdays > div 320:4.321, 390:4.321
- qa100y_nebeski_mir .blog-page-title 1440:3.272, 320:3.272, 390:3.272, 768:3.272
- qa100y_nebeski_mir .blog-page-subtitle 1440:2.543, 320:2.543, 390:2.543, 768:2.543
- qa101c_iznad_oblaka .calendar-weekdays > div 320:2.52, 390:2.52
- qa100e_dark .comment-time 1440:2.145, 768:2.145
- qa100e_classic .comment-time 1440:2.895, 768:2.895
- qa100e_dark_right .comment-time 1440:2.145, 768:2.145
- qa100e_classic_right .comment-time 1440:2.895, 768:2.895
- qa100e_simple_pattern .comment-time 1440:4.323, 768:4.323
- qa100e_simple_image .comment-time 1440:4.323, 768:4.323
- qa100e_simple_retro .comment-time 1440:4.115, 768:4.115
- qa100g_magazin .comment-time 1440:4.296, 768:4.296
- qa100y_nebeski_mir .blog-rich-content p 768:4.353

Priorities: batch confirmed small comment-date failures in shared base/Simple themes and Magazin, preserving mobile appearance; Nebeski subtitle actual fill; weekday labels and Planine/Nebeski archive headings. Use raw before evidence, verify actual child fill and size before implementing. Nebeski tablet body4.353 also needs factory-aware treatment. Earlier successful repairs are not blindly repeated; only these new measured gaps require work.

Raw/results: phase101f_fill_reconciliation.json. Source of inherited fill: base.html customization rules set fill for blog titles/subtitles, box labels and post dates; post_comments.html also explicitly sets mobile comment fill. Future probes must continue capturing actual fill. Opaque surface proof remains valid only with the actual foreground.

No duplicate full suite for read-only audit; latest214 tests101e OK46.479s. Server8017/tab closed and viewport reset. Isolated DB retained. Overall coverage19/37 is not19 passes;18 other themes, factory Default full scenarios, photo zones, desktop targets and user pages remain.
