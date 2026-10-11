# Phase100o — Litica / Podvodna mobile calendar

Date: 2026-10-11. Baseline: c7dc24c (Phase100n).

## Problem and change

A dense week containing seven linked days caused document overflow on phones. At 320/390px, Litica had 92/22px document overflow and Podvodna 92/66px. The single-post fixture did not reveal this failure.

Only these two themes now wrap weekday headings and the date grid in one labelled, keyboard-focusable horizontal scroll region. The grid retains seven columns, 44px minimum targets and 6px gaps. Month navigation stays outside the scroller. A visible narrow-phone instruction explains horizontal movement; native scrolling and focus outline remain available. The calendar card uses its available column width, and today's scale is reset on mobile. Local horizontal scrolling is intentional; this is not a claim of zero local scroll width.

## Browser verification

Bootstrap loaded; isolated .qa100e.sqlite3, server 8017. Both blog and detail at 320, 390, 768 and 1440px for each theme:

- Dense fixtures 2421/2422, posts 15–21 / 22–28 dated October 5–11: 16 states, document overflow 0 and calendar-box overflow 0.
- Standard fixtures 2411/2412, posts 13/14 with two comments: another 16 states, document overflow 0.
- Dense mobile active dates remain at least 44×44px. Scroll region approximately 201px / 271px at viewport 320 / 390, scroll width 348px.
- At 768 and 1440, standard calendar/layout measurement objects equal the Phase100n after measurements. Desktop date targets remain a separate outstanding issue.
- On each dense blog at 320, keyboard right-arrow scrolling reached approximately 147px while window.scrollX remained 0. Clicking day 11 opened the correct canonical post, 21 / 28.
- Previous month, next month and opening the standard post worked for both themes. Two comments remained present; no mutating controls were used.
- Mobile comment-author contrast remained 14.806:1 (Litica) / 13.961:1 (Podvodna), below the photographic zone. No new photographic contrast claim.

The viewport screenshot phase100o-mobile-calendar.jpg was visually inspected: weekday/date alignment, focus outline, helper and native local scrollbar are visible. Per-state raw JavaScript objects were not persisted after the browser session; the values above are the recorded run summary. Phase100n retains the baseline measurements.

## Automated verification and cleanup

Django check: no issues. Migration check: no changes. Full suite: 214 tests, OK, 147.701s, exit 0. The run emitted a Windows WMI/argon2 platform-query exception diagnostic (0x8007000e), then continued and completed all tests successfully; the existing missing staticfiles-directory warning also appeared.

QA tab closed, viewport reset, server 8017 stopped. Synthetic database retained. Original repository, database, media and port 8000 untouched.

## Remaining scope

This closes the confirmed dense phone calendar overflow from Phase100n. Photo=true / contrast=null entries in Phase100l remain unverified, particularly the first desktop Podvodna comment. The evidence index is not a final pass matrix: coverage remains 13/37, with another 24 designs, full factory Default, desktop targets and user pages still pending.
