# Phase 70 — Broad design/editor/calendar/archive audit

## Scope and method

Read-only audit of all 37 authoritative `Profile.TEMPLATE_CHOICES` at
`62d04fe90428c1766620401d2b38c860a6f37f54`. A fresh migrated
`db_browser_phase70.sqlite3` contained one user, published post, tall left/right
custom boxes, both archive modes, analytics, and explicit design values per
registry key. Port 8046 and a temporary browser tab were used; the original
database/media and port 8000 were untouched.

The new checks were stricter than the Phase 42–69 presence matrix:

- server-side: 111 renders (37 designs × `both`/`calendar`/`list`), exact
  calendar/archive visibility and user-blog query route preservation;
- browser: all 37 at 1440×900 and 390×844, visible title/post/body/boxes/date,
  computed customization colors, one primary date representation, author
  timestamp, column top alignment, horizontal overflow, and enabled analytics;
- existing editor UI evidence was reused only for already-proven shared/right,
  simple-background, Magazin, and Nebeska families; newly weak bespoke targets
  were judged from fresh persisted values and computed public DOM.

Legend: **P** pass; **B** blog-title color not reaching visible title; **X** box
title color not reaching visible custom box; **T** body text color not reaching
visible post body; **D** bespoke card has a native fixed date and does not expose
the selectable shared date-style representations; **A** archive-mode defect.

## 37/37 matrix

| Design | Family | Blog/post title | Box/body | Date + author | Calendar/archive | Desktop + 390 |
| --- | --- | --- | --- | --- | --- | --- |
| default | shared-left | P / P | P / T | P | P | P |
| dark | shared-left | P / P | P / T | P | P | P |
| classic | shared-left | P / P | P / T | P | P | P |
| default_right | shared-right | P / P | P / T | P | P | P |
| dark_right | shared-right | P / P | P / T | P | P | P |
| classic_right | shared-right | P / P | P / T | P | P | P |
| simple_pattern | simple | P / P | P / P | P | P | P |
| simple_image | simple | P / P | P / P | P | P | P |
| simple_retro | simple-retro | P / P | P / P | P | A | P |
| soho | special shared-date | P / P | P / P | P | P | P |
| magazin | special shared-date | P / P | P / P | P | P | P |
| litica_noci | shared theme | P / P | P / P | P | P | P |
| podvodna_tisina | shared theme | P / P | P / P | P | P | P |
| vodopad_u_magli | shared theme | P / P | P / P | P | P | P |
| planine_u_magli | shared theme | P / P | P / P | P | P | P |
| nebeski_mir | shared theme | P / P | P / P | P | P | P |
| svemirski_horizont | shared theme | P / P | P / T | P | P | P |
| zlatni_horizont | shared theme | P / P | P / T | P | P | P |
| iznad_oblaka | shared theme | P / P | P / T | P | P | P |
| sumska_svjetlost | shared theme | P / P | P / T | P | P | P |
| polarna_svjetlost | shared theme | P / P | P / T | P | P | P |
| zlatno_polje | shared theme | P / P | P / T | P | P | P |
| neonski_grad | shared theme | P / P | P / T | P | P | P |
| polje_lavande | shared theme | P / P | P / T | P | P | P |
| carobna_ljubicasta | shared theme | P / P | P / T | P | P | P |
| kraljevska_pozornica | shared theme | P / P | P / T | P | P | P |
| dimni_akordi | shared theme | P / P | P / T | P | P | P |
| nebeska_klasika | special shared-date | P / P | P / T | P | P | P |
| ponocna_elegancija | bespoke special | P / P | X / T | D + author P | P | P |
| ruzicasti_vrt | bespoke special | B / P | X / T | D + author P | P | P |
| stara_aleja | bespoke special | B / P | X / T | D + author P | P | P |
| staza_prema_vrhovima | bespoke special | B / P | X / T | D + author P | P | P |
| jedro_u_suton | bespoke special | P / P | X / T | D + author P | P | P |
| misticno_jezero | bespoke special | B / P | X / T | D + author P | P | P |
| sjene_ulice | shared theme | P / P | P / T | P | P | P |
| mjesecev_ples | shared theme | P / P | P / T | P | P | P |
| asfaltni_plamen | shared theme | P / P | P / T | P | P | P |

## Strong passes

- 37/37 HTTP/render, post title customization, custom left/right box presence,
  primary-date count, author timestamp, calendar/archive routes, and desktop/mobile
  visibility.
- 37/37 with analytics explicitly enabled: widget visible, no unexpected desktop
  column top delta, no mobile element beyond 390 px, and document/body overflow
  `0 / 0`.
- Shared date cards: ribbon selected, only inline representation visible; no
  main/inline overlap. Native bespoke dates render only their one fixed element.
- Browser console: zero warnings/errors during the final two sweeps.

## Ranked gaps and smallest safe follow-ups

### Important — Phase 71: six bespoke date/editor contracts

`ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`,
`staza_prema_vrhovima`, `jedro_u_suton`, and `misticno_jezero` render a fixed
`d.m.Y` element rather than the shared main/inline shell. The editor still
offers all date styles, so saved style/effect/scale values do not control those
visible dates. Convert only these six card headers to the shared date contract,
retaining each design's wrapper class/fallbacks, then add computed-style tests.

### Important — Phase 72: bespoke title/box semantic hooks

Persisted `#123456` failed on the visible blog title in four designs
(`ruzicasti_vrt`, `stara_aleja`, `staza_prema_vrhovima`, `misticno_jezero`).
Persisted `#345678` failed on custom box titles in six designs (the same set as
Phase 71 except blog-title-pass designs `ponocna_elegancija` and
`jedro_u_suton`). Candidate cause is missing shared semantic classes and local
theme selectors winning the cascade. Add hooks locally; do not broaden global
selectors.

### Important — Phase 73: Simple Retro archive-mode branch

For `simple_retro`, `calendar` still rendered the archive list and `list` still
rendered the calendar. The unconditional special branch in
`blog_right_sidebar.html` is the root-cause candidate. Apply the same explicit
mode guards already used by other sidebar branches and test all three modes.

### Lower priority / clarify product contract — body text

Persisted body color reached the visible fixture body in only ten designs:
the three simple designs, Soho, Magazin, Litica, Podvodna tišina, Vodopad u
magli, Planine u magli, and Nebeski mir. It did not reach 27 designs (the six
base/right designs, fourteen later shared themes, Nebeska, and six bespoke
specials). The current live editor UI is title/date focused, so first decide
whether body color is a supported live-editor promise or only legacy design
data. If supported, audit `.blog-rich-content`/special body cascade before any
global override; otherwise remove the misleading inactive contract.

## Final gates

### Priority follow-up fixed during audit

The user screenshot exposed a separate live-preview repaint defect for
`boxed_number` + gradient at 170%. DOM inspection showed one primary shell,
one main representation, one inline representation, and one day/month/year;
the apparent copies were not DOM duplication. The live editor was applying
`transform: scale(...)` and gradient clipping to both `.blog-date-shell` and
every descendant, recursively multiplying scale and creating compositing
ghosts. The obsolete direct-style block was removed; CSS variables, semantic
classes, and the centralized date stylesheet now remain the sole renderer.
This preserves gradient and the 70–170% range without timers or repaint hacks.

- `python manage.py check`: 0 issues;
- `python manage.py makemigrations --check --dry-run`: no changes;
- complete existing Django suite: 27/27 passed;
- no application code was changed in Phase 70.
