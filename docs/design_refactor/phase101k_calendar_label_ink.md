# Phase101k — confirmed weekday and phone archive label contrast

## Scope and cause
Actual-fill audit101f found small weekday text below4.5:1: dark/right4.217, classic/right4.074, Simple pattern/image3.362 and retro3.247/3.791. Fixed palette weekday inks are now #aaa dark, #555 classic and #675e55 Simple, including the separate right-hand retro calendar. No dimensions changed.

On phones below576px, Vodopad/Planine/Nebeski/Iznad weekday alpha is removed while retaining each theme's RGB ink. Planine/Nebeski phone archive titles use darker matching ink only when box_title_color equals the exact factory value. Nonfactory #123456 guard renders exclude the archive override (template-level evidence).

## Browser evidence
88 before/after blog/detail states:11 themes ×320/390/768/1440×2. Every measured rectangle unchanged; zero document overflow. This does not certify existing layouts. Both retro calendars measured; second initially retained a separate low-contrast rule, now corrected and remeasured.

Effective actual-fill weekday minima: dark/right8.128, classic/right6.783, Simple pattern/image6.293, retro6.076; phone Vodopad7.718, Planine5.308, Nebeski10.235, Iznad5.309. Phone archive Planine7.171 and Nebeski7.522. The four photographic themes' tablet/desktop labels are unchanged; photo-null remains unresolved.

All11 safe post-open clicks reached the expected existing post. Bootstrap and real ancestor surfaces recorded in raw data. Screenshot outputs/phase101k-nebeski-labels.png inspected. Month/arrow photographic evidence is not claimed closed. Calendar layout, dense-week behavior, other text and control targets are not newly certified by this color-only phase.

Final Django check and migration dry-run pass; all214 tests pass in49.875s after the second retro calendar correction. Original repository/database/media/port8000 untouched. Commit/push only design-refactor.
