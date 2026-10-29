# Support functional acceptance — server evidence

Following the user's explicit clarification that behavior matters as much as appearance, five integration tests in blog/test_support_workflow.py exercise the actual submit_bug_report route using Django's test database and in-memory email backend.

Covered: all three guest request types map to the stored category, title and outgoing message; contact and referring page are saved; required title/message, invalid email and invalid category are rejected without persistence or email; authenticated ownership and optional empty contact are preserved; simulated mail failure retains the report and returns a warning; GET cannot create a report. Targeted run: 5 tests, 0.419s, OK. Raw evidence: C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-support/workflow-targeted.txt.

This proves server persistence/validation and message construction in the isolated test environment. It does not prove external SMTP delivery or native browser success/error presentation. The 103x phone layout evidence remains valid; tablet narrow fields, full keyboard interaction and browser feedback presentation remain open. No application code changed in this batch.

Full validation: 236 tests passed in 82.631s; Django check and migration drift check passed. Raw suite: C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-support/workflow-suite.txt.
