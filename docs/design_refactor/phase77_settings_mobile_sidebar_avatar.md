# Phase 77 — settings mobile sidebar and avatar width

## Scope and cause

Phase 76 left two measured settings-dashboard issues. At 320 px the default
`postavke` subtab overflowed by 9 px: its avatar-upload flex child had an
inline 280 px minimum width inside a narrower padded card. At 768 px the
Bootstrap `col-md-1` sidebar was about 62 px wide, wrapping its labels.

The avatar flex child now has a scoped class; below 576 px its minimum width
can shrink to zero. Between 768 and 991.98 px only the settings sidebar and
content columns become full-width, with the six sidebar links in a three-column,
two-row grid. The CSS URL carries a version query so clients load the changed
stylesheet. At 1440 px the existing 1/11-column dashboard layout is unchanged.
No design template, other tab editor, model, or migration was changed.

## Browser evidence

An isolated copy of the synthetic Phase 76 SQLite database, with its test
owner, was served on port 8059. The original `db.sqlite3`, media and port
8000 were not used.

- At 320 px, the avatar-upload field's right edge moved from 329 to 280 px;
  document overflow changed from +9 to -15 px.
- At 390, 768 and 1440 px the `postavke` page also had no document overflow.
- At 768 px, the six sidebar links measured about 251 px wide and at least
  44 px high in two rows, instead of 62 px wide with wrapped labels. The
  sidebar height fell to 88 px. A screenshot confirmed readable labels.
- All six top-level settings tabs were clicked at 320, 390, 768 and 1440 px;
  each reached its intended URL. None produced positive document overflow
  in this synthetic state.
- At 1440 px the sidebar remained about 118 px wide in the existing desktop
  arrangement. The header remains the Phase 76 desktop layout.

This is not a complete audit of forms, the design editor, avatar crop modal,
or all tab states/content. The fix is limited to the observed width and
sidebar causes.

## Automated gates

- Focused settings contract test: 1/1 passed.
- Full Django suite: 37/37 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
