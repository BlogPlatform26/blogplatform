# Phase100p — comment timestamp contrast audit

Application baseline c0827bb, 2026-10-11. This is a completed measurement mini-phase with a confirmed new P1, not an implementation or a final pass for either theme.

## Scope and evidence

Litica noci and Podvodna tisina, synthetic authors 2411/2412, posts 13/14 and two comments each. Blog and detail at 320/390/768/1440: 16 states, 32 timestamps. Browser computed foreground, opacity, ancestor backgrounds, geometry and photographic bounds are retained in phase100p_comment_time_measurements.json. Composited results are in phase100p_comment_time_results.json. Below the photo, ancestor backgrounds were composited over the body's actual solid color; element opacity was then applied to the foreground before relative-luminance contrast calculation.

| Theme | 320/390, both comments | 768, both comments | 1440 first comment | 1440 second comment |
| --- | --- | --- | --- | --- |
| Litica |11.948:1|4.1824:1 FAIL|4.1824:1 FAIL|4.1824:1 FAIL|
| Podvodna |11.4595:1|3.9873:1 FAIL|Photographic: unresolved|3.9873:1 FAIL|

Results match between blog and detail. At phone widths timestamps use opacity .9 over the dark mobile comment surface. At 768/1440 they use opacity .78 over rgba(255,255,255,.34). These are ordinary small text, so the confirmed ratios are below 4.5:1. Earlier Phase100l author/body measurements did not establish timestamp contrast. The photo=true row's bg value remains only the fallback, never photographic proof.

## Photographic measurement limitation

Podvodna's first desktop author is at y813.97, timestamp at y812.64, and text at y839.30; the photo is 864px high. A paired screenshot attempt temporarily made only comment text transparent in the local template while retaining layout and backgrounds. DOM rectangles matched before/after. However, the screenshot returned 1425x868 for a requested 1440x900 viewport, and visual layout differed from DOM geometry. The coordinate assertion rejected the pixel analysis. These captures are therefore NOT used as a contrast pass or failure. The original template was restored byte-for-byte; git diff confirmed no application changes. No database mutation was needed.

Next implementation priority: narrowly correct timestamp opacity/color in these two themes, verify both comments on all four widths, and obtain trustworthy photographic evidence for the first Podvodna desktop comment. Other photographic header/body/calendar zones remain unresolved.

## Validation and cleanup

The current original application was reloaded after restoring the temporary measurement override, before all 16 timestamp states were collected. Safe post-open navigation to the canonical detail succeeded. No like/comment submissions. QA server8017 stopped, tab closed and viewport reset. Synthetic DB retained.

No lasting application change; the existing Phase100o check/migration/214-test pass remains applicable. This audit does not justify a duplicate full suite. Raw observations are persisted in this commit. Original repo, DB/media, port8000, main and deployment untouched. Coverage remains13/37, not13 passing designs; remaining24 designs, full factory Default, desktop targets and user pages still pending.
