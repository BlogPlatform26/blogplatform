# Phase100q — readable comment timestamps

Baseline e105cf8; before measurements are Phase100p's 16-state matrix. This narrow change closes its timestamp P1 for Litica and Podvodna.

## Change

Only these two themes, at min-width768px, give the timestamp a local opaque #010611 background, #d5e5ff foreground and opacity1. A 2px radius softens the small surface without padding or geometry changes. The selector overrides the shared comment opacity rule. The local opaque surface guarantees contrast independently of the photograph behind the first desktop Podvodna comment; it does not establish contrast for adjacent author/body text. Phone styles remain unchanged.

## Evidence

Isolated .qa100e.sqlite3, authors2411/2412 and posts13/14, both comments, blog/detail at320/390/768/1440, Bootstrap loaded. Raw final computed observations are phase100q_comment_time_after.json.

- All16 states have zero document overflow; both comments remain present.
- Every recorded comment author/time/text rectangle equals the corresponding Phase100p baseline rectangle exactly.
- All16 tablet/desktop timestamps (two comments in eight states) have computed rgb(213,229,255), opacity1 and opaque rgb(1,6,17) on the timestamp itself, with no ancestor opacity. Contrast15.91694:1, including the first desktop Podvodna timestamp over the photo.
- Mobile timestamps retain their earlier opacity/background and contrast11.4595:1 Podvodna /11.948:1 Litica.
- Safe post-open clicks for both designs reached the correct canonical post13/14 and retained two comments. No mutating controls used.
- Screenshot phase100q-comment-dates.jpg visually inspected after scrolling: small date surfaces, readable dates and unchanged comment layout. Screenshot coordinates are not used for contrast math; the opaque computed surface supplies the evidence.

## Validation

Django check has no issues; migration check reports no changes. The first full suite had one stale assertion forbidding a color anywhere in Litica while testing the Podvodna author override. It now checks absence of that author-specific Phase100m rule, allowing the unrelated timestamp to use the same color. Final full suite: 214 tests passed in85.267s, exit0. Existing missing-staticfiles warning only.

QA browser closed and viewport reset; server8017 stopped. Original repository/database/media and port8000 untouched. Synthetic fixtures retained.

## Remaining scope

This closes timestamps only. First Podvodna desktop author/body and other photographic zones remain unverified. Phase100p's rejected screenshot coordinate mapping is not a contrast proof. Coverage remains13/37, not13 passes: other24 designs, full factory Default, desktop touch targets and user pages remain pending.
