# Phase 76 — mobile dashboard header and search

## Scope and cause

The authenticated dashboard uses `dashboard_base.html`, separate from the
public `blog/base.html` fixed in Phase 74b. Before this change it had no
viewport meta tag, a 320 px inline search group, and a single-row header whose
owner menu extended beyond a 320 px viewport. The measured document overflow
was 61 px and the search toggle was only 31 by 30 px at 320 px.

The dashboard shell now declares a device-width viewport. At widths below
992 px, the existing header wraps its owner controls and full-width search
into rows, search fields can shrink, owner text truncates within the viewport,
and header/search controls have 44 px minimum touch targets. The submit
button gains a stable ID for testing. No design template, settings-tab editor,
model, or migration changed. Desktop CSS above this breakpoint is unchanged.

## Browser evidence

An isolated newly migrated SQLite database with one synthetic owner was served
on port 8058. The original `db.sqlite3`, media, and port 8000 were not used.

- At 320, 390 and 768 CSS px, the dashboard reported the requested viewport
  width, a device-width viewport meta tag, and no document overflow on the
  default settings page (scroll width minus viewport width: -15 px).
- At those three widths, the search toggle, input and submit were each 44 px
  high; toggle and submit were 44 px wide. Their center points were hit-testable.
  Opening and closing the collapse changed `aria-expanded` true/false. Checks
  waited for Bootstrap's collapse animation to finish.
- A real search submission at 320 px navigated to `/search/?q=phase76`.
- All six settings sidebar links were visible and navigated at 320 px.
- At 1440 px, the default dashboard retained its 54 px desktop header,
  118 px sidebar, 30 px search toggle, and no document overflow.

This is intentionally **not** a full settings-tab or editor audit. The
`postavke` tab still showed 9 px document overflow at 320 px, and the 768 px
sidebar links are narrow (about 62 px, with wrapped text). These are separate
content/sidebar candidates for a later scoped phase, not evidence that the
header regression remains. Other tab contents, media, and all 37 designs were
not visually regressed here.

## Automated gates

- Targeted dashboard-header contract test: 1/1 passed across six tab responses.
- Full Django suite: 36/36 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
