# Phase100l - current Litica noci / Podvodna tisina matrix

Audit on application commit17cdfa7. Sixteen current states: two designs, blog/detail,320/390/768/1440. This is a completed measurement batch with open findings, not a claim that these designs pass the final matrix. Application code is unchanged.

## Fixture and evidence

Isolated `.qa100e.sqlite3`: authors2411 `qa100l_litica_noci` and2412 `qa100l_podvodna_tisina`, posts13/14, reader2399 and an author reply on each. Factory preferences and native photographic backgrounds, long post title, two paragraphs. Bootstrap loaded. Both comments present in all16 states. Full numerical observations are in `phase100l_litica_podvodna_measurements.json`.

Foreground alpha/opacity and ancestor background alpha were composited. A solid body background was used only below the photographic `body::before` region. Where that pseudo-element intersects the text and no opaque ancestor isolates it, contrast is explicitly null/photo=true. Numbers in its `bg` field are only the solid fallback and MUST NOT be used as photographic contrast. This avoids the earlier error of treating transparent desktop cards as solid. Header/subtitle and several calendar/post zones therefore remain unresolved pending actual pixel evidence. Subtitle opacity0.82 is included.

## Confirmed new findings

1. **P1 Podvodna mobile comment-author**: #0d6efd over the composited comment background rgb(17.96,23.84,36.04) is3.952:1 at320/390, blog/detail. Text is16px, so below4.5:1. Both visible author links use the blue styling. Existing Phase84f2 correction applies only at min-width768px. Its historical mobile4.52 claim does not describe this current shared comment surface. Next narrow fix: extend the theme author color to the mobile comment links and verify both authors/all four widths without overriding other designs.
2. **Tablet calendar overflow in both designs**: at768 the grid client width is117px while scrollWidth is168px (+51px); calendar-box itself overflows35px. Grid tracks include a44px active-day minimum inside seven columns, plus gaps, in a narrow three-column layout. Screenshot confirms days crossing the calendar box into the gutter. Document overflow remains0 and is insufficient proof. Repair container/breakpoint layout while preserving44px interactive targets; do not shrink the active day back below the target.
3. **Desktop targets remain small**: like25.33px high, comment action21px, navigation30x30, active day28.33x35.36, archive32.93px high. Phone/tablet sampled interactive controls meet44px height (active day45.76 after transform). Normal noninteractive dates are not touch targets.

## Proven contrast outside photographic zones

All numbers apply to both blog and detail for the stated widths. F means photographic and not proved, not failure or pass.

| Element | Litica320/390 | Litica768 | Litica1440 | Podvodna320/390 | Podvodna768 | Podvodna1440 |
| --- | --- | --- | --- | --- | --- | --- |
| Post title |19.68|F|F|18.49|F|F|
| Body |16.43|F|F|15.92|15.92|F|
| Post author |4.67|F|F|4.51|4.51|F|
| Like / comment action |4.67|4.67|F|4.51|4.51|F|
| Comment text |14.64|5.68|5.68|13.96|5.37|F|
| Comment author |14.81|5.75|5.75|**3.95**|5.37|F|
| Guest hint |12.52|12.52|12.52|12.10|12.10|12.10|
| Active calendar day |12.77|F|F|12.10|12.10|F|
| Archive |16.62|16.62|F|15.92|15.92|F|

Blog title/subtitle are photographic at all widths. Litica ordinary day320 intersects the end of the photo by a fraction of a pixel, so remains conservatively F;390 is16.43. Podvodna ordinary day320/390/768 is15.92. Calendar navigation: Podvodna320 is7.06; the other sampled cases intersect photographs. A near-threshold4.51 action ratio has little margin and does not prove desktop photographic contrast. Podvodna first desktop comment begins within the864px photo region, so historical5.37 against the flat body cannot establish its actual contrast.

## Layout and safe interaction

Document overflow0 in all16 states. Sampled title, post card, comment bodies and content column have no local overflow; only768 calendar-box/grid findings above. Desktop preserves the photographic three-column identity; mobile stacks columns.768 retains a very narrow three-column arrangement, documented by the calendar failure.

At390 both designs passed previous month (empty September), next month, active October10 day, archive month, `Otvori post`, and `Komentari (2)` clicks. Canonical detail retained both comments. No likes or comments submitted. Phone Podvodna comments and both desktop photographic layouts visually inspected; tablet calendar screenshot confirms overflow.

## Status and next work

Current batch coverage now includes13 of37 designs (first9, Studio/Magazin, these2), with explicit open defects and photographic verification gaps. The other24 special designs still require current batches; factory Default needs a complete nonlegacy pass. This is not13 passing designs and does not close the full goal.

No application change, so no duplicate full suite: last validation on this unchanged application commit is Phase100k check/migration and214 passing tests. `git diff --check` passed. Synthetic fixtures retained for the next fixes; QA server8017 and browser stopped at end. Original repository/database/media, port8000, main and deployment untouched.
