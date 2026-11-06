# Owner answer controls and cancel

The answer label is now associated with a question-specific textarea id. Save/delete targets have scoped minimum height48px (previously31px); no global settings buttons changed.

Four paired320/390/768/1440 samples in z/work/owner-answer-before.json and owner-answer-after.json show document/local overflow0, textarea110px high, both buttons48px. At320 the stacked second button moves down as the first grows; other widths retain side-by-side arrangement. Desktop button height and card height growth are intentional. No palette/font changes were made.

At390, getByLabel Odgovor resolves the field; Tab sequence reaches is_public, save_author_question, delete_author_question. Native Enter on delete opens confirmation; dismiss leaves the answer present. No delete POST occurred. Raw keyboard sequence: owner-answer-keyboard.json. Inspected outputs/owner-answer-controls-phone.png is a scrolled390px viewport.

Owner logged out, guest navigation verified, tab20closed, viewport reset, server63685stopped. No new answer submission. Prior249-test server and browser workflow evidence remains; full owner-page keyboard, long content and browser private-other-viewer/clear transitions are not closed here.

Validation: check and migration check green;249 tests passed in73.483s (owner-answer-suite.txt).
