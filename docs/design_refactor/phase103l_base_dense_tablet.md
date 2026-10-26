# Phase103l — Base populated tablet week audit

Read-only application audit after ed6bf81. No CSS changes. Created isolated synthetic users2674–2677: qa103l_dense_dark, qa103l_dense_classic, qa103l_dense_dark_right, qa103l_dense_classic_right. Posts230–236/237–243/244–250/251–257 publish on2026-10-05 through11 (Monday–Sunday); created_at matches publish_at. Existing fixtures were not modified.

24 browser states: four themes, blog/detail,768/820/991. All have seven active links of44x44 with no mutual rectangle intersections. Dark/classic have document excess0. Dark_right/classic_right each have document excess58/58/59 at768/820/991 on both routes. Thus this is NOT a dense-calendar acceptance pass.44px alone did not ensure containment.

At991 classic_right, the final day column ends at x1034.333 while document client width is976; day10 ends984.333. Overflow nodes are calendar days, not a long profile name. Existing101i stacks columns but does not expand the right calendar grid backing. Next implementation must contain the whole seven-column grid, preserve phone/desktop behavior, and compare before/after320/390/768/1440 plus820/991. Column rectangles and calendar box/grid local widths are in the measurement bundle; do not infer column nonoverlap without calculating it.

Safe native day11 clicks reached canonical detail236/243/250/257. Raw z/work/phase103l/states.json and safe.json. A991 scrolled viewport was captured at z/outputs/phase103l-right-tablet.png; not yet visually inspected, so it is not claimed as reviewed visual evidence. No full suite rerun for this audit; latest224 tests76.836s passed103k. Other photo/default/targets/user-route acceptance remains open.
