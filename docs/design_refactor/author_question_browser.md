# Reader question browser workflow

On 2026-11-05 the existing synthetic reader2672 qa102y_reader visited author2673 qa103g_empty_owner, whose questions setting was preserved by 584a6a0.

At 390px: empty Enter submission produced native valueMissing; two characters reached the server and displayed “Pitanje mora imati barem 3 znaka.” The redirected invalid form was empty. A valid synthetic question was entered, Tab focused Pošalji pitanje, and native Enter submitted. The success message appeared together with the sender's private pending question. Database readback confirmed question1, author2673, sender2672, is_public=False and empty answer. After logout, the same author page exposed neither the private question nor its form, and offered login instead. No email was sent.

Baseline at320/390/768/1440: document overflow0, visible textarea/button local overflow0. Raw author-question-baseline.json also includes hidden zero-size header controls; these are not visible target samples. Textarea50px high, submit31px at all four widths. AX textarea was unnamed (id_question only). These target/name issues remain open, along with full keyboard traversal, owner answer/publication and other-viewer privacy acceptance. No claim of complete U04 closure.

Raw C:/Users/mario/Documents/Codex/2026-10-10/z/work/author-question-baseline.json, author-question-readback.txt and author-question-guest.json. Inspected outputs/author-question-success-phone.png is a390px viewport showing confirmation, not the full page.

Docs/browser-only; no application changes or suite rerun. Latest suite247 tests52.030s from584a6a0. Reader logged out, tab17closed, viewport reset, server91080stopped.
