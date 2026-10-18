# Phase101v — Polje lavande / Carobna ljubicasta

Current standard and dense fixtures:2531/2532 qa101v_polje_lavande / qa101v_carobna_ljubicasta,posts109/110 with two comments;2541/2542 qa101v_dense_ variants,posts111–117/118–124 dated October5–11. Isolated .qa100e.sqlite3 only.

## Before
32 blog/detail states320/390/768/1440 with Bootstrap and actual text fill. Standard phone title overflow320:71/73px,390:1/3px;comment320:3px. Dense phone grid144/74px. Lavande document92/22px;Carobna document0 but calendar visibly clipped, so document width alone was misleading. Lavande dense768 grid228px and box212px. Carobna existing tablet layout already fits seven44px days; its1px grid overflow comes from today's scale1.04 extending0.957px past the right edge.

Lavande archive actual contrast4.396 in resolvable phone states remains a targeted open issue. Photo-backed surfaces remain null,not passes. Desktop calendar targets27.23x34 remain small.

## Change and after
Extended existing phone title stacking/comment wrapping and accessible local calendar scroll region to both themes. Extended tablet full columns only to Lavande. Preserved Carobna's existing tablet layout; reset only tablet today transform.

40 after states:32 standard/dense plus8 dense820/991. Document/title/comment/calendar-grid overflow0. Every active calendar target below1000px is at least44px. All16 tablet column observations show no overlap (0.1px tolerance). Desktop measured rectangles match before; actual fill/color match common-state measurements. Unchanged colors are not a blanket contrast pass.

Native ArrowRight scrollLeft40 both themes;day11 links resolve117/124. Standard open-post links resolve109/110 after changes. Screenshot outputs/phase101v-carobna-after.png visually inspected;before outputs/phase101v-carobna-dense.png shows clipped calendar. Raw measurements saved.

Coverage25/37 is not25 passing themes. Remaining12 begin Kraljevska pozornica/Dimni akordi. FactoryDefault,photo zones,desktop targets,user pages and earlier open items remain in scope. Next narrow fix:Lavande factory archive actual fill/podlage,then remaining matrices.

Final check/migration pass;214 tests OK53.501s after tablet today correction. Existing missing staticfiles warning only.
