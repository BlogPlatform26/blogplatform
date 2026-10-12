# Phase100w — Vodopad/Planine dense calendars

The 768 px three-column layout leaves insufficient calendar width for seven active 44 px days. Dense synthetic weeks also reproduce document overflow on phones. Vodopad/Planine now share the existing Litica/Podvodna calendar capacity rules: full-width columns at 768–991.98, a local horizontal calendar scroller on phones, aligned weekday/day grids and unchanged seven-day semantics. Today scale is removed below 992. The phone hint uses these themes' opaque #eef0e9 / #43513e pair (7.354:1). Existing Litica/Podvodna timestamp rules remain restricted to those themes.

## Evidence

[Raw before/after and additional observations](phase100w_calendar_measurements.json). Isolated authors 2441/2442 (`qa100w_vodopad_u_magli`, `qa100w_planine_u_magli`), posts31–37/38–44 on October5–11 provide seven active days. Standard authors2431/2432 retain two comments. Both fixtures, themes, blog/detail and320/390/768/1440 give32 states before and32 after with Bootstrap.

| Dense blog before |320|390|768|
|---|---:|---:|---:|
|Vodopad document overflow|91|21|0|
|Planine document overflow|100|30|0|
|Vodopad grid overflow|143|73|227|
|Planine grid overflow|155|85|239|

After: document and grid overflow0 in all32 states. On phones the intentionally wider grid scrolls within its labelled focusable region; no day is removed or narrowed. Active targets remain at least44×44 below992. Additional dense blog820/991 observations have no grid/document overflow. All sampled1440 rectangles, scroll/client widths, colors and backgrounds match before. Desktop targets remain small and open; no desktop accessibility completion is claimed.

Day11 safe clicks reach canonical posts37/44. Native Right on the focused Planine region moved scrollLeft to40; locator key attempts returned0, and Vodopad's immediate native observation also returned0, so the latter is not claimed as a completed keyboard-scroll proof. Both day11 links remain reachable through normal link activation. A tablet screenshot was visually inspected. No screenshot-coordinate photographic contrast inference is made; existing unresolved photo-zone evidence remains open, including relocated tablet calendar text.

Check/migration passed. Full214 tests passed in56.654s, exit0, with the existing missing-staticfiles warning. Server8017/tab closed, viewport reset, fixtures retained. Original repo/database/media/port8000 and main untouched.
