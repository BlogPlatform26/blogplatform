# Phase 78a — mobile new-post form audit (no implementation)

Scope: signed-in owner at `/blog/settings/?tab=postovi&post_filter=new`, at
320 and 390 CSS px only. The browser used an isolated copy of the synthetic
test database on port 8060. No form was submitted, post saved/published,
original `db.sqlite3` or media touched, or application code changed.

## Confirmed browser measurements

| Item | 320 px | 390 px |
| --- | ---: | ---: |
| Document scroll width minus viewport | -15 px | -15 px |
| New-post form width | 279 px | 349 px |
| Title input height | 30 px | 30 px |
| CKEditor width / toolbar height | 243 / 235 px | 313 / 159 px |
| Video/date/tag input height | 30 px | 30 px |
| Publish button width × height | 63 × 31 px | 63 × 31 px |
| Save-draft button width × height | 124 × 31 px | 124 × 31 px |

All seven post subtabs (Novi post, Kviz, Anketa, Objavljeni, Skice, Na
čekanju, Otpad) were present, about 41 px high, and their center points
hit-tested on both widths. They wrap into three rows. This is a hit-test,
not a navigation test to the other subtab pages, which are outside this
audit. Title, video, date and tag inputs, and both submit buttons were
present and hit-testable when scrolled into view. No child of the new-post
form crossed the viewport's horizontal edge.

CKEditor loaded with an editable region and toolbar. Its toolbar and editing
area had matching `scrollWidth` and `clientWidth` at both widths, so no
internal horizontal scroll was measured. The toolbar wraps vertically;
observed toolbar buttons were about 30 px high (some 16 px wide). The
new-post form begins around 1163 px down the page after the dashboard
navigation; this is a substantial vertical journey, but not an overflow bug.

## Priority for a next, separate phase

P1 touch usability: make the two primary post actions and the seven subtab
links at least 44 px high at mobile widths, then verify focus/submit behavior
without accidentally publishing. The 30 px text fields and CKEditor toolbar
controls also merit mobile touch review, but editor configuration should be a
separate scoped change because it is a third-party, multirow toolbar. No
Phase 78b implementation is part of this audit.
