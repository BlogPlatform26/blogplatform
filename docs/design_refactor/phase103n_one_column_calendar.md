# Phase103n: one-column right calendar verification

No application changes. Verified the previously untested right-sidebar branch after c31ccc1 using isolated users2678 qa103n_one_dark_right (posts258–264) and2679 qa103n_one_classic_right (posts265–271). Preferences explicitly select right_box_columns=1. Server responses contain one calendar scroll region and omit the two-column layout marker.

20 browser states: both designs, blog/detail,320/390/768/991/1440. All document excess values are0 and all calendar grid-cell intersection lists are empty. Raw measurements include calendar/column/day rectangles, actual linked-day fill, scroll-region client/scroll widths, and all day fonts/fills/backgrounds. Phone overflow remains inside the named scroll region as designed. Native day11 clicks at320 reach canonical posts264 and271.

This closes the one-column calendar containment/navigation evidence gap for these fixtures. No screenshot was taken; no visual screenshot acceptance or new contrast claim is made. Desktop target sizing and broader profile/content/custom-palette acceptance remain open. No full suite rerun for this documentation-only audit; latest224 tests48.849s/check/migration passed in103m.

Raw: z/work/phase103n/fixture-preparation.json, states.json, safe.json. QA server and temporary browser tab closed; viewport reset.
