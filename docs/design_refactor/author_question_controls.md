# Accessible reader question controls

AuthorQuestionForm now supplies the accessible name Pitanje autoru. The public author page submit button has scoped min-height48px, previously31px. No other form or global button rule was changed.

Paired320/390/768/1440 against author-question-baseline.json: textarea remains50px high; submit is48px at every width. Recorded x/y/width/font/actual text fill/background remain identical for visible controls. Document/control-local overflow0. The larger button and following content displacement are intentional on desktop too. Existing pending question1 is present after this phase; baseline preceded that fixture and is not a whole-page identity proof.

Browser AX confirms the question name. Native Enter on empty form390 still produces valueMissing. No duplicate valid question created. Inspected outputs/author-question-controls-phone.png is a scrolled390px viewport including native validation bubble.

Raw z/work/author-question-controls-after.json and author-question-controls-suite.txt. No claim of full U04 closure: owner answer browser journey, full keyboard traversal, answer textarea name and remaining ledger still apply. Logout confirmed by server POST/logout302 and home200 (immediate DOM snapshot was too early); tab18closed, viewport reset, server79330stopped.

Check/migration green;249 tests passed in63.414s.
