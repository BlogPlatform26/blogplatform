# Phase101j — Nebeski factory subtitle and tablet body ink

## Confirmed cause and change
The subtitle was 15.2–17.568px, weight400, with color #334155 but inherited actual -webkit-text-fill-color #81879a. The known solid-surface contrast was2.543:1. On the exact factory blog_title_color only, text fill now follows currentColor. With the existing subtitle opacity and opaque header surface, effective contrast is5.713:1 at all four widths.

The factory body #72788a remained4.353:1 on the tablet card. The existing phone #475569 override now extends through991.98px, retaining7.490:1 on phones and raising tablet to7.490:1. Desktop body styling is unchanged; its photo-backed contrast remains null/unverified.

## Verification
Eight before/after blog/detail states at320/390/768/1440 with Bootstrap and two synthetic comments. All measured element rectangles identical; document overflow zero. Actual text fill, ancestor opacity and backgrounds saved. Safe open reaches post45. Factory/custom #123456 template guard rendering confirms both overrides excluded for nonfactory palettes; this is a template-level custom check, not a custom browser scenario.

Phone screenshot inspected: outputs/phase101j-nebeski-phone.png. Header subtitle is legible; existing faint month/archive labels are separate open findings, not claimed fixed.

Django check and migration dry-run pass. Full214 tests pass in60.701s. Original repo/database/media/port8000 untouched. This is not a full theme pass; remaining photo zones, labels, controls and other designs stay open in remaining_verification_scope.md.
