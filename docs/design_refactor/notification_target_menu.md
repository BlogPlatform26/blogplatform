# Notification mark-all target

Scoped min-height/min-width48px on the full-list mark-all button. Paired320/390/768/1440: heights52/52/31/31 become52/52/48/48. Document overflow remains0. Tablet/desktop button height intentionally changes; no blanket geometry identity claim. Raw z/work/notification-target-before.json and notification-target-after.json. Inspected outputs/notification-target-desktop.png is a1440 viewport.

Phone keyboard: Enter opens both notification and account menus. Account Down focuses Moj blog; Escape closes and restores its toggle. Notification Down stayed on the toggle, while Escape closes. Raw notification-menu-keyboard.json. Notification menu Tab traversal is NOT verified yet. Browser runtime became unavailable on continuation; tab13 logout/close/viewport reset could not be confirmed. QA server37392 stopped; earlier35287 stopped. Do not infer whole U11 closure.

242 tests68.604s passed (notification-target-suite.txt), check clean, migration dry-run no changes. Existing list mark-all native/readback coverage is retained; no new valid mutation attempted in this target pass.

## Browser recovery and menu Tab follow-up

Browser access recovered after resetting the automation runtime. Existing tab13 at1440 retained the synthetic session. Enter opened the notification dropdown; eight native Tabs reached Vidi sve, all six notification links, then the account toggle. Raw z/work/notification-menu-tab.json. Thus ArrowDown staying on the toggle does not prevent keyboard access to these links. This is an all-read desktop menu state; unread mark-read and phone expanded-menu variants are not inferred from it.

Synthetic logout confirmed by POST/logout302 and home GET200; tab13 closed, viewport reset, QA server93090 stopped. This supersedes the earlier unconfirmed cleanup. No application changes or suite rerun in this follow-up; latest242 tests68.604s remains valid for the target change.
