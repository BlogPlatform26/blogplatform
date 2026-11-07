# Onboarding tablet width and button targets

The onboarding page has empty sidebar blocks. Its inherited half-width tablet column squeezed the biography field to 182.046875px at 768px. A template-scoped 768–991.98px rule now uses the available main row and hides those empty columns. Wizard buttons have a 48px minimum height and width.

## Browser evidence

Baseline: `z/work/onboarding-skip-layout-recovered.json`. Final: `z/work/onboarding-tablet-targets.json`, copied from browser temporary storage to durable disk. Twelve final samples cover all three steps at 320, 390, 768 and 1440px. Each has document overflow 0, sampled control local overflow 0 and pairwise sampled control overlaps 0. Native Enter on Next traversed the steps without saving.

Paired first-step field widths are 207→207, 277→277, 182.046875→486.09375 and 398→398px respectively. All twelve paired first-step controls retain their sampled font, foreground fill and background values. Buttons intentionally grow from 38 to 48px at every width, including desktop. This is not blanket geometry or pixel identity. Transparent button backgrounds are not a new composited contrast proof.

`z/outputs/onboarding-tablet.png` is an inspected 768×900 viewport screenshot, not a full-page capture. QA server 83605 was stopped; tab4 was logged out and closed and viewport override reset after browser collection.

## Acceptance boundary

This closes the measured tablet width and wizard button targets. Earlier native hidden-step validation, incomplete-date skip recovery, full phone wizard Tab path, settings Tab path and owner long-question containment are documented separately. Broader U04 contrast/focus and remaining journey matrix requirements are not declared accepted by this change.

Validation: Django check clean; makemigrations --check --dry-run reports no changes; full suite 250 tests passed in 52.791s. Raw suite: z/work/onboarding-tablet-suite.txt.
