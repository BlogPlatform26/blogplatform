# Phase 84f4c — `planine_u_magli` hero contrast

## Scope

This phase closes the photograph-dependent desktop title/tagline finding from
Phase 84f4a. It does not change the photograph, mobile presentation, typography
scale, card layout or Phase 84f4b contrast rules. Tablet touch sizing and the
numeric width discrepancy remain separate P2 work.

An isolated migrated SQLite database used a fresh author with empty design
preferences, one published post and one reader comment. Real-browser checks
covered blog and post-detail at 320, 390, 768 and 1440 px.

## Implementation

At widths of 992 px and above, the existing central header column receives an
opaque, cold mist surface (`#edf1f4`) with a restrained blue-grey border,
20 px radius and soft shadow. Title and tagline use the Phase 84f4b mountain
slate (`#43566c`) without a text shadow. This makes contrast independent of
both bright sky and dark mountain pixels while leaving the panorama exposed
around the compact card.

The selector is deliberately scoped through
`html body .blog-header-main` so the design-local rule wins over the later
shared header component without affecting another design.

## Browser evidence

- Before: title/tagline sat directly on the photograph; their effective
  contrast changed with crop and pixels. The fallback-colour calculation of
  5.22:1 was not a reliable photographic measurement.
- After: actual title and tagline are `#43566c` on the opaque `#edf1f4`
  surface, measured at **6.64:1** on both blog and detail desktop renders.
- Mobile/tablet at 320, 390 and 768 px retain the original transparent header,
  original slate (`#5b6877`) and original layout.
- The 84f4b card colours remained present across all eight states: author and
  actions keep their 7.17:1 contract; comments remain at least 5.96:1.
- No visible non-Leaflet element crossed the viewport. The isolated fixture
  continued to report the known numeric tablet discrepancy (12 px in this
  run) without a visible escaping element.

Desktop visual inspection confirmed that the mountain panorama remains the
dominant composition. Safe navigation at 390 px passed for “Otvori post” and
previous month; no mutating control was exercised.

## Automated verification

A narrow render-contract test checks the surface, scoped selector and
blog/detail output and confirms isolation from `nebeski_mir`. Django system
checks, migration drift and the complete test suite are the final gate.

## Remaining work

- P2: post-action touch targets at 768 px.
- P2: isolate the tablet numeric width discrepancy before changing geometry.
- Phase 84f: audit `nebeski_mir`.
