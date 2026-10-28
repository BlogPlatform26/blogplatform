# Phase103x — support controls

The shared support form now gives phone radio labels, title/email fields and submit a minimum 48px target below 768px. Text fields have explicit accessible names matching their placeholders. Textarea height remains 109.333px. No server behavior changed.

Evidence: C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-support/baseline.json and after-final.json are the paired 320/390/768/1440 measurements. after.json is intermediate, not final. Document and sampled local excess are zero; overlaps-final.json confirms no intersections between distinct controls (nested radio inputs excluded). At 768/1440 sampled control geometry, fill and background are unchanged. Phone field widths are 223.333/293.333px. The existing 94.688px tablet field width remains an open usability concern.

Native phone interaction selected Pitanje and empty submit focused title with valueMissing. No valid POST, email or saved support report was produced. Screenshot C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase103x-support-phone.png was visually inspected: scrolled 390px viewport, not the whole page. Browser capture raster is not a 1:1 DOM pixel measurement.

Validation: Django check and makemigrations --check --dry-run passed; 231 tests passed in 137.713s. Full output: z/work/u12-support/tests.txt. git diff --check passed.

## Remaining acceptance and scope clarification

User explicitly reaffirmed that functionality matters as well as appearance. Keep the full original goal and functional acceptance requirements. Do not narrow completion to visual layout or mark untested persistence/email flows passed. Group remaining work into coherent user journeys instead of reporting every small control as an independent completion.

Next support journey: tablet width usability, keyboard/error state presentation, and isolated server save/type/contact validation with in-memory email, followed by safe browser success/error evidence. Remaining 37-design, factory-default and U01–U12 requirements stay in remaining_verification_scope.md and phase102t_user_route_acceptance.md; historical closed fixes must not be repeated. This phase does not establish overall completion.
