# Phase 101i — dark/classic tablet column containment

The 768px dark screenshot exposed an existing calendar/post collision: a 260px calendar occupied a 152.02px sidebar. Document scrollWidth did not detect that overlap. Phase101h date contrast was valid but was not a layout pass.

For dark, dark_right, classic and classic_right only, 768–991.98px now stacks full-width columns in post/calendar/profile order. Repeated 160px page-top gaps become 24px within this range. Phone and desktop rules are unchanged.

## Verification
- 32 before/after blog/detail states at 320/390/768/1440 with existing synthetic comments, Bootstrap loaded.
- All 24 phone/desktop state geometries exactly match before. No positive document overflow.
- Additional 16 blog/detail states at 820/991. All 24 tablet states have non-overlapping column rectangles. The dark 768 screenshot visibly confirms the calendar no longer overlays posts.
- Safe post-open clicks reach posts 1/2/3/4 in the four variants.
- Actual fill/ancestor surfaces recorded; comment timestamp contrast remains dark 13.713/classic 7.455 tablet+desktop and phone 12.791/10.033.
- Django check and migration dry-run pass; 214 tests pass in 59.310s.

## Limits
This closes the observed tablet column collision in these four variants, not all design verification. Dense calendar touch targets, long content, other themes, photographic zones and user pages remain governed by the open scope. No dense-week result is claimed here. Desktop appearance is preserved. Original repository/database/media and port8000 untouched.
