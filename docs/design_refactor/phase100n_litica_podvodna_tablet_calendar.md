# Phase100n - Litica / Podvodna tablet calendar capacity

## Cause and change

Phase100l confirmed calendar overflow at768px. Seven active days reproduce a larger228px grid overflow: a117px sidebar grid cannot fit seven44px targets plus gaps. For `litica_noci` and `podvodna_tisina` only,768-991.98px now uses full-width main columns, preserving their normal stacked ordering. The calendar uses available width instead of Podvodna's260px cap. Today's scale transform is disabled in this tablet range because it added1-2px overflow on a rightmost noninteractive day. Colors and44px target minimums are retained. Phone and desktop rules are unchanged.

## Browser evidence

Isolated `.qa100e.sqlite3`, server8017, real Bootstrap and native photographs. Standard before/after: authors2411/2412, posts13/14 and both comments, blog/detail320/390/768/1440 (16 states each). Current day11 means the day10 active target no longer has today's scale; do not compare transformed sizes from yesterday without accounting for the date.

Dense fixtures: authors2421 `qa100n_litica_noci`,2422 `qa100n_podvodna_tisina`; published posts15-21/22-28 on October5-11, all seven days of one week active. No source database or media used.

| Tablet dense grid |768px|820px|991px|
| --- | ---: | ---: | ---: |
| Litica width |633.42|682.71|845.13|
| Podvodna width |632.75|682.04|844.46|
| Grid overflow, both |0|0|0|
| Minimum active target, both |44x44|44x44|44x44|

Dense blog AND detail checked at each width (12 states). Before dense768 grid overflow228px; after0. Standard768 calendar-box/grid overflow also0, from approximately35/51px before. Document overflow0 in all standard states and all dense tablet states. Measured columns/calendar/card/targets at320/390/1440 are identical before/after. Existing Litica1px grid overflow with today's noninteractive day at phone widths remains; it is not represented as a pass.

Boundary checks:767 retains full mobile columns,992 returns to the original three columns; standard992 calendar overflow0. A Magazin control does not render the Phase100n rule. Visual inspection confirms a readable tablet calendar and comments; desktop geometry equality confirms the unchanged desktop arrangement.

At768 both designs passed previous/next month, active day to canonical detail and comments navigation; both comments remain. No mutating browser controls used. Moved body/comment content is below the photo: Litica body16.43, comment author5.75, guest hint12.52; Podvodna body15.92, author5.37, hint12.10. Calendar navigation still intersects photographs and is not declared a verified contrast pass. Desktop photographic gaps from100l remain open.

## Newly confirmed next priority: dense phone calendar

Additional dense-fixture checks reveal existing document overflow outside this tablet-only change:

| Design/width |Grid overflow|Document overflow|
| --- | ---: | ---: |
|Litica320|144|92|
|Litica390|74|22|
|Podvodna320|144|92|
|Podvodna390|118|66|

These new fixtures demonstrate a case the earlier single-post mobile checks did not cover. Next phase must fit or intentionally contain the seven-day calendar on phones while preserving interactive targets and calendar semantics, with safe navigation and no document overflow. Do not shrink days to18px as an earlier unrelated tablet fix did. The phone problem is not closed by this phase.

## Validation and status

System check and migration drift check passed. All214 tests passed in126.471s, with the existing missing collected-static directory warning. `git diff --check` passed. Source repository/database/media, port8000, main/merge/deploy untouched. QA server/browser stopped; synthetic fixtures retained. Remaining24 current special-design batches, full factory Default, photographic proofs, other touch targets and user pages remain open.
