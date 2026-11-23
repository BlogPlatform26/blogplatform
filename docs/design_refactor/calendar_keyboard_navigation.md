# Planine calendar keyboard navigation evidence

Recorded on 2026-11-08 against 4737412 using synthetic qa100s_planine_u_magli and post30 in .qa100e.sqlite3. This is a bounded navigation check, not complete calendar acceptance.

At 320, 390, 768 and 1440 CSS pixels, starting from the previous-month link, Tab traversed next-month link, the named calendar scroll region and day11. Native Enter opened the canonical post30 URL. Browser Back returned to the October2026 blog URL. The starting link was programmatically targeted by the supported locator press API; this does not prove a full page-from-top Tab path. The earlier 1280 sample separately exercised previous-month Enter from November to October.

The focused day was entirely inside the viewport at each width; document horizontal overflow was zero. The phone calendar scrolled horizontally to reveal the day. The inspected 390x900 requested viewport screenshot shows a visible dark focus outline around11. Computed outline was auto1px rgb(16,16,16) at every width, but only the phone focus screenshot was visually inspected. Day targets measured44x44 on320/390/768 and25.703125x36 on1440; desktop target acceptance remains open.

The actual day foreground was rgb(86,102,122), backing rgba(245,248,252,0.82), font700 12px/18px Arial. Because the backing remains translucent, these values alone do not prove rendered contrast. No active/today/hover contrast closure follows from this evidence.

Back did not restore focus to day11 in this browser: the following Tab reached the logo on all four widths. Treat this as an observed return-navigation limitation, not evidence of a code regression or a completed recovery path. Further work must decide and verify the intended return focus behavior without conflating browser history behavior with application state.

Durable evidence under C:/Users/mario/Documents/Codex/2026-10-10/z/: work/calendar-journey-initial.json, work/calendar-journey-four-widths.json and outputs/calendar-keyboard-phone.png (viewport screenshot, not full page). The initial sample is1280x720; the four-width samples use height900. Temporary evidence was copied successfully after a usage-related automatic approval failure; no credit reset was used.

No application changes or new suite run. Latest application suite remains250 tests50.645s for dffd80e. QA session97956 was stopped, tab12 closed and viewport override reset. Full all37/U01-U12 acceptance remains incomplete.

## Planine month arrows (2026-11-23)

Evidence-only inspection at HEAD493634c, guest November2026 blog route /blog/qa100s_planine_u_magli/, synthetic .qa100e.sqlite3. At320/390/768/1440 both arrow glyphs have actual text fill rgb(67,86,108), 60020px/20px Garamond. Their rgba(255,255,255,.26) surface is over opaque rgb(241,245,251) title backing (no background image), giving composed rgb(244.64,247.60,252.04) and contrast7.054:1. This normal-state result does not depend on sampling the photograph.

Both arrows receive focus-visible through Shift+Tab/Tab at all four widths (eight states). Computed native outline rgb(16,16,16) auto0.666667px with0.666667px offset. Durable390px viewport screenshot visually confirms the next-arrow ring without clipping. Other widths have DOM focus evidence only; the first desktop screenshot was unsuitable for visual certification and is not counted. Focus-indicator area compliance and hover are not certified here.

Targets are44x44 at320/390/768,30x30 at1440. Document overflow0 throughout. Desktop target acceptance remains open under the project target requirement; no desktop appearance changed. No app or fixture changes, no new test-suite claim. QA server stopped; guest tab closed and viewport reset.

Raw: z/work/planine-calendar-arrow-inspection.json. Screenshot: z/outputs/planine-calendar-arrow390.png (390px viewport, not full page). This closes only normal arrow text/backing contrast on this fixture and records bounded keyboard evidence. Calendar day-with-post/today/hover/active/focus, desktop target decisions and return-focus behavior remain separate. The theoretical darkest-photo composition for the translucent post-day surface is4.378:1; this is a conservative bound, not a measured failing screenshot, so no failure or repair is claimed from it.

## Planine post-day stable surface and focus (2026-11-23)

The non-today day-with-post used rgba(245,248,252,.82), so its normal/focus reading surface depended on the photograph. This change uses the same opaque RGB #f5f8fc, retaining #56667a text: stable contrast5.511:1. The prior4.378 theoretical darkest-photo bound is not presented as a measured fixture failure. Keyboard focus now has a2px solid #43566c inset outline (CSS offset-3px; browser-2.66667px), contrast7.076 against the fixed surface. The ring is contained within the target, avoiding clipping at the horizontally scrolling region edge. Desktop background and keyboard focus intentionally change; dimensions and typography do not.

Paired October2026 blog samples at320/390/768/1440 cover51 calendar nodes per width. All visible node widths/heights/x/relative-y, fonts, fills, colors, images and local-overflow values are retained; only post-day background changes. Viewport-y differences at390/768 came from scroll restoration, so comparison uses coordinates relative to the calendar root. The hidden zero-size hint at768 is excluded from relative-y comparison. Document overflow0. Native focus reveals the offscreen linked day on phones, and all four inspected viewport screenshots show an unclipped inset ring. Targets remain44x44 through768 and25.8125x36 at1440 in this run; desktop target acceptance remains open.

Native390 Enter on day11 reaches /post/30/a-longer-editorial-story-for-mobile-and-desktop-verification/. Final canonical detail checks at all four widths confirm opaque backing, actual child fill, focus-visible, zero document/linked-day local overflow and no calendar-cell intersections. Detail checks are after-only, not an independent paired detail baseline. No synthetic content or credentials changed. The today rule and hover behavior retain their existing separate cascade; this bounded fix does not close those states, other themes, custom palettes or return focus.

Validation:253 tests112.213s passed; check clean; migration dry-run no changes; diff check clean. Raw z/work/planine-post-day-before.json,planine-post-day-after.json,planine-post-day-comparison.json,planine-post-day-detail.json,planine-post-day-suite.txt. Inspected z/outputs/planine-post-day-focus320.png,390.png,768.png,1440.png are scrolled viewport captures, not full pages. QA servers83864/82472 stopped, guest tab2 closed, viewport reset.
