# Phase 73: bespoke title and box editor hooks

## Scope

Phase 73 closes the remaining live-editor title gaps in the six bespoke designs:

- `ponocna_elegancija`
- `ruzicasti_vrt`
- `stara_aleja`
- `staza_prema_vrhovima`
- `jedro_u_suton`
- `misticno_jezero`

The change is deliberately limited to blog-page titles and visible box titles. Body text styling and the existing post-title/date contracts are unchanged.

## Implementation

- Each visible blog heading now exposes the shared `blog-page-title` semantic class.
- Profile, calendar, archive and custom-box headings expose the shared `box-title` semantic class.
- The analytics heading continues to use its existing `sidebar-box-title` shared hook.
- Bespoke CSS consumes `--blog-title-*` and `--box-title-*` variables while retaining each design's previous values as fallbacks.
- Long unbroken blog names are constrained with `max-width: 100%` and `overflow-wrap: anywhere` so enlarged editor values cannot widen the page.

## Regression coverage

The render matrix checks all six designs, every visible box-title type, the analytics hook and emitted editor variables. The live-editor workflow test covers save, reset-all, template isolation and isolation between two users.

Final automated results:

- targeted title/editor tests: 21/21 passed
- complete Django suite: 31/31 passed
- `manage.py check`: no issues
- `makemigrations --check --dry-run`: no changes detected

## Browser smoke test

An isolated copied database and isolated server on port 8049 were used; the original database, media and port 8000 were not touched.

The desktop sweep passed for all six designs. Saved values reloaded with the expected computed styles: blog title Tahoma / `#123456` / 61 px and profile, calendar, archive, custom and analytics box titles Verdana / `#654321` / 23 px. Required boxes remained visible and body colours stayed design-specific.

The initial 390 px mobile sweep also confirmed the semantic targets, computed custom styles and visible box content for all six designs. It exposed overflow from deliberately long, unbroken names at 61 px in four designs. The local `max-width`/`overflow-wrap` safeguard was added afterward. A second narrow browser measurement could not be completed because the isolated development server had already stopped, so the final overflow safeguard is covered by code review and the automated render contract, not a post-fix browser measurement.

## Operational boundaries

No migration or data transformation is part of this phase. The temporary browser database is disposable; the original `db.sqlite3` remains unchanged. This phase does not include merge, pull request or deployment work.
