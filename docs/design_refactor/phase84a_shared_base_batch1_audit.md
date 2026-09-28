# Phase 84a — shared-base batch 1 audit

## Scope and method

This is a docs-only audit of nine shared-base design keys: `default`, `dark`,
`classic`, `default_right`, `dark_right`, `classic_right`, `simple_pattern`,
`simple_image` and `simple_retro`. It does not claim completion of the remaining
28 shared-base designs or all 37 registered designs.

An isolated migrated database contained one author, reader, published post, two
comments and archive mode `both` for each design. Real Edge renders covered both
blog and post-detail at 320, 390, 768 and 1440 px (72 page states). Contrast was
calculated from computed foregrounds and composited rendered backgrounds.
Document and local element bounds and the visible control dimensions were also
recorded. For every design, safe clicks opened the canonical post detail and
the previous-month query. No save, like, publish, delete or other content
mutation occurred. The original database, media and port 8000 were not used.

## Results matrix

Contrast values below are the lowest measured across blog/detail and the four
widths. `A/Ax` means post author/action, `C/Ca` comment/comment-author, and
`Cal` the post-bearing calendar day.

| Design | A / Ax | C / Ca | Archive / Cal | Overflow | Result |
| --- | ---: | ---: | ---: | --- | --- |
| `default` | 7.53 / 5.78 | 15.27 / 4.98 | 7.01 / 5.78 | none | pass |
| `dark` | 9.84 / 7.19 | 6.08 / **2.32** desktop | 11.01 / **3.53** | none | P1 |
| `classic` | 6.89 / 5.34 | 13.04 / 4.57 | 7.97 / 5.78 | none | pass |
| `default_right` | 7.53 / 5.78 | 15.27 / 4.98 | 7.01 / 5.78 | none | pass |
| `dark_right` | 9.84 / 7.19 | 6.08 / **2.32** desktop | 11.01 / **3.53** | none | P1 |
| `classic_right` | 6.89 / 5.34 | 13.04 / 4.57 | 7.97 / 5.78 | none | pass |
| `simple_pattern` | **3.57 / 3.57** | 6.75 / **3.19** | 4.98 / **3.26** | +18 px at 320/390; +10 px at 768 | P1 |
| `simple_image` | **3.57 / 3.57** | 6.75 / **3.19** | 4.98 / **3.26** | +18 px at 320/390; +10 px at 768 | P1 |
| `simple_retro` | **3.18 / 3.45** | 6.21 / **2.84** | 4.98 / **3.26** | none | P1 |

Blog and detail produced the same contrast and overflow result for each design.
The photographic `simple_image` variant therefore fails even before accounting
for any especially light or dark image region: its measured text treatment on
the rendered content surface is already below 4.5:1.

## Responsive and target evidence

- All nine designs keep post-action targets 44 px high at 320 and 390 px.
- At 768 px, post-action links shrink to 17 px (`default`, `dark`, their right
  variants, `simple_pattern`, `simple_image`, `simple_retro`) or 19 px
  (`classic`, `classic_right`). Calendar navigation, post days and archive
  links remain at least 44 px at 768 because of the existing shared tablet
  contract.
- At 1440 px, the compact desktop calendar/navigation controls are 27–40 px and
  archive rows 25.5–41.6 px; this is recorded as desktop density, not a new P1.
- The visible `simple_retro` sidebar controls were explicitly re-measured after
  excluding its hidden duplicate sidebar markup; mobile/tablet controls are
  present and at least 44 px.
- `simple_pattern` and `simple_image` overflow comes from
  `.calendar-box.calendar-box--simple`: document width is 338/408/778 at
  320/390/768 respectively. The problem disappears at 1440 px.
- No document or local overflow was found in the other seven designs.

## Priority

### P0

None found. Routes rendered, navigation worked and no content became
unreachable in the audited states.

### P1

1. **Simple-family contrast contract:** fix `simple_pattern` and `simple_image`
   together, then verify whether the same shared color selectors can safely
   cover `simple_retro`. Author/action, comment-author and active calendar-day
   contrast are all below 4.5:1.
2. **Simple calendar containment:** remove the repeatable 18/10 px overflow in
   `simple_pattern` and `simple_image` without changing desktop widths.
3. **Dark-family comment/calendar contrast:** correct desktop comment-author
   contrast (2.32:1) and the active calendar day (3.53:1) once in the shared
   dark contract, covering `dark` and `dark_right` together.
4. **Simple Retro contrast:** if it cannot safely share item 1, use a narrow
   retro-specific palette adjustment; its author/action/comment-author values
   are 3.18/3.45/2.84:1.

### P2

1. Extend the post-action 44 px target contract from mobile through 768 px for
   these shared-base layouts. This is separable from the contrast fixes.
2. After the P1 work, visually recheck long localized archive labels and custom
   boxes; the synthetic content used here intentionally exercised only the
   standard archive entry and comment structure.

## Suggested next smallest fix

Start with the shared containment rule for
`.calendar-box.calendar-box--simple`. It is the smallest measurable layout
change, affects exactly the two overflowing variants, and can be regression
tested independently before changing their palette. Follow with the shared
simple-family contrast contract as a separate phase.
