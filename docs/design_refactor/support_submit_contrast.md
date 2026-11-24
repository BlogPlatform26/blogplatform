# Support submit contrast and focus (2026-11-24)

The shared sidebar support submit button uses scoped #084298 colors and a solid3px focus-visible outline with3px offset (rendered2.66667px). This intentionally changes desktop button color and keyboard focus too; dimensions and typography are unchanged.

Recorded search fixture /search/?q=qa102y: normal text contrast rises4.016 to8.354 against opaque rgb(248,241,232). Focused white text on #084298 is9.362; outline against card is8.354. Transparent button ancestors have no background images.

Paired320/390/768/1440 samples contain18 visible form nodes each: exact rect/font/image preservation, background colors and local-overflow values unchanged; only button foreground changes. After document overflow0. Raw z/work/support-contrast-fresh-before.json and support-button-after.json. Before samples were taken during focus transitions: they are geometry evidence, not settled-focus evidence. Do not infer a missing focus indicator from those samples. Earlier stable observation showed the original blue fill and translucent4px shadow after transition.

Native Tab to submit was visually inspected at all four widths, with durable900px-height scrolled viewport images z/outputs/support-button-focus320.png, support-button-focus390.png, support-button-focus768.png, support-button-focus1440.png. The ring is contained within its card and does not overlap the preceding email field. At1440 Enter with empty fields focuses invalid title; no valid submission or email. Missing temporary screenshots after usage-review failure were regenerated and copied successfully.

Validation: manage.py check clean; makemigrations --check --dry-run no changes; full253 tests77.717s OK, session67351. No application change after that suite. QA server52599 exited;8017 listener absent; guest tab11 closed and viewport reset.

Scope: closes recorded shared-sidebar submit normal/focus contrast repair. Hover/active variables use the same dark color but pointer-state acceptance is not claimed. Other support field/radio focus contrast, retry-page coverage, remaining server-invalid/legal states, calendar states and full37/U01-U12 remain open.
