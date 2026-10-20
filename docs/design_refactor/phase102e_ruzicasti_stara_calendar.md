# Phase102e — Ruzicasti / Stara phone calendars

Both custom phone calendars now use a focusable local horizontal scroll region with minimum344px grid, seven44px targets and6px gaps. Phone parent grid uses minmax(0,1fr) and children min-width0 to contain the intrinsic grid width. Initial wrapper-only attempt expanded the page; final measurements follow the parent-grid correction and QA restart.

32 standard/dense blog/detail states320/390/768/1440: document overflow0. Dense phone day starts50px apart with44px targets; no overlap. Tablet/desktop measured rectangles identical102d; actualfill/color unchanged. Safe standard157/158 and day11 165/172. Native ArrowRight settled40px both; immediate0 samples were taken before animation settled and are not final scroll evidence.

Check/migration green; all214 tests passed in45.274s. Screenshot APIs both failed; no new screenshot or visual screenshot verification claimed. DOM geometry and interaction evidence saved to phase102e_measurements.json.

Next Ruzicasti month3.359 andweekday2.948 ink remain open. Six remaining special-theme matrices,photozones,desktop targets,factoryDefault,user pages remain. Coverage31/37 is not passes.
