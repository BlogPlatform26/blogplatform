# Phase103v — phone legal content and navigation

On all three legal pages, phone content began at y402.521 below the sidebar and its90px top margin; links were21px high. Route-scoped CSS below768px now places the main content first, removes that sidebar top margin and gives links48px height. Desktop and tablet rules are untouched.

Twelve paired guest states: terms, privacy, content rules at320/390/768/1440. Phone content now starts y114.188. Document and sampled local excess0 before/after. All sampled rectangles/fonts/fills/backgrounds at768/1440 are identical. Twelve after states have no consecutive content or sidebar-link overlaps. Content backing resolves through transparent ancestors to opaque white BODY, with no ancestor background image. Actual text fills are retained; no rendered-pixel contrast claim. Native Enter follows sidebar links to each of the three canonical routes at390px. This is link activation proof, not a complete sequential Tab-order audit.

Raw evidence in C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-legal: baseline.json, after.json, backing-overlaps.json, navigation.json, tests.txt. Inspected phase103v-legal-phone.png:390px viewport of content rules, not the whole document. Initial screenshot attempt failed; subsequent capture succeeded.

Full suite231 tests50.958s; check and migration check green. No database/content/email mutations. U12 support/bug-report validation, tablet/desktop link target sizes and full keyboard audit remain open. Legal wording was not changed or audited for legal correctness.
