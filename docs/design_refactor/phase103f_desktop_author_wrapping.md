# Phase103f: desktop secondary author wrapping

Baseline8c9f48e, 2026-10-25. Both other chats inactive; clean Git and fresh capacity. Only isolated .qa100e.sqlite3/8017.

The 168-character synthetic author name had local horizontal excess1044px at1440 and occupied one clipped line. Existing phone/tablet anywhere wrapping ended at991.98px. Add overflow-wrap:anywhere to the shared secondary-author rule, retaining the existing two-line preview clamp and six desktop columns.

Four paired before/after widths320/390/768/1440: document overflow0; author local excess0 after (desktop1044 to0), author height desktop16.896 to33.792px. Phone/tablet sampled grid/title/author rectangles exactly equal. Desktop author and enclosing grid height intentionally increase; this is not identical desktop geometry. Actual sampled fill/color unchanged. The two-line preview still truncates the full168-character name with an ellipsis; this closes horizontal clipping, not a full-name-in-card requirement.

Desktop grid still six columns. Two populated card link boxes are217.104/217.115px wide,327.406px high, separated19.334px, no mutual overlap. Native first-card click reaches post227 canonical detail. Own server restarted after template edit; tab closed, viewport reset, server stopped afterward.

Screenshot z/outputs/phase103f-desktop-author.png is a scrolled1440 viewport, not the full page. Visually inspected: two author preview lines, ellipsis, separated cards and footer. No rendered-pixel gradient contrast claim. Raw files z/work/phase103f; paired measurements consolidated here.

Django check and migration check green. All223 tests pass in49.363s.

Still open: empty-owner browser flow, gradient native hover/pixel proof, photographic zones, desktop targets, Base4 dense week, factory Default, remaining U02–U12 and final matrix. No new37-design sweep.
