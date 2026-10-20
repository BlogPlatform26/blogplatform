# Phase101z — Kraljevska / Dimni calendar containment

Both themes use the existing keyboard-focusable local phone calendar scroll region with seven44px columns. Dimni's viewport-width centered calendar caused x=-7.667 at320;it now stays at left0,width100% within its column. Tablet layouts retain their fitting seven-day arrangement. Kraljevska tablet today transform is reset to prevent grid-edge crossing. Desktop rules unchanged.

40 after blog/detail states:32standard/dense320/390/768/1440 plus8dense820/991. Document and calendar-grid overflow0;active targets at least44px below1000px. All16tablet column observations have no overlap (0.1px tolerance). Measured desktop rectangles match101y exactly. Raw contrast results retained;photo-null remains unverified,not a pass.

Native ArrowRight settled40px both themes. Day11links opened133/140;standard opened125/126. Screenshot outputs/phase101z-dimni-calendar.png inspected:month navigation and calendar now stay within phone edges,local scrollbar visible.

Initial suite failed two subcases of the old Phase96a test because it required the defective viewport-width rule. Updated that existing test to verify a focusable scroll region and44px minimums,retaining default-theme exclusion. No new implementation-mirroring test was added.

Remaining:narrow Dimni phone comment content usability,photo zones,desktop targets. Coverage27/37 is not27passes. Next current matrices Nebeska klasika/Ponocna elegancija;other8 themes,FactoryDefault and user pages remain.

Final validation: Django check and migration check passed; all 214 tests passed in 128.637s. Browser evidence was collected on 19 October before the final test-only assertion update.

