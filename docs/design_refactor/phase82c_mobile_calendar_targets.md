# Phase 82c — Mobile calendar and archive touch targets

## Scope

Phase 82c adds one shared, mobile-only contract in `blog/templates/blog/base.html` for both calendar render systems. At viewport widths up to 600 px, interactive month arrows, post-bearing calendar days, and archive links receive a minimum 44 px touch height; month arrows and clickable days also receive a minimum 44 px width. The selectors cover all registered designs without changing their individual desktop rules.

The known cramped `default_right` sidebar at 768 px is intentionally unchanged and remains deferred to Phase 82d.

## Browser verification

Verification used an isolated copy of the database, synthetic published posts, and representative designs from both render systems: `default`, `default_right`, `simple_retro`, `magazin`, and `stara_aleja`.

| Design | 320 / 390 px after | 768 / 1440 px |
| --- | --- | --- |
| `default` | arrows and days 44×44; archive links 44 px high | unchanged |
| `default_right` | arrows and days 44×44; archive links 44 px high | unchanged, including known 768 px constraint |
| `simple_retro` | arrows and days 44×44; archive links 44 px high | unchanged |
| `magazin` | arrows and days 44×44; archive links 44 px high | unchanged |
| `stara_aleja` | arrows and days 44×44; archive links 44 px high | unchanged |

No horizontal document overflow appeared at 320, 390, 768, or 1440 px. Two adjacent interactive days measured 44×44 with a 6 px horizontal gap, confirming that the larger targets do not overlap.

Safe-click checks passed for previous/next month navigation, a multi-post day, an archive month, and a single-post day that opened the canonical post URL.

## Regression coverage

`CalendarMobileTargetsContractTests` renders every registered design and verifies that the shared responsive contract and all three interactive element classes are present. Existing render-matrix coverage continues to exercise the complete design registry.

The original `db.sqlite3`, user media, port 8000, merge state, and deployment state were not changed.
