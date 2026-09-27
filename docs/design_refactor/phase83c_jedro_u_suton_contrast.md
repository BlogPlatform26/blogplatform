# Phase 83c — `jedro_u_suton` contrast stabilization

## Scope

This narrow remediation covers the post author, post actions, archive links and
comments identified by the Phase 83a audit. The photographic sunset and the
existing maritime character remain visible; titles, layout and unrelated
sidebar content are unchanged.

## Change

- Post author/action rows and archive links use an opaque deep-navy surface with
  warm, light action text.
- Comment cards use the existing opaque mobile parchment palette at every
  viewport, making their contrast independent of bright and dark photo zones.
- The shared mobile exception and its colours remain unchanged.

## Verification contract

The focused regression test renders the blog and post-detail routes, verifies
the local opaque-surface contract, confirms the existing mobile palette, and
ensures an unrelated bespoke design does not receive these rules.

An isolated copy of the Phase 76 trial database supplied a synthetic author,
reader, published post and two comments. The blog and post-detail routes were
checked at 320, 390, 768 and 1440 px. Computed opaque-surface contrast was
11.57:1 for author/action/archive text, 15.43:1 for desktop comment text and
8.50:1 for desktop comment-author links. The unchanged mobile palette measured
17.69:1 for comment text and 7.59:1 for comment-author links. A real `Otvori
post` navigation click reached the detail route, and none of the four widths
produced document-level horizontal overflow.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 64/64 tests.

This is one narrow remediation from Phase 83a. It does not complete the visual
audit of all 37 designs.
