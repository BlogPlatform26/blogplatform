# Phase103m: right calendar containment

Dark Right and Classic Right dense calendars previously escaped the document on phones as well as tablets. The 24 paired blog/detail states at320/390/768/820/991/1440 had document excess88/64/58/58/59/0px respectively. All now measure0.

The two right-layout sidebar branches now wrap weekday labels and days in a named keyboard-focusable scroll region, scoped to these two designs. Below992px the calendar uses available sidebar width; the seven columns retain minimum44px targets and the grid has minimum44px rows. Phones scroll inside the calendar; tablets show the whole week. Desktop CSS is unchanged. Both one- and two-sidebar-column template branches receive the wrapper; browser fixtures exercise the default two-column configuration, so one-column browser acceptance remains open.

## Evidence

- 24 paired states: both designs, blog/detail,320/390/768/820/991/1440. Every final grid has zero cell intersections, including inactive days. Every document has zero horizontal excess.
- Phone scroll region widths207.33/277.33px contain a344px grid; tablet regions624.67/676.67/848px contain the complete grid. Local scrolling is intentional, not clipped inaccessible content.
- Four desktop samples are exactly identical for recorded calendar/day/column rectangles, linked-day fills and document excess. Full sampled classic-right desktop font/fill/background/opacity fields also match; aggregate text whitespace changed because of the wrapper. No broad pixel-identity or contrast claim.
- Native keyboard focus through day11 brings the phone region to scrollLeft136.67. The initial ArrowRight sample was0 and is not evidence of arrow scrolling. Safe native day11 clicks reach canonical posts250 and257.
- Phone and tablet geometry/height intentionally change. Desktop small target dimensions remain a separate ledger item.
- Screenshots at z/outputs/phase103m-calendar-phone.png (320 viewport, scrolled) and phase103m-calendar-tablet.png (991 viewport, scrolled) were visually inspected. These are viewport images, not full pages or1:1 DOM-pixel measurements.

## Validation

Django check: no issues. Migration dry run: no changes. Full suite:224 tests pass in48.849s. Isolated .qa100e.sqlite3 and workspace TEMP/TMP used. No original database/media/port8000 touched.

Raw evidence: z/work/phase103m/before.json and after-final.json (authoritative); after.json is an intermediate narrower tablet implementation and is not final evidence. Additional safe.json, keyboard.json, style-before.json, style-after.json and tests.txt. Bundled measurements accompany this note.

Remaining: one-column browser variant, desktop targets, other photo surfaces, factory Default and U02–U12 workflows; gradient hover/pixel limits remain. This is not final design acceptance.
