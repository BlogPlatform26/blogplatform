# Phase101o - Sumska/Polarna phone post headers and comment wrapping

The existing <=575.98px header and long-comment-word wrapping rule excluded these two designs. Add them to its template condition, placing the title above the date and permitting individual comment words to wrap. No palette or desktop rules changed.

## Evidence
16 standard blog/detail states at320/390/768/1440 with Bootstrap and two comments. Before uses101n current measurements, with original faults documented101l. Post-title and comment local overflow now0 in every state (before320 title68/71, comments2/3). Document overflow0 for these standard fixtures only. Eight phone header checks show16px separation between title bottom and date top, with no overlap. Safe open77/78 succeeds. Screenshot outputs/phase101o-polarna-phone.png inspected.

All measured tablet/desktop static rectangles match101n; date-sensitive active/today calendar rectangles excluded because the real current date changed. Every measured CSS color and actual text fill matches before; existing local contrast surfaces are preserved. No new photographic contrast claim is made.

Dense calendar overflow, tablet target sizing, archive/active-day contrast and other open scope remain. This is not a whole-theme pass. Raw before/after, header and safe-navigation evidence is stored in phase101o_phone_wrapping_measurements.json.

Django check and migration dry-run pass; all214 tests pass in79.169s.
