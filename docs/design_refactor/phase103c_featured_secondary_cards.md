# Phase103c - secondary featured cards

Baseline e5fd69a. Fresh Git clean/synced, both other project tasks inactive, ordinary capacity available. Previous turn yielded new raw evidence rather than a new application change. Only isolated QA database and port8017 used.

## Changes and browser evidence

Secondary date text is now opaque #595959 instead of rgba(0,0,0,.5). Actual child count0,11px700, ancestor card opaque white and opacity1: contrast rises from3.977 to7.005. This deliberately changes date ink on desktop as well as mobile.

At768-991.98px the secondary grid uses three columns instead of six, and title/author text wraps anywhere. The two populated synthetic cards were measured before/after at320/390/768/820/991/1440. Tablet card widths106.44/115.10/143.67 become230.89/248.22/305.33px. Tablet long author local overflow1156/1147/1119 becomes0; cards do not overlap. The existing two-line preview clamp remains. Phone and1440 sampled card/grid/text rectangles are exactly equal in paired captures; six desktop columns remain. Document overflow0 in all six after states.

Raw before-final.json, after.json, ink-inspection.json and safe.json are consolidated in phase103c_measurements.json. Earlier exploratory before.json is not the paired baseline. Own server restarted after template edit. Native click on the first secondary card reaches post227 canonical detail URL. Screenshot C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase103c-secondary-tablet.png shows the scrolled768 requested viewport, not the full page; visually inspected.

## Acceptance boundary

This closes the demonstrated tablet secondary width/wrapping and secondary date contrast findings. Transparent title fill is accompanied by a clipped gradient, not an invisible title. Bright gradient segments still need contrast work; the screenshot confirms their pale appearance but is not a numeric pixel contrast measurement. Long unbroken desktop author remains clamped with local scrollWidth excess1044; this phase does not close that usability case. Empty following/owner states, other user routes, photographic text, factory Default, target and dense-week checks and final acceptance remain open. No new sweep of37 themes.

## Validation

Full219 tests passed in175.006s. Django check and migration dry-run passed. No schema change.
