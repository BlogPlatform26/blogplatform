# Author settings validation retry

Invalid profile submissions redirected to a fresh form, discarding the draft. A native390 browser submission of year10000 with a changed biography reproduced the loss. The saved database biography was not changed by the invalid request.

The handler now redirects only after success. Invalid submissions render the bound form. Every author field renders its Django error list, and the profile form renders non-field errors. Django associates the date error through aria-invalid=true and aria-describedby=id_author_birth_date_error.

Four paired clean states320/390/768/1440: all18 sampled fields have identical geometry, fonts, actual fill and background; document overflow0. Four invalid states retain biography/date with document/error-local overflow0. Error text intentionally adds vertical space. Native390 correction (clear optional date) and Enter on save persisted the retained biography. Database readback confirms questions=True and date=None. Synthetic owner2673 now has biography Synthetic retry draft must survive.

Regression covers invalid-request database preservation, bound biography/contact, rendered field error and corrected resubmission persistence. Initial red failed302 versus200; targeted green1 test0.208s. Final250 tests64.172s passed, Django check clean, makemigrations --check --dry-run found no changes. No redundant rerun after recovering the completed process56163.

Raw z/work/author-retry-before.json, author-retry-after.json, author-retry-baseline-error.json, author-retry-errors.json, author-retry-readback.txt and author-settings-retry-{red,green,suite}.txt. Inspected z/outputs/author-retry-phone.png is a scrolled390 viewport showing retained biography and date error, not a whole page.

QA servers40306/70147 stopped; owner logged out, tab5 closed, viewport reset. No SMTP or production mutation. This fixes retry/error association; complete keyboard traversal, other error combinations and owner long-content remain separate acceptance requirements. Documentation write was temporarily rejected because automatic approval review reached its usage limit, then resumed after recovery; no credit reset used.
