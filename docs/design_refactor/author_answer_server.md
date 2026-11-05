# Author answer server acceptance

Two additional isolated tests in blog/test_author_journey.py exercise the real settings POST endpoint and rendered public author endpoint, rather than service helpers alone.

- Owner saves a trimmed private answer with answered_at; the sender sees its question, another authenticated user does not, and a guest does not see the private answer.
- Owner publishes an answer; a guest sees it. Clearing the answer while requesting publication forces is_public=False and clears answered_at; the guest no longer sees the question.
- A different authenticated user cannot update or delete the question by submitting its id to their settings endpoint; persisted answer and visibility remain unchanged.

Targeted six author-journey tests passed in1.234s. Raw z/work/author-answer-tests.txt. Full-suite result is recorded in author-answer-suite.txt. No application behavior or template changes in this phase; no email, browser submission or persistent QA data change.

This complements author_question_browser.md and author_onboarding_preservation.md. Owner browser answer/publication, full keyboard/error presentation, named question/answer textareas and31px reader submit target remain open. Server tests do not close those browser requirements.

Full suite:249 tests passed in56.273s; check and migration check green.
