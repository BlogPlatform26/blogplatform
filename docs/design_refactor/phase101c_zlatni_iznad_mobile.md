# Phase101c - Zlatni horizont / Iznad oblaka

Current standard and dense fixtures: authors2471/2472 with posts61/62 and two comments each; dense2481/2482 with posts63-69/70-76 for October5-11. Isolated .qa100e.sqlite3 only. Both blog/detail at320/390/768/1440:32 before and32 after states, Bootstrap loaded.

Confirmed before failures: phone title overflow Zlatni79px at320/9px at390, Iznad68px at320; comment text3/2px at320. Dense phone document overflow91/21 and90/20px at320/390. Tablet dense calendars already fit seven44px links. Dates: Zlatni>=7683.875:1, Iznad phone3.944 and solid desktop3.453; photo date remained null. Iznad author link4.175:1 because its nested anchor retained lighter ink despite the existing parent override.

Changes: extend existing phone title-above-date, long-comment-word wrapping and locally scrollable seven-column calendar rules to both themes. Keep tablet layouts. Zlatni dates>=768 use opaque#1a1009 with existing#f0d6bd ink and opacity1,13.421:1; phones unchanged11.036. Iznad dates use opaque#fff7fc/#514956,8.190:1 all widths. Include the actual author anchor in its existing Phase87d ink rule,8.190:1. No customization storage changed.

After: all32 states document and sampled local overflow0. Active dense links remain7x44px on phone/tablet. All sampled tablet/desktop rectangles match before within0.05px. Native Right scroll settles40px in both phone regions; day11 opens69/76. Standard post-open reaches61/62 with2 comments. No content mutation through UI. Raw observations/results/navigation in [measurements](phase101c_measurements.json).

Validation: check clean, migration dry-run no changes,214 tests OK71.505s; expected missing-staticfiles warning. Screenshot captured at390 and inspected: it reveals very pale month heading/archive label, not covered by existing measured selectors. These are NEW OPEN candidates requiring actual computed styles and surfaces; do not mark theme complete. Photo-null areas and desktop targets remain open. Screenshot geometry is not used for pixel contrast calculations.

Current coverage19/37 is not19 passes. Next inspect month/title/archive labels and reconcile screenshot versus computed colors; then remaining18 themes. Server/tab closed, synthetic fixtures retained. Only design-refactor push; original repo/database/media/port8000 untouched.
