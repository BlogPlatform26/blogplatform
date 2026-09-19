# Phase 74b — mobile header and search

## Scope

The active shared base template now declares a device-width viewport. At widths up to
575.98 px, the inline search occupies its own full-width flex row, its field can
shrink within the row, and the search controls and authentication links retain
44 px minimum touch height. Desktop rules and design-specific templates are unchanged.

## Verification

- An isolated SQLite copy and local server on port 8057 were used. The original
  `db.sqlite3`, media files, and port 8000 were not touched.
- At 320 and 390 CSS px, home, search, login, register, user blog, and post
  detail all rendered at the requested viewport width. The search toggle
  expanded and collapsed the inline form. The field measured 44 px high and
  the submit button 44 by 44 px. No document-level horizontal overflow was
  found (scroll width minus viewport width was -15 px with the scrollbar).
- A real UI submission of `mobile` navigated to `/search/?q=mobile`.
- At 1440 px, the homepage retained its desktop header and three-column
  composition with no document-level horizontal overflow.
- The shared-header regression test covers rendering of the six public routes.

Bootstrap's collapse animation briefly leaves the search form in a
`collapsing` state after a click; closed-state checks wait for it to become
hidden. This change does not audit every design or authenticated navigation.
