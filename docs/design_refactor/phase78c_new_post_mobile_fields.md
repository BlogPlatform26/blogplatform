# Phase 78c — mobile ordinary fields in the new-post form

## Scope and cause

The new-post form's ordinary controls were fixed at 30 px high with 12.8 px
text on both 320 and 390 px viewports: title, YouTube URL, publication date,
tags, and native image chooser. A mobile-only rule below 576 px now gives
those controls 44 px height, 16 px text for the four text/date controls,
and 16 px labels. The native file chooser uses 14 px text at 44 px height:
at 16 px its browser-generated “No file chosen” text was clipped at 320 px.
No desktop style or CKEditor toolbar rule was changed.

## Browser verification

An isolated copy of the synthetic owner database ran on port 8062. The
original `db.sqlite3`, media and port 8000 were not used.

| Width | Title/video/date/tags | Image chooser | Document overflow |
| --- | --- | --- | ---: |
| 320 px | 44 px high, 16 px font | 44 px high, 14 px font | -15 px |
| 390 px | 44 px high, 16 px font | 44 px high, 14 px font | -15 px |
| 1440 px | 30 px high, 12.8 px font, unchanged | 30 px high, 12.8 px font, unchanged | -15 px |

At both mobile widths, the title, video and tag fields accepted real clicks
and became the active element. Publication date and image chooser received
keyboard focus without opening a picker; the focused element was confirmed.
No form was submitted; the trial database still had 0 posts. A 320 px screenshot
confirmed that the native chooser's empty filename text fits at 14 px.

CKEditor toolbar controls remain small and are a separate mobile touch risk.
Their configuration and CSS were not edited in this phase. This is not a
full post-creation workflow test.

## Automated gates

- Focused render-contract test: 1/1 passed.
- Full Django suite: 39/39 passed.
- `manage.py check`: no issues.
- `makemigrations --check --dry-run`: no changes detected.
