# Box editor controls and formatting persistence

Verified 2026-11-27 on design-refactor, based on a6a7801. This closes the recorded main-toolbar target/focus defect and heading/spacing save regression, not every U06 popup or the full 37-design/U01-U12 objective.

## Changes and scope

The add, direct-edit and settings box forms share a scoped toolbar stylesheet. Main toolbar buttons, split-list arrows and the settings line-spacing select are at least 48px wide/high through 991.98px. Previously most buttons were 29.896px square and split arrows 16px wide. Keyboard focus uses an inset opaque #084298 outline. Dropdown/palette interiors retain their existing styles and require separate acceptance.

Browser feature checks found heading text-align and line-height were stripped on save. The shared HTML sanitizer now permits its existing safe style property list on headings, list items and blockquotes, and includes line-height. Scripts, event handlers and non-allowed CSS properties remain removed. This also preserves supported block formatting when other callers use the same sanitizer; it does not alter already stored content.

Intentional desktop changes: keyboard focus indicator and preservation of user-selected heading/spacing formatting after save. No desktop toolbar target/layout change. Mobile/tablet toolbar height grows to make space for the larger controls; content below moves vertically.

## Paired browser evidence

Twelve states: add, direct edit of box1, settings edit of box1, each at CSS viewport 320/390/768/1440, height900. Samples include actual SVG path fill, text fill, fonts, foreground, background and three ancestor backings. 79 nodes per add/direct state,81 per settings state. All sampled styles unchanged. Document and sampled local overflow0; no intersecting main buttons/selects; all main controls meet48px at320/390/768. Maximum desktop rectangle difference0.0000382px (floating-point measurement), with unchanged toolbar heights.

Settings toolbar heights before/after:320 234.927/391.146;390 159.458/279.563;768 84.083/112.188;1440 46.396/46.396. Add/direct:320 188.531/446.333;390 150.844/278.958;768 188.531/334.750;1440 75.469/75.469. Standalone forms have narrower content at768 than settings; their measured wrapping is retained explicitly, not equated with the settings layout.

Normal primary ink #333 on white contrast12.635; focus #084298 on white9.362. Active Bold path #2977ff on #dbecff3.371 (icon); focus on this active backing7.782. Disabled controls are not counted as enabled-control contrast passes. 72 native Right-arrow focus states across four widths had visible opaque outlines. Final stylesheet restricts the same outline to main controls; representative final four-width captures confirm it, plus direct/add390 and title Tab to line-spacing select390.

Screenshots inspected: box-editor-final320/390/768/1440.png (settings, scrolled viewport), box-editor-direct390.png and box-editor-add390.png. These are viewport evidence, not full-page screenshots or universal popup acceptance.

## Actual editing and persistence

At390, native UI actions applied bold/italic/underline/strike, font18px/Georgia, foreground/background colors, heading, center alignment and a localhost link. Undo removes the link; redo restores it. Direct save and settings reload retained inline formatting/link but initially lost heading alignment. Remove Format removed inline styles; quote and bullet/numbered lists changed the rendered HTML. Line spacing2 initially disappeared after settings save/reload.

After the sanitizer fix, settings save/reload retains both line-height:2 and text-align:center on the heading inside the numbered quote. A second list item can indent into a nested list and outdent back to a sibling. The attempted first-item indent was unavailable; it was not reported as a successful action. Basic feature evidence does not cover every dropdown option, picker dialog or keyboard-only feature combination.

The only modified fixture was synthetic owner2673 box1. Original title, left/order0 and content <p>Synthetic edited content</p> restored with owner/title/position guards and browser readback. No new box remains. Owner logged out (guest Prijava/Registracija confirmed), tab27 closed, viewport reset. Own server45508 stopped;8017 listener absent. Earlier own servers22352/82689/23932 stopped for template reloads. Locmem email only; original repo/database/media/8000 untouched.

## Tests and evidence files

New regression test reproduces lost heading alignment/spacing before the fix, then checks saved formatting and removal of script/onclick/position CSS. Targeted9 tests pass. Full267 tests pass in59.783s; Django check clean, makemigrations --check --dry-run reports no changes. Existing staticfiles-directory warning remains; it did not fail checks.

Raw under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: box-editor-before.json, box-editor-focus-before.json, box-editor-final.json, box-editor-comparison.json, box-editor-focus-after.json, box-editor-final-focus.json, box-editor-contrast.json, box-editor-contrast-ratios.json, box-editor-flow.json, box-editor-fixture.json, box-editor-test-before.txt, box-editor-test-after.txt, box-editor-suite.txt. box-editor-after.json is the intermediate main-toolbar version; final measurements supersede it. Screenshots are in z/outputs/ with names above.

## Next U06 work

Verify dropdown/palette/link-dialog containment, target sizes and focus, plus standalone add/direct main-field/submit targets (390 screenshots still show compact controls). The settings main-field targets and existing layout movement/recovery closures are retained. U06 stays PARTIAL until these remaining controls and relevant keyboard paths are proven. Continue the full other U01-U12 and photographic/calendar requirements without restarting the37-design initial tour.
