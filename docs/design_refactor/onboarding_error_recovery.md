# Onboarding error recovery

Fixes the hidden invalid-date state reproduced in onboarding_hidden_error_baseline.md. The wizard now renders each field error and non-field errors. On an invalid server response it opens the step containing the first aria-invalid field and focuses that field. Next/back navigation focuses the first control in the destination step, avoiding loss of keyboard position when the old step is hidden.

Four paired clean initial states320/390/768/1440 have identical sampled heading/info/textarea/button rectangles, font, actual fill and background; document overflow0. Four rendered invalid states show step2, retained date10000-01-01, focus id_author_birth_date, associated error id_author_birth_date_error, document/error-local overflow0. Native390 Enter transitions focus full_name then hobbies; invalid submit returns to date. Clearing the optional date and Enter Spremi succeeds and redirects to the owner's blog with confirmation. Database readback retains biography and questions=True/date=None.

Raw z/work/wizard-before.json, wizard-after.json, wizard-errors.json, wizard-readback.txt, wizard-targeted.txt, wizard-suite.txt. Inspected outputs/wizard-error-phone.png is a scrolled390 viewport showing step2 and its error, not a full page. Existing styling is unchanged; error content intentionally adds height.

Targeted6 tests1.015s passed with additional rendered field-error/draft assertions. Full suite: 250 tests passed in 54.843s. Check clean; migration check found no changes. QA servers27651/12574 stopped; logout/tab7close/viewport reset confirmed. No email or production mutation. Complete all-field Tab traversal, native constraint failures in hidden steps, skip browser workflow and owner long-content remain separate acceptance work.
