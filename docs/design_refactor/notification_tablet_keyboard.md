# Notification tablet layout and keyboard sequence

Scoped notifications-only768-991.98 rule gives main content100% width and two supporting columns50% underneath. Before, tablet list competed with narrow sidebars; after main width608.094 at768 and819.469 at991 (previously half those widths). Screenshot outputs/notification-tablet.png is an inspected768 viewport showing the readable list and start of supporting columns. Tablet arrangement intentionally changes.

Five paired320/390/768/991/1440 states: document and every sampled local overflow0. Phone320/390 and desktop1440 complete sampled objects (rectangles/fonts/fill/background/local) identical before/after. Tablet supporting columns start at the main bottom and meet horizontally without intersection. Raw z/work/notification-tablet-before.json and notification-tablet-after.json.

At320/390/768/1440 native Tab from page start visits four navbar controls, mark-all, all six notification rows, then support. Raw notification-four-width-tab.json includes focus geometry/outline/shadow. This closes normal main-list traversal, not every expanded dropdown or search interaction. Mark-all remains31px when its label fits one line on tablet/desktop; target enlargement is still open and was not silently changed in this layout fix.

242 tests59.326s, check clean, migration dry-run no changes; raw notification-tablet-suite.txt. Reader logged out, tab12 closed, viewport reset; servers27390/23384 stopped. No persistent content or mail mutation. U11 still retains larger-screen target and expanded-menu keyboard acceptance.
