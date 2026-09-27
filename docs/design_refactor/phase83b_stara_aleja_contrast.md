# Phase 83b — `stara_aleja` contrast stabilization

## Scope

This phase changes only the local `stara_aleja` presentation. The photographic
background and the established old-world visual identity remain visible, while
text that previously depended on the brightness of the photograph now sits on
an opaque, predictable surface.

## Change

- Blog and post titles use an opaque parchment surface while retaining their
  existing editor-controlled colour variables.
- Author metadata and post actions use an opaque dark-brown surface; nested
  links are explicitly warm and no longer inherit the generic blue link colour.
- Desktop/tablet comment cards use the same opaque dark-brown family already
  established by the mobile exception. Comment text, timestamps and links have
  explicit high-contrast colours.
- The shared mobile comment exception is unchanged.

## Verification contract

The focused regression test renders both the blog and post-detail routes and
checks the local surface/link contract. It also verifies that the mobile
exception remains present and that another bespoke design does not receive the
Stara Aleja rules.

An isolated copy of the Phase 76 trial database supplied a synthetic author,
reader, published post and two comments. Both the blog and post-detail routes
were exercised at 320, 390, 768 and 1440 px. Computed opaque-surface contrast
ratios were 7.87:1 for the blog title, 8.33:1 for the post title, 13.07:1 for
author/action links and 14.42:1 for comment text. A real `Otvori post`
navigation click reached the detail route. None of the four viewports produced
document-level horizontal overflow.

Final gates: `manage.py check` reported no issues, `makemigrations --check
--dry-run` reported no changes, and the full Django suite passed 61/61 tests.

This is one narrow remediation from the Phase 83a audit. The remaining 28
designs still do not have a complete equivalent visual audit.
