# Phase 78d — mobile CKEditor toolbar targets

## Scope

On the dashboard's new-post form, 21 visible CKEditor toolbar buttons were
30 px high before this phase. Most icon buttons were 30 px wide, and the two
split-list arrows were only 16 px wide. The custom line-spacing select was
30 px high. A rule scoped to `#newPostForm` and widths below 576 px now sets
toolbar buttons to at least 44 × 44 px and the spacing select to at least
44 px high. No editor plugin/configuration, post data, or desktop CSS changed.

## Isolated browser evidence

A synthetic-owner SQLite copy ran on port 8063; the original `db.sqlite3`,
media and port 8000 were untouched.

| Width | Toolbar buttons | Spacing select | Toolbar height | Horizontal overflow |
| --- | --- | --- | ---: | --- |
| 320 px | 21/21 at least 44 × 44 px | 44 px high | 363 px | None |
| 390 px | 21/21 at least 44 × 44 px | 44 px high | 259 px | None |
| 1440 px | Existing 30 px height, minimum width 16 px | Existing 30 px | 46 px | None |

At 320 and 390 px, Heading, Font Family and Font Size dropdowns each opened
and exposed their menu. Their visible panels remained within the viewport;
`document.scrollWidth - innerWidth` was -15 px, and the toolbar items'
`scrollWidth` equaled `clientWidth`. No formatting option was selected and
the post form was not submitted.

Tradeoff: the enlarged buttons make the mobile toolbar considerably taller
than before (about 189 → 363 px at 320; 159 → 259 px at 390). This is a
conscious touch-accessibility tradeoff; a later editor-specific design pass
could reduce vertical space without shrinking targets. This phase does not
claim a complete screen-reader or editor-feature audit.

## Automated gates

- Focused render-contract test: 1/1 passed.
- Full Django suite: 40/40 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
