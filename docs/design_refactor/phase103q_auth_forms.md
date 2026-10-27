# Phase103q — public authentication form layout

U02 baseline found a shared col-md-6 containing column squeezing sidebar-free authentication forms. At768 registration username/blog-name fields measured54.677px and password fields90.365px; help text was8px. The reset route unexpectedly rendered Django admin's registration/password_reset_form.html, confirmed by browser title/branding and template loader origin in django/contrib/admin.

The login/register/password_reset route names now receive full containing width and hide their empty sidebars. Registration help is14px with1.5 line height; registration and public reset inputs/buttons have48px minimum height. Reset inputs use border-box sizing and full available width. The public reset template moved to blog/password_reset_form.html and the route selects that unique name, preventing admin template precedence. Designed blog routes do not receive these rules.

## Evidence

Twelve initial guest states and twelve final states cover320/390/768/1440. All document excess values are0. Registration tablet username/blog-name fields now194.031px, password fields369.073px; desktop form width intentionally expands. Login phone widths are unchanged. Registration controls are48px high and help computes14px. Public reset input/button widths match at238.667/308.667/246.708/566.667px across the four widths, with48px height. This is not a blanket contrast or keyboard acceptance claim.

Wrong synthetic login produced the rejection message and was measured at all four widths without resubmitting. Empty registration submission focuses id_username with valueMissing=true. Invalid reset email focuses id_email with typeMismatch=true. No registration completion, credential change or email transmission occurred. Server-side invalid email is additionally covered by a regression test; the test also ensures public template selection and absence of admin/base_site.html.

Sixteen Planine/Nebeski blog/detail controls at four widths retain exactly the sampled caption/container/main-column rectangles, fonts, fills and backgrounds from103p; document excess0. This is scoped regression evidence, not another37-theme audit.

Raw evidence: z/work/u02-baseline/initial.json, after.json (login/register final; reset portion is intermediate admin rendering), reset-final.json, login-errors.json, blog-controls.json and tests.txt. Compact/preserved measurements are in phase103q_auth_forms_measurements.json. The registration768 viewport screenshot z/outputs/phase103q-register-tablet.png was visually inspected. The reset320 screenshot phase103q-reset-phone.png is scaled inside a white canvas and is only limited visual evidence; do not infer pixel contrast or full-page acceptance from it.

Validation:226 tests pass in64.337s; Django check and migration drift check pass. Remaining U02 work includes registration server-error states, complete keyboard/contrast acceptance and successful account/reset workflows. U03 token/result pages and other ledger work remain open.
