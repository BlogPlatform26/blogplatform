# Phase100s — current Vodopad / Planine matrix

Application baseline43d6962. Sixteen current states: vodopad_u_magli and planine_u_magli, blog/detail at320/390/768/1440, Bootstrap loaded, factory preferences, native photo, long post title, two paragraphs and two comments. Synthetic authors2431/2432 (qa100s_vodopad_u_magli / qa100s_planine_u_magli), posts29/30, reader2399. Fixtures remain in isolated .qa100e.sqlite3.

This is a completed audit batch with open defects, NOT a whole-design pass. No application code changed.

## Confirmed findings

- Timestamp contrast below4.5:1 in both themes. Vodopad phone3.955, tablet3.467 and second desktop3.467. Planine phone3.941, tablet3.419 and second desktop3.419. First desktop timestamp is photo-dependent and unresolved. Both comments measured; blog/detail match.
- Long post title local overflow at320: Vodopad57px, Planine81px; Planine390 also11px. Document overflow0 in all16 states does not close these local failures.
- Comment text local overflow at320: Vodopad7px, Planine9px. Needs cause confirmation before change.
- Tablet768 calendar: Vodopad grid+52px/box+36px; Planine grid+64px/box+46px. Screenshot visually confirms calendar columns crossing into the content gutter. Preserve seven-day semantics and44px active targets when fixing layout. This single-post fixture does not prove dense-week behavior.
- Desktop targets remain small: like25.33px high, action links21px, month navigation30x30px, archive32.93px, active date28.33x35.36 Vodopad /26.84x37.44 Planine. Phone/tablet sampled action and calendar targets are>=44px.
- Planine desktop subtitle calculated4.347:1 after opacity over opaque header surface; confirm actual font/weight and child styling before deciding the fix. Vodopad desktop subtitle4.682:1.

## Contrast evidence and limitations

Raw computed colors, all ancestor backgrounds/opacity, photo height, geometry, local overflow and target dimensions are in phase100s_vodopad_planine_measurements.json. Derived contrast is in phase100s_vodopad_planine_results.json. Photo/gradient-dependent values are null, not passes or failures. Solid fallback alone is never photographic evidence. The conservative analyzer leaves unresolved backgrounds with gradients, even when an older phase claimed a pass; resolve those against their actual layers rather than inferring regression from null.

On solid phone surfaces, Vodopad post title7.085/body5.327/author and actions7.684/comment author5.284/comment text6.927; Planine title4.772/body5.308/author and actions7.171/comment author6.470/comment text6.433. Tablet comment text7.935/7.252 and author6.053/7.294 respectively. Guest hints6.435/6.599 on all sampled widths. These establish only the sampled elements and backgrounds, not all photo zones.

## Interaction, cleanup and next steps

At390 safe post-open clicks reached canonical posts29/30, each retained both comments. No like/comment submissions. Planine320/768 screenshots inspected for narrow layout and tablet overflow; screenshot coordinates are not used for contrast calculations. QA tab closed, viewport reset and server8017 stopped. Synthetic DB retained; original repo,DB,media,port8000 untouched.

No application changes, so latest Phase100q check/migration/214-test pass still applies; duplicate full suite not run. git diff --check passed. Next: close confirmed timestamp contrast, then narrow title/comment overflow and dense calendar layout in fully verified mini-phases. Continue remaining22 special designs and full factory Default; photographic proofs, desktop targets and user pages remain open. Current coverage15/37 is not15 passing designs.
