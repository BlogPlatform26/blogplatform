# Phase 78b — mobile new-post tabs and actions

## Scope

On the dashboard's `post_filter=new` view, seven post subtabs and the two
primary action buttons had 41 px and 31 px heights respectively (Phase 78a).
Only this view now gets a mobile rule below 576 px: its subtabs and
`Objavi` / `Spremi kao draft` buttons have a minimum height of 44 px.
Desktop styling and the CKEditor configuration were not changed.

## Browser verification

An isolated copy of the synthetic owner database ran on port 8061. The
original `db.sqlite3`, media, and port 8000 were not used.

| Width | Seven subtab heights | Publish / draft height | Document overflow |
| --- | --- | --- | ---: |
| 320 px | 44 px each | 44 / 44 px | -15 px |
| 390 px | 44 px each | 44 / 44 px | -15 px |
| 1440 px | 41 px each, unchanged | 31 / 31 px, unchanged | -15 px |

At 320 and 390 px, a real click on the active `Novi post` tab stayed on the
new-post view. Each action button received keyboard focus through a harmless
arrow-key press; `document.activeElement` identified the correct button.
Neither submit button was clicked, the form was not sent, and no post was
saved or published (`Post.objects.count()` remained 0 in the trial DB).
The six other subtab destinations were not opened in this focused check.

This does not solve the 30 px form fields or CKEditor toolbar controls noted
in Phase 78a; those require separate scoped work.

## Automated gates

- Focused render-contract test: 1/1 passed.
- Full Django suite: 38/38 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
