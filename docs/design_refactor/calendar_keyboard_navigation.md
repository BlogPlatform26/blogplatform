# Planine calendar keyboard navigation evidence

Recorded on 2026-11-08 against 4737412 using synthetic qa100s_planine_u_magli and post30 in .qa100e.sqlite3. This is a bounded navigation check, not complete calendar acceptance.

At 320, 390, 768 and 1440 CSS pixels, starting from the previous-month link, Tab traversed next-month link, the named calendar scroll region and day11. Native Enter opened the canonical post30 URL. Browser Back returned to the October2026 blog URL. The starting link was programmatically targeted by the supported locator press API; this does not prove a full page-from-top Tab path. The earlier 1280 sample separately exercised previous-month Enter from November to October.

The focused day was entirely inside the viewport at each width; document horizontal overflow was zero. The phone calendar scrolled horizontally to reveal the day. The inspected 390x900 requested viewport screenshot shows a visible dark focus outline around11. Computed outline was auto1px rgb(16,16,16) at every width, but only the phone focus screenshot was visually inspected. Day targets measured44x44 on320/390/768 and25.703125x36 on1440; desktop target acceptance remains open.

The actual day foreground was rgb(86,102,122), backing rgba(245,248,252,0.82), font700 12px/18px Arial. Because the backing remains translucent, these values alone do not prove rendered contrast. No active/today/hover contrast closure follows from this evidence.

Back did not restore focus to day11 in this browser: the following Tab reached the logo on all four widths. Treat this as an observed return-navigation limitation, not evidence of a code regression or a completed recovery path. Further work must decide and verify the intended return focus behavior without conflating browser history behavior with application state.

Durable evidence under C:/Users/mario/Documents/Codex/2026-10-10/z/: work/calendar-journey-initial.json, work/calendar-journey-four-widths.json and outputs/calendar-keyboard-phone.png (viewport screenshot, not full page). The initial sample is1280x720; the four-width samples use height900. Temporary evidence was copied successfully after a usage-related automatic approval failure; no credit reset was used.

No application changes or new suite run. Latest application suite remains250 tests50.645s for dffd80e. QA session97956 was stopped, tab12 closed and viewport override reset. Full all37/U01-U12 acceptance remains incomplete.
