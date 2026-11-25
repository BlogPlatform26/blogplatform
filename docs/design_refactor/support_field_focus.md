# Support field and retry focus — 2026-11-25

Sidebar fields/radios and retry select/fields/button now use opaque #084298 focus-visible outlines without shadows. This intentionally changes desktop keyboard focus too. Radio offset0 leaves1.33333px clearance at390 (4px text gap, rendered2.66667px outline); other controls use3px offset. Sidebar submit colors from e5c9674 are unchanged.

Eight paired samples cover search sidebar and invalid-title retry at320/390/768/1440:17/18 visible descendant nodes respectively. Fonts, colors, fills, background images and local overflow are unchanged. Sidebar x/width/height exact, document-y drift at most0.000326px; retry rectangles exact. Document/local overflow0. Samples include focused message fields. Final native keyboard checks cover16 sidebar and20 retry focus states. Outline contrast is8.354 on sidebar beige and9.362 on retry white. Radio390, sidebar email1440 and retry submit at all four widths were visually inspected. Whitespace-title POST returns400 and preserves the synthetic message without a valid submission.

Evidence under C:/Users/mario/Documents/Codex/2026-10-10/z/work/: support-field-focus-probe.json; support-fields-before.json; support-fields-after.json; support-fields-focus.json; support-sidebar-final-focus.json; support-fields-final-suite.txt. Inspected scrolled viewport images (height900) in z/outputs/: retry-fields-focus320.png, retry-fields-focus390.png, retry-fields-focus768-final.png, retry-fields-focus1440-final.png, support-sidebar-final1440.png. Earlier768/1440 captures were clipped and are superseded by -final files.

Final tree:253 tests55.352s pass; check clean; no migrations. No app edits after tests. Server71112 stopped, listener8017 absent, guesttab16 closed, viewport reset. Documentation write was briefly blocked by usage-limit approval review and resumed after recovery, without credit reset.

Remaining: pointer hover/active, retry button normal text contrast, other invalid/legal states, calendar and full37/U01–U12 acceptance. This is a bounded focus repair, not full acceptance.
