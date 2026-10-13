# Phase101d - sidebar label contrast audit

Read-only application audit after101c: Zlatni horizont/Iznad oblaka, blog/detail320/390/768/1440,16 states with existing two-comment fixtures. New selectors: month label span, archive heading, sidebar headings and weekday cells, alongside the existing measurement set. Raw observations and computed-solid results in phase101d_sidebar_label_measurements.json.

Confirmed P1: Iznad archive heading on320/390 uses factory#f0dbe9 on solid#f7f4f6, contrast1.201:1,13px normal text. Both routes agree. services.py factory mapping at iznad_oblaka sets box_title_color#f0dbe9; design CSS consumes --box-title-color for calendar/archive/sidebar headings. This is not a screenshot artifact.

Month labels at all four widths, and archive headings at768/1440, remain photo-null: fallback composition is not rendered photographic proof. Zlatni mobile archive is15.036:1; no corresponding solid failure confirmed there. Do not globally darken all themes or claim photo areas pass.

Next: local factory-aware Iznad label treatment with a photo-independent surface where needed, preserving user palette selections and geometry; verify headings/labels in both routes/all widths, safe navigation, tests, screenshot and raw evidence. Consider extending the targeted selector audit to sidebar headings of remaining themes, since prior matrices omitted these labels.

Application unchanged; no redundant full suite. Latest full214 tests101c passed71.505s. Server8017 and tab closed; fixtures retained. Five-hour usage was84% at phase start, so a fresh capacity check precedes implementation. Goal remains incomplete.
