# Phase103s: public reset confirmation controls

Baseline: 6897167. The valid-token form manually rendered two password toggle groups while the shared initializer created another pair. Two fields therefore had four buttons, with extra rows on narrow screens. Fields and toggles were 30px high; submit was 37.333px.

Removed the manual wrappers/buttons and retained the shared functional initializer. Scoped reset-confirm CSS keeps each input/toggle in one row, permits shrinking, and gives fields/buttons 48px height. The invalid-link retry button also becomes 48px. Desktop form geometry intentionally changes; this is not a desktop geometry-preservation claim. No shared initializer or blog design behavior changed.

Four paired valid-token states at 320/390/768/1440 now have exactly two toggles, two groups, document excess0 and group excess0. Input widths are180.333/250.333/203.708/523.667px; toggle widths44px and all controls48px high. Input and toggle share the standard1px Bootstrap border overlap. Raw rectangles permit checking row alignment; no assertion about every text node or full contrast acceptance is made. After measurements include computed font, fill and background; baseline did not capture these styles, so no before/after color equality claim.

On320, native clicks independently changed the empty first and second inputs to text, then restored password. Empty submit focused id_new_password1 with valueMissing=true. No password was entered or changed and no email was sent. Four invalid-link controls have doc/local excess0 and48px retry targets; native retry reached /password-reset/. The reset-complete login target remains a separate37.333px follow-up.

A valid-token server regression test covers the public template, both fields, and absence of duplicate manual groups.229 tests pass in52.485s; check and migration check pass. Raw evidence is z/work/u03-valid-token/{before,after,interactions,invalid-controls}.json and tests.txt.

Viewport screenshots z/outputs/phase103s-reset-phone.png and phase103s-invalid-phone.png at390 were visually inspected. Initial screenshot calls failed; later capture recovered. These are viewport captures, not full pages or pixel-contrast evidence. Valid-token layout/toggle behavior is verified; expired-token timing, password-success/email workflow, complete-page login target, and remaining acceptance ledger stay open.
