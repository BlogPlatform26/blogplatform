# Owner answer browser workflow

On b920f12, synthetic owner2673 opened /blog/settings/?tab=autor and saved question1 with a private answer. The page showed Odgovoreno, Privatno za posiljatelja and answered1/unanswered0. The owner then edited the text to Synthetic owner public answer, checked public visibility and saved. The page showed Javno and the checked option. After logout, the public author page displayed the question and published answer to the guest.

Raw guest DOM: z/work/author-answer-guest.txt. Screenshot outputs/author-answer-guest.png is an inspected390x900 viewport; the answer text is below the captured bottom edge, so DOM supplies that proof. No whole-page screenshot claim.

This complements server privacy/ownership transitions in author_answer_server.md. Browser other-viewer private answer, clear-answer transition, full keyboard and four-width owner-form geometry remain open. Answer textarea uses placeholder as its current name; its visible label lacks association. No application changes or suite rerun; latest249 tests63.414s from b920f12.

Initial browser synchronization timed out during login; reconnect recovered existing tab19 on home. No duplicate submission occurred during recovery. Owner logged out; guest state verified; tab19closed, viewport reset, server59225stopped. Only isolated QA question1 changed; no SMTP.
