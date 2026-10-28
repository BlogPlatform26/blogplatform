# Phase103t: reset workflow server coverage

This phase adds tests only; application templates, CSS, routes and runtime behavior are unchanged from2c30627.

Two integration tests use temporary Django test-database users and an explicitly overridden in-memory email backend. No SMTP delivery, persistent QA-account update, browser credential entry or production data access occurs.

The success test requests a reset through the public endpoint, checks the done redirect and single intended recipient, follows the link extracted from the generated email, and checks validlink. A mismatched confirmation returns field errors in the public template without changing the password hash. Matching passwords redirect to complete, persist the new hash, reject the old password and permit Django client login with the new password. A fresh client cannot reuse the original token.

The expiration test fixes issuance time and advances validation to61seconds against a60second timeout. The public invalid-link page offers retry and the original password remains valid. Time mocking is confined to the test; application timeout policy is unchanged.

Targeted module:7 tests passed in1.865s. Full suite:231 tests passed in64.047s. Check and migration check pass. Raw full-suite log: z/work/u03-valid-token/phase103t-tests.txt.

These are server integration results, not browser success-flow acceptance, email deliverability evidence, or new layout/contrast coverage. No new screenshots or viewport measurements were needed for a tests-only change. Browser password-entry completion, expired-token browser state, reset-complete login target and the rest of the acceptance ledger remain open.
