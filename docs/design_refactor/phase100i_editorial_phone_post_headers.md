# Phase100i - Studio and Magazin phone post headers

## Scope and cause

The shared horizontal title/date header compressed long post titles on phones. At 320px the Studio title had only 36.90px and 70px of local overflow; Magazin had 88.90px and 32px of local overflow. Document overflow was zero, so document-only checks missed the issue.

Both post-card partials now identify the header with `editorial-post-header`. Below 576px the title and date stack vertically, the title uses the available width, and long tokens may wrap. Tablet and desktop retain the existing horizontal layout. No palette or content changes.

## Browser verification

Used the isolated `.qa100e.sqlite3`, authors 2401/2402 and posts 11/12, long editorial title, two comments and system photographic hero. Actual Bootstrap styles loaded. Measured blog and detail at 320/390/768/1440 before and after (16 states per pass), after restarting the template-caching QA server.

| Design | Width | Title width before | Title width after | Title local overflow before/after |
| --- | ---: | ---: | ---: | ---: |
| Studio (`soho`) | 320 | 36.90 | 183.33 | 70 / 0 |
| Studio (`soho`) | 390 | 106.90 | 253.33 | 1 / 0 |
| Magazin | 320 | 88.90 | 235.33 | 32 / 0 |
| Magazin | 390 | 158.90 | 305.33 | 0 / 0 |

The same measurements apply to blog and detail. All 16 after states have zero document and sampled local overflow (card/header/title/date). At 768 and 1440 the complete measured title/date/header geometry is identical before and after for both routes and designs. At 575px the header stacks; at 576px it remains horizontal, without sampled overflow. Visual checks at 320px confirm readable titles followed by dates with intact content and comments. Safe post opening and comments navigation passed for both designs at 390px; both comments remain present. No mutating browser actions were used.

## Validation and limits

`manage.py check`, `makemigrations --check --dry-run`, and all 214 tests passed (89.553s). The suite emits the existing missing collected-static directory warning. `git diff --check` passed. Source repository, source database/media and port 8000 were not changed.

This closes the narrow mobile title layout findings from Phase100g. It does not close Magazin photographic hero contrast, desktop touch targets, the remaining design matrix or full factory Default verification. Phase100h contrast fixes remain separate evidence; this phase changes layout only.
