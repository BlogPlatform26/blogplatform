# Phase 83e — tablet calendar and archive touch targets

## Scope

Phase 83e extends the existing shared Phase 82c calendar/archive target contract
from 600 px through the Bootstrap tablet breakpoint at 991.98 px. It covers both
the shared sidebar calendar and bespoke special-design calendars without
changing individual design markup.

The contract keeps interactive month arrows and post-bearing days at least
44×44 px and archive links at least 44 px high. Existing 320/390 behaviour is
unchanged, and 1440 px desktop rules remain outside the media query.

## Baseline

At 768 px the isolated browser run measured the shared `default` example at
30×30 px month arrows, approximately 29×31 px for a post day and 28.9 px for an
archive link. The bespoke `magazin` example measured 30×30 px arrows, a 28 px
post-day height and a 24 px archive-link height. Both examples were already at
least 44 px on 320/390, while 1440 retained the compact desktop sizing.

## Regression contract

The existing registry-wide render test now explicitly requires the 991.98 px
breakpoint for every registered design, in addition to the shared arrow, day
and archive selectors.

## Browser result

After the change, both representative render systems measured at least 44 px
for arrows, post days and archive-link height at 320, 390 and 768 px. The shared
example retained its existing 46.2 px mobile/tablet post day; the bespoke
example measured exactly 44×44 px. At 1440 px both retained their original
compact desktop dimensions. No tested viewport produced document-level
horizontal overflow.

Real, non-mutating clicks reached the previous-month query, the canonical post
detail from a calendar day, and the archive-month query.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 66/66 tests.

This phase does not change post-action touch targets or complete the visual
audit of all 37 designs.
