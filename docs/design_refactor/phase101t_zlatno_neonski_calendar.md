# Phase101t — Zlatno polje / Neonski grad calendars

Extended the existing local phone calendar scroll region and 768–991.98 full-column layout to these two themes. Seven-day semantics and 44px active targets are preserved. Desktop styles are unchanged.

## Evidence

Raw before: Phase101s standard/dense series (and Phase101r initial calendar failures). After: 40 blog/detail states: four standard/dense fixtures at 320/390/768/1440, plus both dense fixtures at 820/991. All document overflow is zero; calendar grid fits its own scroll region. Minimum active target below 1000px is 44px. All 16 measured tablet column layouts have no overlap (0.1px rounding tolerance). All measured desktop rectangles match Phase101s exactly; actual text fill/color match at common widths. Photo-backed contrast remains unresolved; unchanged ink is not contrast proof.

Native ArrowRight settled at scrollLeft40 for both dense phone calendars. Day11 links opened posts101/108; standard post links opened93/94. Screenshot outputs/phase101t-zlatno-calendar.png visually confirms the tablet calendar above the post, without overlap; no screenshot coordinate mapping is used for contrast.

Django check and migration dry-run pass. Full suite:214 tests OK in64.398s. Only the existing missing staticfiles warning appeared.

Remaining: Zlatno like actual blue4.243 and archive4.273 need actual child confirmation/local correction; photographic labels and desktop targets remain open. Coverage23/37 is not a pass count. Next themes: Polje lavande / Carobna ljubicasta.
