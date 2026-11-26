# Box settings containment and long-content workflow

Recorded on 2026-11-26, based on HEAD 4bea6dd. Full all37/U01-U12 acceptance remains incomplete.

## Repairs and intended desktop effects

The settings column has zero right padding, so the Bootstrap row's negative right gutter produced 7px document overflow at320/390/768/1440. Set that row's right margin to0. At1440 this intentionally reduces the row by7.198px and each side card by3.604px; the second card shifts left3.604px. The editor and its normal controls retain desktop geometry. Fonts, foregrounds, fills, images and sampled ancestor backing remain unchanged across all95 sampled nodes at each width.

At widths through991.98px, add/title/position/save/delete/box-link targets and the drag handle have48px height (handle48px width). Title/select were32px, add26.042px, save/delete25.885px, link40.865px and handle26x34px. Button spacing becomes8px and actions can wrap. Desktop targets retain their prior dimensions. The title and position labels now identify their controls.

An80-character unbroken title exposed a grid item minimum width and flex heading minimum width defect. Before this additional repair, document excess was217px at320 and147px at390; the side-card content also exceeded its clipped boundary. min-width:0 on the grid item and min-width:0/overflow-wrap:anywhere on the editor heading children restore containment. Long titles intentionally wrap on any width when necessary. The list title keeps its existing ellipsis; the full title remains readable in the editor heading and editable input.

The same workflow found that CKEditor displayed1200 characters but the server rejected the input because &nbsp; was counted as literal markup characters. UserBoxForm now decodes HTML entities after stripping actual tags, then applies its existing whitespace normalization. Escaped text such as &lt;b&gt; remains visible text for the limit. Sanitized stored HTML is unchanged by this counting fix. This behavior applies on desktop too.

## Browser proof

Paired normal snapshots at320/390/768/1440:95nodes each; document and sampled local excess0 after the repair. All sampled fonts/colors/fills/images/backing match. Mobile/tablet vertical shifts follow enlarged targets; desktop11 changed rectangle properties are limited to the row/cards and their contents. See box-settings-final-comparison.json for exact values rather than claiming complete desktop geometry identity.

Native title-Tab reaches the editor's line-spacing select (not directly its editing area). Position-Tab reaches Save and the next Tab reaches Delete at all four widths;12 recorded focus-visible states. This records navigation, not numerical focus-contrast acceptance. The CKEditor toolbar's30px line-spacing control is outside the enlarged main-control claim.

At390, an80-character unbroken title and75 repetitions of LongContentWord plus a space were submitted with positionright. The initial1200-character editor input was rejected before the entity repair, preserving the draft. Resubmitting the same draft after restart succeeded. Reload retained the title/content/right position; normalized custom counter1199 and CKEditor counter1200 differ by trailing whitespace. Four-width long-content samples have document excess0 and no sampled element outside the viewport. Intentional local excess remains only in the ellipsized list title and horizontally scrollable single-line title input; it is not page overflow.

Enter on Delete opened the confirmation with the long title; document excess0 at390. Enter on Odustani returned to settings. Opening Boxes retained the long title andright position. The synthetic box1 was then restored through the UI and reloaded: title Synthetic box edited, content Synthetic edited content, positionleft. No deletion occurred. No new box was created.

Inspected screenshots: box-settings-final320.png, box-settings-final390.png, box-settings-final768.png, box-settings-final1440.png and box-settings-long390.png. These are scrolled900px-high viewports, not whole-page acceptance. At320/390/768 the save/delete area is visible without overlap; the1440 screenshot shows both side cards and editor.

## Evidence and remaining work

Raw files live in C:/Users/mario/Documents/Codex/2026-10-10/z/work/: box-settings-before.json, box-settings-after.json, box-settings-comparison.json (intermediate normal), box-settings-final.json, box-settings-final-comparison.json (authoritative final normal), box-settings-long.json (long-title failure before additional containment), box-settings-long-final.json, box-settings-keyboard.json, box-settings-actions.json, box-length-before.txt, box-length-after.txt, box-settings-final-suite.txt. Screenshots live in the sibling outputs directory.

The two new rendered-length tests reproduce three failing valid-entity cases before the fix; after the fix all8 box workflow tests pass in2.368s. Boundary tests accept1200 ampersands/escaped visible tag characters and reject1201 ampersands or1203 escaped visible characters. Full suite result is recorded separately below.

QA used .qa100e.sqlite3, locmem email and8017. Owner logged out (guest login link verified), tab24 closed, viewport reset and own server45379 stopped with no8017listener observed. Original repository/database/media/8000 were not used.

Remaining groupedU06: drag/reorder autosave and readback, full-capacity UI states, editor toolbar accessibility/targets and numerical focus/contrast; wider full37/U01-U12 scope remains in the matrix. Do not repeat recorded recovery or long-content save/cancel proofs without a regression.

Final validation2026-11-26:261tests84.208s pass; Django check clean; makemigrations --check --dry-run reports no changes. Raw box-settings-final-suite.txt.
