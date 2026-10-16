# Phase101n — Polarna actual comment/author ink and both theme timestamps

The101l before audit identified the real nested post-author link as light on the existing light span surface (1.043:1), and mobile author/body text fill as light despite dark CSS color (1.178/1.059). This phase supplies dark #123047 ink to that link and currentColor fill to the real mobile comment elements, including bp-comment-word spans. Existing opaque #f1fbff surfaces are retained. Polarna registration text now has the same explicit ink/surface rather than translucent Bootstrap muted ink over blue.

At>=768px both themes' small timestamps gain matching local opaque reading surfaces and opacity1: Polarna #123047/#f1fbff, Sumska #354b32/#f5fbef. Mobile dates remain unchanged.

## Verification
16 standard blog/detail states320/390/768/1440 with2 comments and Bootstrap. Compared against101l; all static rectangles identical, excluding the date-sensitive day14/today16 calendar scale. Existing phone title/comment overflow and calendar findings are unchanged/open.

Polarna post-author, both comment authors/bodies and registration message12.980:1 on all widths. Actual bp-comment-word fill verified#123047. Polarna dates>=76812.980; phone12.591 unchanged. Sumska dates>=7689.042; phone7.407 unchanged. Opaque local surfaces provide photo-independent proof for these elements only.

Safe open reached77/78, and comments link reached the visible Polarna comments. Screenshot outputs/phase101n-polarna-comments.png inspected. No user palette fields changed; the fix reconciles existing theme reading surfaces and fixed author/comment ink.

Django check and migration dry-run pass;214 tests pass in52.524s. Other101l layout, calendar, archive/active-day contrasts, photographs and control targets remain open. Original repo/database/media/port8000 untouched.
