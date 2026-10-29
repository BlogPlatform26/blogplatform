# Home tablet columns and support form usability

The home page previously squeezed support fields into a quarter-width sidebar:94.016px at768 and146.859px at991 in this browser run. Scoped CSS at768–991.98 now places the main feed in a full row and the two supporting columns in half-width columns below it. Fields measure246.047/351.734px. No change is applied to phone or >=992 desktop rules, search, or designed blog/detail routes.

Before/after320/390/768/991/1440: document excess0. Raw z/work/u12-support/tablet-before.json and tablet-after.json retain geometry, local excess, actual fill/background. Phone support widths223/293 and desktop254 unchanged; desktop support coordinates/styles unchanged. Main feed heights and phone support y differ in rapid resize samples, consistent with previously observed transitions; these samples are NOT proof of identical whole-page geometry. CSS scope and unaffected sampled control sizes/colors are the preservation evidence; no blanket pixel-equality claim.

At768/991 all three column rectangles have no intersections (tablet-checks.json). Native Tab from title visits message, email, submit. Native next-page link at768 reaches /?page=2&filter=featured and exposes previous navigation. No form submit/email/database mutation. Screenshot outputs/support-tablet-layout.png is an inspected scrolled768 viewport showing the wider form and adjacent supporting column, not the entire page.

This closes the recorded home tablet field-width defect. Tablet small control heights, full keyboard traversal and equivalent search support layout remain open; do not claim universal support acceptance. Previous support retry and server workflow remain closed. Full suite result follows.

Validation:237 tests57.491s passed; Django check, migration drift check and git diff --check passed. Raw u12-support/tablet-suite.txt.
