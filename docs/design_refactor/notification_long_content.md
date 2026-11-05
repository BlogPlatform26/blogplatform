# Long notification containment and phone keyboard evidence

The full notification list now inherits overflow-wrap:anywhere from its scoped container. QA notification3 uses existing synthetic sender2671/post221 and recipient2672. Its unbroken title previously exceeded the row by1195/1125/1172/852px at320/390/768/1440 despite document overflow0. After the change every sampled row has local excess0, and document overflow remains0. The ordinary factory sender also had5px local excess at320; it now wraps within the row.

Actual sampled row font, fill and background are unchanged at all four widths. Row heights intentionally grow to expose the whole title, including desktop; this is not identical geometry. Raw before/after: z/work/notification-long-before.json and notification-long-after.json.

Native Enter at390 on notification3 reaches canonical post221; returning displays Pročitano. Native Tab from the top reaches logo, search, notifications menu, account menu, mark-all, then all three notification rows before support. Raw notification-keyboard-phone.json. This verifies this phone sequence, not all keyboard/menu states or other widths. Existing mark-all and recipient-isolation evidence remains valid.

Inspected z/outputs/notification-long-phone.png is a390 viewport showing the complete wrapped title and all three rows; it is not a full-page capture or pixel contrast proof. Reader logged out, tab10 closed, viewport reset, QA servers13418/67070 stopped. No real messages or credentials changed. Initial native login attempt failed; verified existing synthetic password and locator fill succeeded, without a credential reset.

242 tests passed56.686s (z/work/notification-long-suite.txt); check and migration dry-run passed. Remaining U11: tablet containing-width usability, desktop targets, full keyboard variants, actual child contrast/overlap and representative follow/comment/mention browser destinations. No whole U11 closure.
