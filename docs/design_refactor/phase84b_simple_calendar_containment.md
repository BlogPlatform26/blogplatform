# Phase 84b — simple calendar containment

## Scope

This phase fixes only the repeatable responsive calendar overflow in
`simple_pattern` and `simple_image`. Contrast findings remain deferred to
Phase 84c.

## Implementation

Below 992 px, `.calendar-box.calendar-box--simple` uses `border-box`, `width:
100%` and `max-width: 100%`. Its existing 16 px padding and border are therefore
contained inside the responsive sidebar column instead of being added to its
width. The rule is rendered only for the two affected templates. It does not
apply at 1440 px and does not alter `simple_retro`.

## Verification

The browser run used an isolated copy of the database with synthetic Pattern
and Image blogs. Both the blog index and post detail were checked at requested
viewports 320, 390, 768 and 1440 px. Before the change, document overflow was
repeatable at 320/390/768 (18/18/10 px); after the change, `scrollWidth` equaled
`clientWidth` for both pages and both designs at every viewport. The calendar
remained inside the content column, while the desktop layout at 1440 px stayed
contained and unchanged by the media-scoped Phase 84b rule.

The previous-month control was also clicked safely on each design and navigated
to the expected `?year=2026&month=8` URL. Short fixture labels were used for the
final measurements so an intentionally long synthetic blog title would not be
misreported as calendar overflow.

Django verification: `manage.py check`, migration drift check, the focused
calendar contract tests, and the complete test suite all pass.
