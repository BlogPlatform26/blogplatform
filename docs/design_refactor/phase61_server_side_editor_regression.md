# Phase 61 — server-side editor regression

## Scope

Phase 61 adds a focused regression suite for the active title/date workflow at
`/blog/settings/live-editor/naslovi/`. It does not exercise browser JavaScript or
the three simple-design background branches.

## Permanent coverage

`blog/test_design_live_editor_workflow.py` verifies:

- an authenticated user can open the active live editor;
- `save_title_settings=1` follows the POST/redirect/GET contract;
- all 14 title and date fields are persisted;
- the save contract is exercised for every one of the 37 authoritative
  `Profile.TEMPLATE_CHOICES` entries;
- a write is scoped to `data.design_customizations[active_template]`;
- saving a second template preserves the first template's customization;
- two users using the same template remain isolated;
- `reset_titles_mode=all` restores the active template's title/date defaults
  while preserving another template's customization.

The tests use the real URL, view, preference service and `UserBlogPreference`
model. They intentionally assert the current normalized-data contract: reset
stores the active template defaults rather than deleting unrelated template
keys.

## Verification

- Focused suite: 6 tests passed.
- Full Django suite: 20 tests passed.
- `manage.py check`: no issues.
- `manage.py makemigrations --check --dry-run`: no changes detected.

Django created an in-memory SQLite test database. The original `db.sqlite3` was
not migrated or modified.

## Remaining scope

Browser-side live preview, individual client-only reset buttons, computed CSS
application after reload, and the simple-design background editor remain for a
separate browser-focused phase.
