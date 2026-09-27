# Phase 82d — Plus tablet layout

## Scope and decision

The two-sidebar variants `default_right`, `dark_right`, and `classic_right` previously switched directly from the mobile stack to a 50/25/25 three-column row at 768 px. At tablet widths this left each sidebar too narrow for the calendar.

For `right_box_columns == '2'`, the 768–1199.98 px range now gives the main content a full row and places the two visible sidebars below it at 50% each. No content is hidden. The existing mobile stack below 768 px and the existing desktop 50/25/25 layout from 1200 px remain unchanged. The separate `right_box_columns == '1'` branch remains unchanged at 60/40.

## Browser measurements

Measurements used an isolated database copy with six synthetic published posts and archive mode `both`.

| Viewport | Before | After |
| --- | --- | --- |
| 320 px | existing full-width mobile stack; calendar 236.67 px; 44 px mobile targets | unchanged |
| 390 px | existing full-width mobile stack; calendar 260 px; 44 px mobile targets | unchanged |
| 768 px | content 340 px; sidebars 170 px; calendar 144 px; active day 14.69 px; month title wrapped | content 680 px; sidebars 340 px; calendar 260 px; active day 27.81 px; month title one line |
| 1024 px | content 468 px; sidebars 234 px; calendar 208 px; month title wrapped | content 936 px; sidebars 468 px; calendar 260 px; month title one line |
| 1440 px | content 676 px; sidebars 338 px; calendar 260 px | unchanged |

At every measured width, `documentElement.scrollWidth` equaled `clientWidth`. Browser checks of `dark_right` and `classic_right` at 768 px produced the same 340 px sidebar / 260 px calendar result. With `default_right` explicitly configured for one sidebar column, the existing 60/40 layout remained active, the left sidebar stayed hidden, and the Phase 82d contract was not rendered.

Safe clicks passed at 768 px for previous month, next month, a multi-post day, and an archive month.

## Regression coverage

`PlusTabletLayoutContractTests` verifies the tablet contract for all three Plus designs when configured for two sidebar columns and verifies that the one-column branch remains separate.

The original `db.sqlite3`, user media, port 8000, `main`, merge state, and deployment state were not changed.
