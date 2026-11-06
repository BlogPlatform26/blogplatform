# Author private-answer browser follow-up

Validated on 2026-11-06 against 87e4401 in isolated .qa100e.sqlite3, localhost:8017. No application change.

Owner qa103g_empty_owner unchecked public visibility for existing synthetic question 1 and saved through the settings form. The resulting page showed the save confirmation and Privatno za pošiljatelja. The answer text remained Synthetic owner public answer (the text itself is not a visibility flag).

After native logout, the guest author page contained neither the question nor answer. After native login as its sender qa102y_reader, the same author page displayed both under Tvoja privatna pitanja i odgovori and Privatno. This proves sender/guest browser visibility for the saved private state. The unrelated authenticated viewer and clear-answer transitions remain browser follow-ups; their existing server tests are not new browser proof.

Raw DOM text: C:/Users/mario/Documents/Codex/2026-10-10/z/work/author-private-browser.json.
Viewport screenshot: C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/author-private-sender.png, inspected. Default desktop viewport, not a whole-page capture; the private section starts near the bottom and the answer itself is below the captured area. DOM text supplies answer visibility proof, not the screenshot.

No new layout, contrast, four-width, or complete U04 acceptance claim. No suite rerun for this documentation-only follow-up; latest application verification remains 249 tests / 73.483s plus check and migration check from owner_answer_controls.md. Both QA sessions logged out; tab 1 closed; no viewport override introduced; server 43331 stopped. Synthetic question 1 remains private with its existing answer. No SMTP or production data touched.
