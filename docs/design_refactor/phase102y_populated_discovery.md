# Phase102y: populated discovery workflows and repairs

Baseline97914ac. Isolated.qa100e.sqlite3 fixtures: author2671 qa102y_author, reader2672 qa102y_reader following that author, posts221-228, tag qa102ylongtaglongtaglongtag. Eight published/admin-featured entries exercise two pages. Post221 has169 unbroken title characters after its prefix and420 unbroken body characters; the author's blog name is168 unbroken characters. No real accounts/media/mail were used. The fixture remains for subsequent targeted work.

Twenty guest before/after states cover featured, all filtered by populated tag, search posts/users/tags at320/390/768/1440. Four logged-in following states and actual page2 navigation additionally confirm the following filter returns synthetic author results. The following-series evidence predates the repair; its code path was not changed. This is a reader following fixture, not proof of every owner workflow or empty following state.

Findings and changes:

- Search users: long blog-name text exceeded its content column by1248.49/1178.49/1225.11/905.16px despite document overflow0. Scoped search-user-result wrapping now gives0 text excess at all widths.
- Featured secondary cards: six-column grid made phone cards30.44/42.10px wide and locally overflow26/14px. It now has one column below576 and two below768. Measured320/390 card widths279.33/349.33px; sampled local overflow0. Existing two-line truncation remains intentional; full content remains available through the link. Tablet/desktop grid unchanged.
- Featured last page: navigation was conditional on a nonempty secondary preview list, so page2of2 lost the previous link. Pagination now depends on has_other_pages; the secondary heading/grid separately require preview content. Browser next reachespage2 and previous returnspage1. A functional eight-result test checks the last page, preserved tag/filter and absence of an empty secondary heading.

All20 final guest states have document/sample local overflow0. Eight tablet/desktop non-user-result states retain every sampled rectangle. User result height intentionally grows to contain the name. Actual fill samples are retained in raw data, but this is not a composed-contrast signoff. Screenshots z/outputs/phase102y-users-phone.png show a320px viewport, not a full page. Source image fallback404 remains open; the earlier featured screenshot is not a reliable final card view and is not acceptance evidence.

Check/migration green;217 tests pass58.218s. QA templates were measured after a fresh8017 server. Guest session restored after synthetic login. Remaining U01: empty following/owner distinctions, keyboard/source order, actual contrast (including inactive filters and gradient text), tablet card usability, image fallback and broader real content cases. Do not repeat closed pagination/query/name wrapping or the37-theme series.
