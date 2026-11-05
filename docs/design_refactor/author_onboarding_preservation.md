# Author onboarding preserves question settings

The onboarding wizard omitted the questions checkbox but bound the full author ModelForm. Validation changed its instance to false before the old restoration assignments ran. Saving a biography therefore disabled existing reader questions.

The view now snapshots the four settings managed outside onboarding before validation and restores those values before saving. No template, CSS, font or color changes.

Regression: test_author_onboarding_preservation failed before the fix with questions True -> False; contact/social/website stayed unchanged in that reproduction. It passes after the fix. Four author-journey tests also cover question validation and persistence, owner/disabled/guest rejection, onboarding skip, invalid date and valid biography save.

Validation: check and migration check green; 247 tests passed in 52.030s. Raw files under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: author-onboarding-regression.txt, author-onboarding-suite.txt, author-onboarding-before.json, author-onboarding-after.json, author-onboarding-readback.txt.

Browser: initial wizard controls sampled at 320/390/768/1440 before/after have identical recorded rectangles/font/actual text fill/background/local overflow; document overflow zero. These samples are not full wizard or public-author acceptance. At 390, synthetic owner2673 qa103g_empty_owner advanced through all three steps and submitted with native Enter. Success message and redirect appeared. Database readback confirmed the saved synthetic biography and questions=True after preparing that test setting. Only isolated .qa100e.sqlite3 was used; no email or credential changes.

Screenshot: outputs/author-onboarding-success-phone.png is an inspected 390px viewport, not a full-page capture. It shows the save confirmation; database evidence establishes preservation.

Logged out and closed tab16; viewport reset; QA server stopped. The earlier failed-load tab15 contained no login. Public author question browser workflow, full keyboard/error presentation and remaining U04 acceptance remain open.
