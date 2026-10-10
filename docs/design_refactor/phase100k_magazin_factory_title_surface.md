# Phase100k - Magazin factory title contrast and wrapping

## Problem and change

Phase100j confirmed white factory title contrast of approximately1.44-1.74:1 over the system photograph. The factory white title now has an opaque #2f271f surface matching the existing tagline caption, with a6px visual surround and no text shadow. Its computed white-on-surface contrast is14.68:1, independent of the photograph. The surface applies only when title color is absent or factory #ffffff; explicit nonwhite user title colors retain their previous transparent surface and color. This does not promise accessibility for arbitrary custom palettes.

Long-title testing additionally reproduced53.39px of tagline/post overlap at320px. The hero overlay now participates in a shared grid with the image, so its content contributes to hero height. Bottom spacing reserves the existing118px desktop /56px mobile post overlap plus28px breathing room. The title can wrap unbroken tokens. Normal short-title geometry and image bounds remain unchanged; long headers grow as needed.

## Browser evidence

Isolated `.qa100e.sqlite3`, author2402, post12, two comments, selected `soho_sunrise_valley` system photograph; actual Bootstrap loaded. Before evidence is the complete eight-state Phase100j series on parent application code. After final changes, blog and detail320/390/768/1440 all show14.6765:1, loaded photograph naturalWidth1600, both comments, zero document/title-local overflow and zero tagline/post overlap. Title position/width and image geometry match the Phase100j measurements (accounting for the recorded scroll offset).

Additional checks:

- 61-character spaced title: eight blog/detail states across the four widths; title heights175.99/105.59/70.40/35.20px. No sampled overflow or overlap; contrast14.68:1 throughout. At320 the photo remains210px high while the hero expands below it to hold the caption and clearance; visually inspected.
- 64-character unbroken title: blog at all four widths, zero document/title overflow and zero overlap; wraps to175.99/140.79/70.40/70.40px.
- Explicit #123456 title color: blog320/1440 preserves computed rgb(18,52,86), transparent title background and zero local overflow. Not claimed as a contrast pass.
- Safe `Otvori post` and `Komentari (2)` clicks at390 reach canonical detail and retain both comments; no likes/comments submitted.
- Desktop normal title and phone long title visually inspected. Synthetic title and raw saved preferences restored afterwards; QA server8017 and temporary browser closed after verification.

## Validation

System check passed; `makemigrations --check --dry-run` reported no changes. All214 tests passed in135.452s; the existing missing collected-static directory warning remains. `git diff --check` passed. No source repository/database/media/port8000 changes, no main/merge/deploy.

## Remaining scope

This closes the factory Magazin photo-title P1 and the reproduced long-title overlap. It does not complete desktop touch targets, remaining26 special-design matrix batches, factory Default full verification, historical local overflow findings or the whole37-design goal. Existing100i Studio/Magazin post-title fix and100h Studio contrast fixes remain valid separate evidence.
