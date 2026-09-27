# Phase 83f — mobile post-action touch targets

## Scope

Phase 83f adds one shared mobile contract for the interactive controls rendered
by `post_actions.html`: the like button, comments link and blog-list
`Otvori post` link. At widths up to 575.98 px each receives a minimum 44 px
height. View count and restricted-state text remain non-interactive and are not
artificially enlarged.

The change is structural only: it preserves each design's local colour,
background and typography. Existing comment edit/delete targets are unchanged,
and 768/1440 layouts remain outside the new media query.

## Baseline

In isolated browser renders, both shared `default` and bespoke `magazin`
examples measured 25.33 px for the like button and 21 px for post-action links
at 320 and 390 px. The same compact dimensions appeared on blog and post-detail
routes and remained appropriate for 768/1440 desktop-style layouts.

## Regression contract

Registry-wide coverage renders every registered design and verifies that the
shared mobile selector contract is present. A separate assertion confirms the
post-detail comments link uses the same action markup.

## Browser result

After the change, both representative render systems measured exactly 44 px
high for the like button, comments link and `Otvori post` link at 320 and
390 px, on both blog and post-detail routes. Their original 25.33/21 px
dimensions remained unchanged at 768 and 1440 px. None of the sixteen checked
route/design/viewport combinations produced document-level horizontal
overflow.

A keyboard Tab step moved focus from the comments link to `Otvori post`, and a
real click reached the canonical post-detail URL. No like action or other data
mutation was performed.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 68/68 tests.

This phase does not change tablet/desktop post actions or complete the visual
audit of all 37 designs.
