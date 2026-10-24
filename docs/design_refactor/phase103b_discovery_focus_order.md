# Phase103b — main content before support in source

Baseline6ace0d7. Previous turn103a was progress. Fork inactive, worktree clean, fresh capacity27% five-hour/20% weekly consumed. No parallel writer.

## Change

Move the existing main column, including its single inherited content block, before the left column in base.html. A low-specificity left-column order:-1 retains the prior visual arrangement; discovery phone left order0 keeps main first. Existing more-specific Base tablet order rules remain effective. No JavaScript rearrangement or positive tabindex is required. Shared-base source order intentionally becomes main,left,right, including blog pages; this improves main-content priority but is not a full accessibility acceptance of every route.

## Browser evidence

Home featured and search qa102y/posts, plus representative dark blog qa100e_dark and post10 detail, at320/390/768/1440. Twelve search/blog/detail before/after column rectangle sets match exactly, document overflow0. Home initial immediate samples were unstable: .post-title has a0.3s transition and viewport changes produced intermediate line heights. They are retained as diagnostic raw evidence, not accepted regression measurements. Rechecked original template after restarting QA, used bounded repeated geometry reads to settle, then restored edited template and restarted.320/390/1440 settled home column rectangles match;768 after a fresh load matches the original settled768 exactly (main height5691.625). All final home document overflows0. The recheck files supersede initial home rectangles. No claim of universal identical fill or all37 regression coverage.

Eight real Tab actions from Registration reach Istaknuti postovi on home or Sve on search, at all four widths. Previously the support radio received focus. Focusable controls remain native elements. Safe Korisnici click preserves q=qa102y and reaches scope=users. Screenshot C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase103b-search-focus.png is390 requested viewport, not full page; shows the visible focus outline on Sve and was inspected.

Raw files consolidated in phase103b_measurements.json include original transient samples, settled rechecks, fresh768 result and focus outcomes. QA used isolated .qa100e.sqlite3/8017 only. No database/content mutation.

## Acceptance boundary

This closes the recorded source/focus priority defect, not every focus path, modal, keyboard interaction or user workflow. Remaining U01 gradient contrast, empty following/owner distinctions and tablet secondary-card usability continue with the photo/default/target and U02–U12 queue. No restart of37-theme audit.

## Validation
Django check and migration dry-run green. Full219 tests passed in169.126s, including two rendered-response tests requiring filters before support without JavaScript. No schema change.
