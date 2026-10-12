# Phase100v — mobile comment word wrapping

The 100s local comment overflow was caused by `.bp-comment-word` using `inline-block` and `white-space: nowrap`. At 320 px the word `verification.` occupied 80.93 px in a 74 px Vodopad or 72 px Planine comment column. The outer comment's wrapping rule could not break this child.

Below 576 px, only Vodopad/Planine now limit each word to its column and allow wrapping inside an overlong word. Ordinary short words retain their inline-block behavior. Desktop CSS is unchanged.

[Raw measurements](phase100v_comment_wrap_measurements.json) contain 16 unique before and after states: both themes, blog/detail, 320/390/768/1440, with Bootstrap and two comments. Both comment containers have zero local overflow in all after states; document overflow is zero. Every sampled rectangle and local overflow on 768/1440 is identical. Sampled colors, font sizes and ancestor backgrounds/opacity are unchanged. This is not new photographic contrast proof.

At 320 px safe post-open clicks reach posts 29/30 and show both comments. The Planine overlong word now occupies 72 px with client/scroll width 72, normal white-space and anywhere wrapping. Synthetic data is unchanged.

Validation: Django check and migration check passed. Full suite completed successfully: 214 tests in 139.947 seconds, exit 0. The existing missing-staticfiles warning was emitted. QA server and browser tab were closed; synthetic DB retained. Remaining work includes tablet/dense calendars, subtitle candidate, photo zones and targets; no complete theme pass is claimed.
