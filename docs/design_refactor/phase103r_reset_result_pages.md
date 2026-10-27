# Phase103r — public reset result templates

Following103q, template-loader inspection confirmed that password_reset_done, password_reset_confirm and password_reset_complete also resolved to django/contrib/admin/templates/registration. Twelve browser baseline states (three routes at320/390/768/1440) displayed Django administration branding. Invalid-token rendering offered no retry link in its main content.

The existing public templates now live under blog/ and their URL views explicitly select those unique paths. These three sidebar-free routes receive the same full containing width as103q. No email/token/password behavior was modified. New regression tests ensure result template selection and invalid-token retry rendering without admin/base_site.html.

Twelve final states have zero document and sampled local excess. Public messages are visible and the native retry link reaches/password-reset/; the completion login link reaches/login/. The inspected390 viewport capture is z/outputs/phase103r-invalid-reset.png, not a full-page acceptance claim. Raw before.json, after.json, safe.json and tests.txt are in z/work/u03-reset; measurements are retained in phase103r_reset_result_measurements.json.

Validation:228 tests pass in63.212s; Django check and migration drift check pass.

These are direct GET result-layout checks: they do not prove mail delivery, a successful password change, expiry handling or the valid-token form. Retry/login links measured37.333px high and remain a touch-target follow-up. U03 is not closed by these scoped results.
