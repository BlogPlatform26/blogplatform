# Remaining author-control focus

The owner profile form and filters, and public author-page controls, now use an opaque #084298 focus-visible outline (3px CSS, 3px offset), replacing translucent shadows. The profile wrapper scopes this to the author form. Desktop keyboard focus intentionally changes too; normal layout and typography do not.

## Evidence

Widths: 320, 390, 768 and 1440 CSS px. Paired owner samples cover 24 controls per width; public samples cover Back, question textarea and submit. Recorded normal geometry, fonts, colors and backgrounds are unchanged apart from vertical floating-point differences below 0.001px. Recorded document/local overflow is zero.

Native owner Tab evidence covers 27 steps per width, including date segments, profile controls and filters. The date-picker internal button uses its native visible black indicator, inspected at390; its host does not match focus-visible. Do not count it as an opaque custom outline. Public native evidence covers12 focus states, all visible and within their cards. The outline contrasts9.362:1 against white; the recorded guest card is .95 white over white body with no image. This is fixture-specific backing evidence, not acceptance of every custom theme.

On2026-11-17, screenshot capture recovered. Visually inspected and saved Back, textarea and submit at390, and submit at320/768/1440. Indicators are visible without clipping or overlap on these controls. Guest sign-in at390 was also saved; its outline is close to adjacent explanatory text, so inline-link spacing remains a separate review item. Owner four-width images were already inspected. No question/profile form was submitted in this final review.

Raw evidence under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: author-remaining-owner-before.json, author-remaining-owner-after.json, author-remaining-owner-focus320.json, author-remaining-owner-focus390.json, author-remaining-owner-focus768.json, author-remaining-owner-focus1440.json, author-remaining-public-before.json, author-remaining-public-after.json, author-remaining-public-focus.json, author-guest-backing.json, author-remaining-suite.txt.

Images under the sibling outputs directory: author-owner-focus320.png/390.png/768.png/1440.png; author-public-focus390-0.png, author-public-focus390-1.png, author-public-focus390-2.png; author-public-focus320.png, author-public-focus768.png, author-public-focus1440.png; author-guest-focus390.png. Images are viewport captures, some scrolled; they do not represent full-page acceptance.

Validation:251 tests passed in155.786s; Django check clean; migration check reports no changes. Application code did not change after that suite. Final QA used .qa100e.sqlite3, locmem email and port8017. Reader logout verified by guest navigation, tab10 closed, viewport reset, own server15239 stopped.

## Remaining scope

This closes the recorded form/filter opaque-focus repair, not full U04. Inline guest/content-link spacing, custom public backing/link states, calendar active/today/hover/focus/arrows/return focus and the remaining all37/U01-U12 matrix stay open. Do not rerun the paired form measurements without a new change.
