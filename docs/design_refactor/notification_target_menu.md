# Notification mark-all target

Scoped min-height/min-width48px on the full-list mark-all button. Paired320/390/768/1440: heights52/52/31/31 become52/52/48/48. Document overflow remains0. Tablet/desktop button height intentionally changes; no blanket geometry identity claim. Raw z/work/notification-target-before.json and notification-target-after.json. Inspected outputs/notification-target-desktop.png is a1440 viewport.

Phone keyboard: Enter opens both notification and account menus. Account Down focuses Moj blog; Escape closes and restores its toggle. Notification Down stayed on the toggle, while Escape closes. Raw notification-menu-keyboard.json. Notification menu Tab traversal is NOT verified yet. Browser runtime became unavailable on continuation; tab13 logout/close/viewport reset could not be confirmed. QA server37392 stopped; earlier35287 stopped. Do not infer whole U11 closure.

242 tests68.604s passed (notification-target-suite.txt), check clean, migration dry-run no changes. Existing list mark-all native/readback coverage is retained; no new valid mutation attempted in this target pass.
