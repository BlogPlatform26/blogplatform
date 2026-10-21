# Phase102h — Staza/Jedro phone containment

Staza standard320 previously expanded its intrinsic grid to349.91px within276.67px, producing59px document overflow. Both dense phone calendars had44px targets with starts only37.34/36.19px apart. Phone-only minmax(0,1fr), child min-width0 and post wrapping now contain the columns. Focusable calendar scroll regions contain344px grids with seven44px targets and6px gaps.

## Evidence

- Before: Phase102g. After:32 standard/dense blog/detail states at320/390/768/1440 with Bootstrap. Document and measured title/comment/grid overflow zero.
- Dense320/390 starts now50px apart, targets44x44: no adjacent overlap. Existing768 seven44px layout preserved.
- All sampled768/1440 rectangles identical to102g; actual text fill and color unchanged at every width. Photo contrast remains unverified; unchanged ink is not a photo readability pass.
- Safe standard opens173/174 and dense day11 opens181/188. Native ArrowRight settled at40px in both calendars.
- Screenshot `C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase102h-jedro-calendar.png` inspected: local horizontal scrollbar visible. Photo calendar/profile text still needs readability verification.
- Django check and migration dry-run pass. Full214 tests pass in46.558s. No original DB/media/port8000 changes. Own server8017 stopped, tab closed, viewport reset.

Raw evidence in phase102h_measurements.json. This closes the confirmed phone layout findings, not the whole themes. Photo zones, desktop targets and broader remaining scope stay open. Next initial series: Misticno jezero/Sjene ulice, then Mjesecev ples/Asfaltni plamen.
