# Phase100m - Podvodna mobile comment-author contrast

## Change

Phase100l measured mobile comment-author links at3.952:1. The existing Podvodna-only #d5e5ff author-link rule now applies at every width instead of only min-width768px. It uses the existing theme body color on the mobile comment surface. No shared CSS or other design is changed. Tablet/desktop declarations are unchanged in effect.

## Browser verification

Before evidence: Phase100l eight Podvodna blog/detail states on45e0915. After: same isolated `.qa100e.sqlite3`, author2412, post14, reader2399 and author reply, native photograph, Bootstrap; blog/detail320/390/768/1440.

- At320/390 both author links compute rgb(213,229,255). Their surface is color(srgb 0.835294 0.898039 1 / 0.08) over body#010611, giving effective rgb(17.96,23.84,36.04) and **13.961:1**, improved from3.952:1. Both comments remain below the photographic pseudo-element.
- At768 the existing color and measured5.369:1 are unchanged.
- At1440 the existing color is unchanged. First comment intersects the photographic area; actual pixel contrast remains an open100l item. The solid fallback ratio is not claimed as desktop proof.
- Document overflow0 in all eight states. Existing768 calendar-box+35px/grid+51px remains open. No new sampled title/card/comment overflow.
- Safe `Otvori post` then `Komentari (2)` clicks at390 reached canonical detail with both comments. Both visible author links and surfaces were checked, screenshot visually inspected. No mutating action submitted.
- Litica mobile author links retain their original rgb(214,230,255), confirming the local theme boundary.

QA server8017/browser stopped. Synthetic fixtures retained; source repository, source database/media and port8000 untouched.

## Validation

System check and migration drift checks passed. The first full run had one failure in the old Phase84f2 test that explicitly required a desktop-only media query; the other213 tests passed. That existing contract test now checks the all-width rule and retains isolation assertions for Litica/default. No application change was needed after browser verification. Final full suite:214/214 passed in127.509s. Existing missing collected-static directory warning only. `git diff --check` passed.

## Remaining work

This closes the confirmed mobile author-link P1 only. Both100l tablet calendar overflows are next, followed by unresolved photographic contrast, remaining24 special-design current batches, complete factory Default verification and desktop targets/user pages. The37-design goal is not complete.
