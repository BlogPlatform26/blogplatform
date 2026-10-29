# Support retry preserves submitted content

Previously a whitespace-only title passed native required validation, failed server validation and redirected to a blank form, losing the message. Invalid submissions now render a bound retry form (HTTP400) with field errors and the original message, contact and category. Correcting the title submits through the same endpoint. Return navigation is constrained to the current host and avoids redirecting to the POST-only endpoint.

Browser proof: native390 submission with whitespace title and qa-retry-retained-20261029 message displayed the specific title error while preserving the message and Pitanje category. Correcting only the title to qa-retry-corrected-20261029 produced Pitanje je poslano. QA used .qa100e.sqlite3 and explicit in-memory mail; no SMTP delivery claimed.

At320/390/768/1440 retry fields are223.333/293.333/550.75/606.667px wide, controls48px tall and textarea133.333px. Document/control-local excess0. Raw geometry/fill/background: C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-support/retry-browser.json. A new standalone retry card intentionally replaces the old error redirect at every width. Existing normal support form styles are unchanged; its narrow tablet layout remains open. Screenshot support-retry-phone.png is an inspected390 viewport capture, not full page.

Six targeted tests passed1.292s, including retained invalid input and corrected successful save. Check and migration check passed. Full suite result recorded below. Remaining support acceptance: normal tablet form usability, complete keyboard traversal, other invalid field combinations in browser. No blanket U12 closure.

Full suite:237 tests passed94.920s (raw u12-support/retry-suite.txt). Database readback confirmed synthetic report id2 preserves the original message and question category after correction. git diff --check passed.
