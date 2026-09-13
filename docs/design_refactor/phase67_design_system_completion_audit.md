# Phase 67 — Design system completion audit

## Scope

This is a requirement-by-requirement audit of `design-refactor` at
`97ddb456cc8c9773db42b10d6d660132136bd142`. It uses the authoritative model
registry, permanent Django tests, committed implementation, and the existing
Phase 42–66 evidence. The already completed 37-design browser matrix was not
repeated. No production database, migration, media file, or application code
was changed by this audit.

## Active registry and design families

`Profile.TEMPLATE_CHOICES` is the authoritative registry and contains exactly
37 unique active keys. `ActiveDesignRenderMatrixTests` divides it into two
disjoint and exhaustive families and fails if the registry and family manifest
drift.

- Standard/shared (28): `default`, `dark`, `classic`, `default_right`,
  `dark_right`, `classic_right`, `simple_pattern`, `simple_image`,
  `simple_retro`, `litica_noci`, `podvodna_tisina`, `vodopad_u_magli`,
  `planine_u_magli`, `nebeski_mir`, `svemirski_horizont`, `zlatni_horizont`,
  `iznad_oblaka`, `sumska_svjetlost`, `polarna_svjetlost`, `zlatno_polje`,
  `neonski_grad`, `polje_lavande`, `carobna_ljubicasta`,
  `kraljevska_pozornica`, `dimni_akordi`, `sjene_ulice`, `mjesecev_ples`,
  `asfaltni_plamen`.
- Special/full-custom (9): `soho`, `magazin`, `nebeska_klasika`,
  `ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`,
  `staza_prema_vrhovima`, `jedro_u_suton`, `misticno_jezero`.

## Completion matrix

| Requirement | Evidence | Status |
| --- | --- | --- |
| Authoritative active-design count and family split | `Profile.TEMPLATE_CHOICES`; `ActiveDesignRenderMatrixTests.SPECIAL_DESIGNS`; Phase 42 registry-driven render matrix. The permanent test asserts 37 unique keys, disjoint families, no missing or extra key, template resolution, HTTP 200, post/body/comments/calendar/archive context, and active customization CSS. | PASS |
| Known CSS conflicts identified and corrected | Phase 46 / `1185e6e` scopes the terminal default body fallback so it cannot override `litica_noci`; Phase 55 / `a061b01` fixes Soho's mobile fixed-width columns; Phase 56 / `3207af7` removes Magazin's `100vw` overflow cause; Phase 63a / `c5a3b25` gives Magazin shared semantic editor targets; Phase 63c / `d54ba29` gives Nebeska semantic title/date targets with local CSS-variable fallbacks. Each fix has a permanent assertion or subsequent browser PASS. | PASS for all observed conflicts |
| Shared behavior without loss of special identity | The nine active special designs retain their own templates and per-design post-card partials. Those cards include the shared `post_body.html`, `post_actions.html`, and `post_comments.html`; their layouts use the centralized calendar, archive, profile-action, and restricted-note components introduced in Phases 38–41 (`9023cbc`, `ebd15f3`, `b200b04`, `ea807e1`). Phase 42 verifies the common render contract for all 37; Phases 55–59 verify the special DOM/layout/assets at both viewports. | PASS |
| Title/date editor save, reset, isolation, live preview, and CSS-variable application | Phase 61 / `fc2b768` permanently exercises save PRG, all 14 fields for all 37 designs, cross-template preservation, two users on the same design, and active-only reset. Phase 62 proves real-browser `default_right` live variables, UI save/reload, individual reset, reset-all, and mobile behavior. Phase 63a proves Magazin real DOM/computed targets and persistence; Phase 63c proves Nebeska actual UI save/reload/reset and its special date contract. | PASS |
| Background editor representative branches | Phase 64 / `3c82997` permanently covers allowed simple designs, pattern/retro modes, system image, upload, delete, reset, file removal, and template isolation. Phase 65 proves `simple_pattern` gradient/pattern live preview, persistence, reset, assets, and 390 px behavior. Phase 66 proves `simple_image` system image, isolated upload/delete, persistence, reset, assets, and 390 px behavior. | PASS |
| Every active design at desktop and 390 px | Standard/shared: Phases 43–45 and 47–54 cover all 28 at 1440×900 and 390×844 after the Phase 46 Litica correction. Special: Soho Phase 55, Magazin Phase 56, Nebeska Phase 57, three designs in Phase 58, and the final three in Phase 59. Phase 59 records the resulting 37/37 completion, including layout, key content, local assets, overflow, and browser error gates. | PASS |
| Django integrity gates | On 2026-09-13: `.venv\\Scripts\\python.exe manage.py check` reports 0 issues; `makemigrations --check --dry-run` reports no changes; the complete available Django suite passes 26/26 using a test database. | PASS |
| Repository handoff state | Before this document, local HEAD and `origin/design-refactor` were both `97ddb456cc8c9773db42b10d6d660132136bd142`, with a clean tree. After the documentation-only completion commit is pushed, the final handoff verifies a clean tree and equal local/remote SHA. | PASS at final handoff gate |

## Browser-controller limitation

Phase 63a, Phase 65, and Phase 66 record that the browser controller focused
and activated the visible submit control but did not dispatch the native form
POST. Those passes did not claim a successful click: they submitted the same
URL/view and form payload through Django's client against the same isolated
database, then used a real browser reload to verify stored controls, public
computed styles, assets, and reset results. Phase 62 and Phase 63c independently
contain successful real-UI POST/302/reload evidence. This is a smoke-tool
limitation, not an observed application failure, but future browser automation
should keep explicit network-log assertions around form submission.

## Residual risk and recommendation

The available evidence is strong enough to mark the design-system stabilization
scope complete. Residual risk is concentrated in browser/environment variance,
future registry drift, and the controller limitation above—not in a known
failing active design or persistence contract.

Use a controlled pull request or verified fast-forward from `design-refactor`
to the target branch. Before merging, review the complete target-branch diff,
run the same three Django gates in CI, and retain the registry matrix and editor
workflow tests as required checks. This audit does not perform a merge, PR
merge, database migration, or deployment.
