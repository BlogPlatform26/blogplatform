# Author answer privacy transitions

Browser evidence collected 2026-11-06 against 87e4401/74dab49, isolated .qa100e.sqlite3 on localhost8017. No application changes.

Native login as unrelated synthetic viewer2681 (qa_u04_unrelated_20261106) showed the author biography/question form but neither question1 nor its private answer. Combined with author_private_visibility_browser.md, sender/guest/unrelated-viewer separation is verified for this fixture.

Owner2673 then replaced the answer with three spaces, checked public visibility and saved. The returned page showed confirmation, answered0/unanswered1, an empty answer and unchecked public visibility. Guest view after logout contained neither question nor answer. Database readback confirms answer='', is_public=False, answered_at=None; question1 remains owned by2673 with sender2672.

Raw evidence: z/work/author-privacy-transitions.json and author-clear-readback.txt. Inspected z/outputs/author-cleared-answer.png is a scrolled default desktop viewport, not a whole-page capture; it shows empty answer, unchecked public flag and unanswered status. No new four-width or contrast claim.

Both sessions logged out, tab3 closed, server63727 stopped; no viewport override introduced. Synthetic viewer2681 remains available. Question1 is now unanswered/private. No SMTP or production mutation. No suite rerun for documentation-only evidence; last application suite249 tests73.483s/check/migration green belongs to owner_answer_controls.md. Full U04 long-content and keyboard/error presentation remain open.

Documentation was initially blocked by automatic approval review exhausting its usage allowance; the write did not execute. After capacity recovered, the saved evidence was re-read before this document was written.
