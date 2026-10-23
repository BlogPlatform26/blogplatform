# Phase102w: phone discovery content before supporting sidebars

Baseline817ac72. Home and search receive a route-scoped discovery-layout-row class. Below768px the main content column has order:-1, placing results before notices/support. Tablet/desktop and blog-theme routes keep their existing order. This changes visual flex order; source/keyboard order remains unchanged and is not certified as a complete accessibility workflow.

24 after states (six102v guest routes x320/390/768/1440) all have document overflow0. All12 phone states put content first, with measured column rectangles nonoverlapping. At320 populated search content beginsy114.188 instead of652.188,538px earlier. Support remains rendered below it. Search scope users/posts switches safely preserveq=qa. Phone390 screenshot z/outputs/phase102w-search-phone.png is the initial viewport, not a full-page image.

All sampled rectangles in12 tablet/desktop states are identical to102v. Fill samples match except home post-title H4 transparent RGB components: alpha0 remains0 in both cases; child anchors match. No color/background changes were implemented, and no new photo or composed-contrast acceptance is claimed. Existing inactive filter contrast, following-owner/populated featured/tags, long unbroken content, keyboard ordering and U12 controls remain open.

Initial external stylesheet candidate did not appear in browser computed order. It was removed; the final scoped template rule was measured only after restarting the isolated8017 server. Final raw evidence is phase102w_measurements.json. Check/migration pass and216 tests pass63.659s. Original DB/media/port8000 untouched. No37-design re-audit.
