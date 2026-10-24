# Phase103d - darker home title gradient

Baseline19c55fd. Only the existing home-only title gradient normal and hover stops change. Purple/orange/gold gradient identity remains; desktop colors intentionally darken. No layout declarations changed. No public blog or search rule changed.

Normal stops #6d28b0/#9a4200/#755600 have white contrasts8.137/6.660/6.802. Hover stops #552080/#793400/#5c4300 have11.026/9.114/9.301. These are computed color contrasts, not rendered-pixel measurements. For opaque sRGB linear interpolation, convex channel luminance bounds the gradient by its endpoints. Browser actual normal backgroundImage confirms the new stops; transparent text fill is intentional background-clip:text. Inspected before ancestor chain has opaque white card inner background, opacity1 and actual title child0.

Eight featured/all states at320/390/768/1440: all sampled title x/width/height identical to before, document overflow0. Safe first title click reaches post221 canonical detail. Raw before/after/safe consolidated in phase103d_measurements.json. Before was recorded earlier24Oct; after recovered later24Oct following browser timeouts. Lost REPL measurements were discarded and recaptured, not counted. QA server restarted after edit; isolated database/port8017 only.

Both screenshot APIs returned Unable to capture screenshot. No new screenshot or visual/pixel confirmation is claimed. Normal DOM and calculated contrast evidence is complete for these samples; rendered-pixel/screenshot and native hover confirmation remain open. The hover palette was changed consistently but not exercised with a native pointer. Do not describe this as full U01 contrast acceptance. Desktop long-author clamp, empty following/owner, other routes/photo/target/default/final matrix remain open.

Django check and migration dry-run passed. Full219 tests passed379.596s before browser recovery; no source edits afterward, so the suite was not redundantly rerun. Server and successful QA tab closed, viewport reset.
