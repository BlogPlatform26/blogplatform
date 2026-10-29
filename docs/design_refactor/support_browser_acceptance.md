# Support browser submission evidence and remaining defect

At commit39ed9b2 a dedicated localhost8017 server used .qa100e.sqlite3 and an explicit django.core.mail.backends.locmem.EmailBackend override. Native browser form submission at390px created a synthetic question titled qa-support-browser-20261029 with no contact email. The redirected page visibly displayed Pitanje je poslano. No external SMTP used.

Success and server-validation error alerts were measured at320/390/768/1440: document and alert-local excess0. Success actual fill rgb(10,54,34), opaque background rgb(209,231,221), height57.333. Error fill rgb(33,37,41), transparent background with visually white page; height81.333 on phones,57.333 on larger widths. Raw: z/work/u12-support/browser-success.json and browser-error.json. Screens support-success-phone.png and support-error-phone.png are inspected390 viewport captures, not whole-page images.

CONFIRMED OPEN DEFECT: title containing only spaces passes native required validation but fails server validation. Redirect displays generic Nije poslano feedback and clears the previously supplied message. Browser measured retainedMessage empty at all widths after the single failing submission. Preserve submitted values and show actionable field errors before accepting this workflow. Tablet narrow fields and complete keyboard traversal remain open. No application code changes in this evidence batch; latest suite236 tests82.631s from preceding server test commit.

Database verification: synthetic report id1 is question with expected title and empty email; invalid whitespace-title submission saved zero reports. QA server stopped, temporary tab closed, viewport reset.
