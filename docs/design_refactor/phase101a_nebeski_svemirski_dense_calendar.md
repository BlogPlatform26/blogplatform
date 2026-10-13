# Phase101a — dense calendar verification

Read-only application audit on100z. Isolated authors2461/2462 (`qa101a_nebeski_mir`, `qa101a_svemirski_horizont`), posts47–53/54–60, October5–11, provide seven active days in one week. Both blog/detail320/390/768/1440 measured with Bootstrap:16 states. [Raw evidence](phase101a_dense_calendar_measurements.json).

| Design | Width | Document overflow | Grid overflow | Active targets |
|---|---:|---:|---:|---|
|Nebeski|320|92|145|7 ×44×44|
|Nebeski|390|22|75|7 ×44×44|
|Nebeski|768|0|229|7 ×44×44|
|Nebeski|1440|0|0|~27×34|
|Svemirski|320|91|143|7 ×44×44|
|Svemirski|390|21|73|7 ×44×44|
|Svemirski|768|0|0|7 ×44×44|
|Svemirski|1440|0|0|~27×34|

Blog/detail agree. The existing Svemirski tablet layout fits this dense week at768; do not replace it simply because Nebeski fails. Both phone calendars need local containment preserving seven days and44px targets; Nebeski additionally needs tablet capacity. Desktop targets remain open. This audit is not photographic contrast proof or a complete theme pass.

Application unchanged; latest full214-test result is100z OK51.544s. No duplicate full suite for fixture-only/read-only audit. Server8017/tab closed, viewport reset, synthetic fixtures retained. Original repo/database/media/port8000 untouched. Use this as dense before evidence for the next implementation alongside100z standard states with comments.
