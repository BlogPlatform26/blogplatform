# Phase 75 — mobile inventory and test matrix

This is a source-code inventory and a test plan, not a new visual regression run.
Phase 74a/b already addressed public comment readability and the shared public
header at narrow widths. Preserve each design's desktop identity while making
the mobile flow readable and touch-operable. No application code, original
database, media, `main`, or deployment was changed in this phase.

## Page types and authentication states

| Surface | Anonymous/public | Signed in / owner-specific |
| --- | --- | --- |
| Discovery | Home (`/`, featured/all), search (`/search/`, posts/users/tags), blog list if linked | Following filter, notifications and user menu |
| Auth and account | Login, register, activation/reactivation, password reset, terms/privacy/content rules | Profile redirect, edit profile, password change, account deactivate/delete |
| Author's site | `/blog/<username>/`, author detail, post detail (same design as author) | Follow/restrict/block actions, own controls, analytics visibility |
| Content interactions | Like and visible comments as permitted; calendar/archive navigation | Comment create/edit/delete, quiz/poll, post create/edit/delete, boxes |
| Dashboard | Not available | `/blog/settings/` tabs: posts, boxes, design/live editor (including ambience), author, account, statistics; export |
| Administration | Not in ordinary public matrix | Django admin, security-events, post exports: separate staff-only audit |

Several URL endpoints are POST/action or token routes rather than independent
layouts (like, follow, comment, notifications, analytics, email confirmation).
Test their *controls on the containing page*, not an unauthenticated direct GET.
The URL map is `blogplatform/urls.py`; the exact visibility of any control
depends on permissions, profile settings and content state.

## Registered design matrix

`Profile.TEMPLATE_CHOICES` in `blog/models.py` defines **37 selectable keys**.
There are 42 HTML files in `blog/templates/blog/designs/`; file count is not
the selectable-design count. `soho` resolves to `studio.html` through
`resolve_design_template_name()`; test the registered key, not the file stem.

| Family for sampling | Registered keys | Count |
| --- | --- | ---: |
| Base and right-layout variants | `default`, `dark`, `classic`, `default_right`, `dark_right`, `classic_right` | 6 |
| Simple | `simple_pattern`, `simple_image`, `simple_retro` | 3 |
| Editorial | `soho` → `studio`, `magazin` | 2 |
| Scenic, ornate and bespoke | `litica_noci`, `podvodna_tisina`, `vodopad_u_magli`, `planine_u_magli`, `nebeski_mir`, `svemirski_horizont`, `zlatni_horizont`, `iznad_oblaka`, `sumska_svjetlost`, `polarna_svjetlost`, `zlatno_polje`, `neonski_grad`, `polje_lavande`, `carobna_ljubicasta`, `kraljevska_pozornica`, `dimni_akordi`, `nebeska_klasika`, `ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`, `staza_prema_vrhovima`, `jedro_u_suton`, `misticno_jezero`, `sjene_ulice`, `mjesecev_ples`, `asfaltni_plamen` | 26 |

## Shared render and control map

| Area | Main source of layout/behavior | Mobile-sensitive controls |
| --- | --- | --- |
| Public shell | `blog/templates/blog/base.html`, `blog/static/css/style.css`, inline shell CSS/JS | Logo, search collapse/form, auth/user menu, notification dropdown |
| Designed blog and detail | `blog/layouts/blog_design_base.html`, 37 selected design files, `blog/services.py` renderer; bespoke designs can extend `blog/base.html` directly | Header, columns, title, post cards, images/video, sidebars |
| Reused blog components | `blog/components/blog_header.html`, `blog_posts.html`, `post_card.html`, `post_actions.html`, `post_comments.html`, left/right sidebars, `blog_box.html`, `blog_profile_interaction_actions.html` | Follow/author actions, edit/delete, like, comment form/action menus, custom boxes |
| Calendar/archive | `blog_calendar_grid.html`, `blog_archive_entries.html`, design-specific wrappers | Prev/next month, dates with posts, archive links at narrow widths |
| Dashboard shell and settings | `blog/templates/dashboard_base.html`, `blog/blog_settings.html`, `blog/settings/_*.html`, `blog/static/blog/css/blog_settings.css` | Separate navbar/search, tab sidebar, design picker/live editor, posts/boxes/settings controls |
| Dashboard scripts | `blog_settings_main.js`, `design_live_editor.js`, banner/avatar/title helpers under `blog/static/blog/js/` | Tab switching, modal/dropdown, save/reset controls, preview |

`blog/templates/blog/post_detail.html` and `user_blog_page.html` exist, but
normal post/blog views resolve the selected `designs/<key>.html`; do not treat
those two templates as the primary 37-design route without runtime proof.

## Prioritized viewport matrix for subsequent phases

P0 = blocking function, P1 = content/layout, P2 = polish. At each viewport,
check document and component overflow, visible text size/contrast, 44 px
touch targets where practical, click/keyboard reachability, and a screenshot.
Use synthetic accounts/content and an isolated DB; never original `db.sqlite3`.

| Priority | 320 px | 390 px | 768 px | 1440 px |
| --- | --- | --- | --- | --- |
| P0 public shell: home/search/login/register | Toggle, submit, menu, form, no overlay | Repeat | Breakpoint handoff | Desktop identity baseline |
| P0 signed-in dashboard: settings/editor, create/edit post | Separate navbar/search, tabs, save/reset and form controls | Repeat | Sidebar-to-content transition | Existing dashboard baseline |
| P0 blog/post interactions: representative design family | Comment/like/follow/edit controls, calendar/archive | Repeat | Column stacking | Unchanged design baseline |
| P1 all 37 registered designs on blog + detail | Automated overflow/readability scan, then inspect outliers | Outlier rerun | Family representatives and outliers | Family representatives and outliers |
| P1 auth/account/author/notifications/boxes | Forms, long labels, validation, controls | Repeat | Layout transition | Representative baseline |
| P2 animations, decorative artwork, uncommon states | Only after P0/P1 | Same | Same | Preserve desktop composition |

For a small next phase, first use one anonymous and one owner account on an
isolated server to verify `dashboard_base.html` at 320/390/768/1440. Its source
has **no viewport meta tag**, duplicates the public navbar, and retains an
inline `width: 320px` search group. These are concrete source-level risk
signals, not a measured UI failure yet. If confirmed, Phase 76 should fix
only the dashboard shell/search/touch controls and add a focused regression
test, leaving design-specific pages for later phases.
