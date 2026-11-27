# Box layout save and movement acceptance

Verified 2026-11-26/27 against baseline 318ad64, synthetic owner 2673 only. This closes the recorded U06 layout movement/save/recovery/full-capacity work, not the whole U06 journey or all 37/U01-U12 objective.

## Problem and change

The previous AJAX path accepted a followed HTML redirect as success, including validation failures. Multiple individual updates could partially persist if a later update failed. Drag previews remained in the DOM after an outside drop, and reordering had no non-drag control.

The endpoint now validates the complete owned ID set, positions, duplicates and side limits before atomic updates, returns explicit JSON success with the acknowledged layout, and keeps the existing HTML redirect path. Invalid/stale requests return 400/409 JSON errors. The client serializes saves, retains the latest pending layout, verifies the acknowledgement, shows a retry button on failure and warns before leaving with pending/unsaved layout. Retry keyboard focus moves to the live status, then Tab reaches the title field. This is page-local queueing, not a multi-tab conflict-resolution claim.

Each box has a native select for up/down, movement to an available side, or swapping with a chosen box when the other side is full. Existing native drag remains. Cancelled drag restores the initial ordering. Counts, item badges and active editor side update with movement; unrelated reordering preserves an unsaved editor position choice.

## Paired visual evidence

CSS viewports 320/390/768/1440, height 900. Six synthetic boxes, same initial order on both sides. The first temporary baseline expired during inactivity; it was regenerated from the exact three HEAD frontend files in the single authorized worktree, with the draft backed up and restored byte-for-byte and the QA server restarted. No second repository was used.

For each width, 119 existing sampled nodes retain font, foreground, background/image/backing, x and width. Document and sampled local overflow are 0. Added selects measure 48px high. Four partial-capacity measurements show no select/link intersections. Actual ancestor chains confirm opaque white beneath select text and focus, and white behind save/error status.

Intentional desktop changes: each box card gains 55.1979px in height for the new control; each three-box side gains 165.5938px, with resulting vertical movement of following content. Existing editor control dimensions are preserved. New keyboard focus outlines and save-status colors apply to desktop too. No claim of unchanged overall desktop height.

Measured contrast against opaque white: select text/focus #084298: 9.3624:1; select border #64748b: 4.7588:1; success #146c43: 6.4500:1; error #b02a37: 6.4968:1. Retry outline-button normal/focused white-blue pair 4.5007827874:1. CSS outline 3px computes 2.66667px in this browser environment, with 2px offset; all four focus captures were inspected for separation/clipping.

## Native workflows

- At 390, move down, explicit success, reload readback; swap into the other full side, success and reload readback. Native Space/End/Enter on the select performs a full-side swap and retains select focus.
- At 1440, native pointer drag reorders, swaps between full sides, and dropping outside cancels without changing the final ordering. These three outputs are transcribed with provenance in box-layout-drag-observations.json because the temporary detailed flow file expired; they are not newly sampled after the final retry-focus-only refinement.
- Stop own QA server, move a box, observe error and retained DOM with retry at all four widths. Restart, Enter retry, success and reload preserve the selected order. Final version repeats recovery at 390 and confirms focused status followed by Tab to id_title.
- An attempted reload with an unsaved offline layout left the page and draft intact. getJsDialog returned undefined: this is not evidence of a visually inspected browser confirmation or every in-flight timing race.
- At 390 with 2+2 boxes, an unsaved editor side choice survives another box's reorder; moving into the third slot persists after reload. Header counts agree with 1/3 and3/3 at all four widths.
- Move the remaining original box into an empty left side; right becomes empty. Restore/read back original box 1 title/content/left/order 0. Temporary IDs 2-6 removed with owner/title guards.

## Validation and durable evidence

Five regression tests cover reorder/full-side swap acknowledgement, invalid/stale/foreign/duplicate/full-side/malformed positions and IDs without writes, malformed JSON, HTML active-box redirect and rollback on second-update failure. Pre-fix failures: box-layout-tests-before.txt. Final full suite: 266 tests in 84.741s, Django check clean, no pending migrations: box-layout-final-suite.txt. Initial intermediate suite: 266 tests in 84.931s is superseded.

Raw files under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: box-layout-before.json, box-layout-final.json, box-layout-final-comparison.json, box-layout-controls.json, box-layout-contrast.json, box-layout-error.json, box-layout-flow.json, box-layout-resumed-flow.json, box-layout-drag-observations.json, box-layout-fixture.json. Earlier after/comparison and draft-backup files are intermediate, not final application evidence.

Inspected scrolled viewport images under z/outputs/: box-layout-final320/390/768/1440.png, box-layout-retry320/390/768/1440.png, box-layout-restored390.png. Width labels refer to CSS viewport, not a claim of 1:1 raster pixels.

QA server 34581 stopped; 8017 listener absent. Owner logout verified through guest Prijava/Registracija; tab 26 closed and viewport override reset. Original repository/database/media/8000 untouched. No real email.

## Remaining work

U06 editor toolbar keyboard/features, targets and numerical focus/contrast remain open. This change does not accept the CKEditor toolbar or every stale-session/multi-tab interaction. Continue the other full37 design and U01-U12 matrix requirements without repeating the closed layout/long-content/recovery work.
