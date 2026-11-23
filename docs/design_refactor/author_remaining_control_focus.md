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

## Guest sign-in inline spacing repair (2026-11-23)

The guest Prijavi se link had3.885px between its right edge and the first following character, while the opaque focus outline extended5.333px (2.66667 width plus offset). The390 screenshot showed the ring entering the following word. A scoped author-guest-login class now adds margin-inline-end:0.5rem. The gap measures11.885px at320/390/768/1440, leaving6.552px beyond the ring. The8px shift of following text is intentional on desktop too. Link dimensions, typography and outline are unchanged.

Native Tab from Back focuses the sign-in link at all four widths; focus-visible is true and document horizontal excess0. All four900px-high viewport images were inspected; at320 the following text wraps below with no visible ring/text collision. Enter reaches /login/ (guest, no credentials entered). Paired normal samples include24 leaf nodes per width, with all measured rectangles/fonts preserved. At768/1440 sampled colors/backgrounds also match;320/390 have a header search-icon foreground difference recorded in raw evidence, unrelated to the scoped link rule. The text following the link intentionally shifts8px and is measured separately by DOM Range; leaf-only equality is not a claim that this text stayed in place.

Raw under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: guest-link-before.json, guest-link-after.json, guest-link-suite.txt. Inspected screenshots under z/outputs/: guest-link-after320.png, guest-link-after390.png, guest-link-after768.png, guest-link-after1440.png.253 tests136.958s passed, Django check clean, no migrations. QA used .qa100e.sqlite3, locmem email, own8017 servers26616/14680 stopped; guest tabs5/6 closed and viewport reset.

This closes the recorded guest inline sign-in overlap. Custom content-link/backing states and calendar active/today/hover/focus/arrows/return focus remain open, as does full all37/U01-U12 acceptance.

## Content-link contrast and inline focus (2026-11-23)

A temporary synthetic2673 fixture added a long URL (https://example.test/ plus18 dugi-put/ segments), a short social URL and a website URL. It exposed link contrast4.293:1: actual fill#0d6efd over rgba(248,249,250,.9), rgba(255,255,255,.95) and white body, composed RGB248.7/249.6/250.5. The existing outward3px outline offset also entered adjacent prose around a wrapped URL.

The existing scoped .author-page-info-value a rule now uses#084298 and an always-visible underline. Its focus-visible override uses outline-offset0, preserving the existing3px opaque outline while keeping it outside the glyphs and away from surrounding words. These color/decoration/focus changes are intentional on desktop too. The measured new text contrast is8.929:1 on this backing. Arbitrary custom photographic backing acceptance remains open.

Paired320/390/768/1440 measurements preserve all three links' rectangles, line fragments, fonts, card geometry and backgrounds exactly. Long URL wraps into10/7/7/4 fragments respectively; the short social URL wraps into2 fragments only at320. Document and info-card local overflow0. Native Tab traverses all three links at every width (12 focus-visible states, offset0). Long-link focus inspected at all four widths;320 durable screenshot recovered using native Tab/Shift+Tab after an earlier scaled/cropped capture was rejected. No external URL was opened.

Raw z/work/author-content-link-before.json, author-content-link-after.json, author-content-link-suite.txt; viewport images z/outputs/author-content-link-after320.png, author-content-link-after390.png, author-content-link-after768.png, author-content-link-after1440.png (900px-high viewports, not whole-page acceptance).253 tests115.544s/check/migrations green. QA8413/94324/38596 stopped, guest tabs7/8/9 closed, viewport reset. Synthetic2673 social and website fields restored to empty; bio remains Synthetic retry draft must survive. No credentials changed.

Recorded content-link contrast/focus issue closed; other custom backing/hover states and calendar active/today/hover/focus/arrows/return focus remain open within the full37/U01-U12 objective.
