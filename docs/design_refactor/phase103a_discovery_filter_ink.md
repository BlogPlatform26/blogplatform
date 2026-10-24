# Phase103a — discovery filter ink and keyboard finding

Baseline b8f571a. Previous phase102z was progress: committed missing fallback asset and browser/test evidence. Fork confirmed inactive; worktree clean before edits. Capacity89% five-hour consumed, ordinary usage allowed; no reset requested.

## Scoped change

Home/search inactive filters previously rendered actual #888 on opaque white (3.544886:1). Route-conditional .discovery-layout-row rule now uses #595959 for both color and -webkit-text-fill-color, giving7.004729:1. Active and hovered filters retain existing rules. This deliberately changes inactive desktop filter color as well as mobile; no claim that all desktop colors are unchanged.

## Browser evidence

Eight before/after states: home featured and search qa102y/posts at320/390/768/1440. Every measured filter rectangle is identical before/after, document overflow0, active fillblack preserved. Raw actual fill, font, weight, ancestor backgrounds/opacity/image and geometry are in phase103a_measurements.json. Scope is these controls, not all text or photo contrast. Safe click Korisnici retained q=qa102y and reached scope=users. Viewport screenshot C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase103a-search-filters.png is320px requested viewport, not full page; visually inspected.

## Confirmed keyboard gap

DOM focusable order places support controls before main filters. At320 home, native Tab from Registration focused an INPUT radio, whereas support radio sits at document y5166.7 and main filters at y272.2. This proves source/focus order differs from phone visual order; it does not prove a scroll jump (scrollY remained0 in the recorded action). Preserve this as the next scoped layout/focus correction, not a passing keyboard audit. Existing visual order repair is retained.

## Remaining scope

U01 keyboard order, gradient text contrast, empty following/owner distinctions and tablet secondary-card usability remain. U02–U12 and design photo/default/target acceptance gaps remain. No new37-design sweep.

## Validation
Django check and migration dry-run green. Full217 tests passed in125.035s. Isolated QA database/port8017 only. No schema change.
