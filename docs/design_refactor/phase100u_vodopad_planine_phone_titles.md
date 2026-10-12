# Phase100u — Vodopad/Planine phone post titles

The shared post header kept its title beside the date, leaving only 63.69 px (Vodopad) or 40.35 px (Planine) at a 320 px viewport. Under 576 px these two themes now put the title above the date. Other themes receive only an inert header class.

## Evidence

Complete raw before/after observations and safe navigation results: [measurements](phase100u_mobile_title_measurements.json). Fresh before observations use the same date as after, avoiding changes in calendar today state. Two themes × blog/detail × 320/390/768/1440 = 16 unique states in each run, with Bootstrap loaded and two comments per post.

- All post-title local overflow is zero after the change; document overflow remains zero.
- At 320 px title widths become 157.33/155.33 px; at 390 they become 227.33/225.33 px.
- All sampled element rectangles and local overflow at 768/1440 are identical before/after. Sampled text colors are unchanged at every width.
- Safe post opening at 320 reaches posts 29/30 and displays both comments. A qualitative phone screenshot was inspected; screenshot coordinates are not used as pixel-contrast evidence.
- Django check and migration check passed. Full suite: 214 tests, OK in 154.145 seconds, exit 0. Only the existing missing-staticfiles warning was emitted. QA server and tab are closed; synthetic DB retained.

This closes the standard long-title overflow from 100s. It does not close comment-text local overflow, tablet/dense-week calendars, photographic contrast, desktop targets, or the Planine subtitle candidate. No broad theme pass is claimed. Original database, media, port 8000 and main were untouched.
