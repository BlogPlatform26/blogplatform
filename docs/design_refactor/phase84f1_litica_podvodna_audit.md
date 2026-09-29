# Phase 84f1 — `litica_noci` and `podvodna_tisina` audit

## Scope and method

This docs-only audit covers two registered bespoke designs: `litica_noci` and
`podvodna_tisina`. An isolated migrated SQLite copy contained one author, one
published post, one reader comment and current-month calendar/archive data per
design. Real Edge renders covered blog and post-detail at 320, 390, 768 and
1440 px (16 states). No source data, media or mutating control was used.

Contrast was calculated from computed foregrounds and composited rendered
background colours. Desktop screenshots were also inspected to distinguish
text protected by opaque/translucent content surfaces from text whose result
would depend on a photograph. All measured post, comment, calendar and archive
text below sits on a defined dark or grey surface; none of the reported ratios
depends on sampling a particular photograph pixel. The large photographic hero
regions remain visually intact and contain only the already-readable white blog
title in the checked fixtures.

## Results

Ratios are the minimum across blog/detail and all four widths.

| Design | Author | Action | Comment | Comment author | Calendar | Archive | Overflow |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `litica_noci` | 16.62 | 4.67 | 5.68 | 5.75 | 12.77 | 16.62 | none |
| `podvodna_tisina` | 15.92 | 4.51 | 5.37 | **1.52 desktop** | 12.10 | 15.92 | none |

The unauthenticated comment hint (“Za komentiranje je potrebna registracija.”)
is a separate confirmed failure: approximately **1.36:1** in `litica_noci` and
**1.31:1** in `podvodna_tisina` on the desktop dark surface. It inherits
Bootstrap's dark muted colour rather than a design-aware light muted colour.

No document overflow or visible component overflow was found in any of the 16
states. At 320/390, post-action links, calendar navigation, post days and
archive links are at least 44 px. At 768, calendar navigation/days/archive stay
at least 44 px, while post-action links are 21 px. At 1440, compact desktop
controls measure 21 px for post actions, about 30–35 px for calendar controls
and 32.9 px for archive rows.

Safe “Otvori post” and previous-month links succeeded for both designs. No
like, save, publish or delete action was exercised.

## Priority

### P0

None. All routes and safe navigation worked, content remained reachable and no
overflow was found.

### P1

1. `podvodna_tisina`: give the desktop comment-author link a design-local light
   cyan/white colour on the grey comment card; current blue is 1.52:1.
2. Both designs: override `.small.text-muted` only inside the comment area with
   a light muted ink that reaches 4.5:1 on the dark surface.

### P2

1. Extend post-action touch targets through 768 px for these bespoke designs;
   the links are currently 21 px high at tablet width.
2. The action-link ratios (4.67:1 and 4.51:1) technically pass but have little
   margin. Recheck them when changing either design's blue accent or surfaces.

## Smallest next fixes

Start with a `podvodna_tisina`-scoped desktop comment-author colour and a narrow
contract test. Follow with one shared, comment-area-only muted-hint override if
the same light ink is confirmed on both dark surfaces. Keep the tablet target
change separate because it is a geometry concern.

The remaining Phase 84f designs (`vodopad_u_magli`, `planine_u_magli`,
`nebeski_mir`) and the other unaudited registered designs remain open.
