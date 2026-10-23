# Phase102t: user-route acceptance reconciliation

Source baseline7633b61. Read Phase75 inventory, Phase76/77,78b/c/d,79d/e,80b/b2/c/d,81a/b2/c and current URL map. Source selectors and associated contract tests remain present for profile fields/menu, design tabs and both post-form families. This is evidence reconciliation, not a new browser pass or blanket route acceptance. Previous goal turn102s was progress (committed implementation and browser/test evidence).

## Retain existing narrow closures

| Existing proof | What is already proved | What it does not prove |
|---|---|---|
|76 and77|Dashboard viewport/header search; actual search submission; six top-level tabs at four widths; avatar containment and tablet sidebar|Every tab's controls, validation or persistence|
|78b/c/d|New-post tabs/actions/ordinary fields/CKEditor targets at320/390 and desktop; dropdown opening|768 coverage in these focused phases; creation, draft/autosave or editor feature workflow; other six post-filter destinations|
|79d/e|Direct create/edit forms at four widths; toolbar opening; public-shell owner menu/search|Submitted create/edit results, validation and post deletion|
|80b/b2/c|Live-editor actions/fields and two-design preview at four widths; unsaved slider reflected in preview|Persisted design settings, all design controls or all37 previews|
|80d|Three design subtabs and primary controls at four widths; tab switching|Music switches, design cards, save/reset persistence|
|81b2|Notification dropdown containment in BOTH shells at four widths; unread fixture unchanged|Opening a notification or marking read; all notification-list states|
|81c|Profile fields/save button/menu targets at four widths; focus works|Validation and saved values|
|81a|Profile redirects to selected blog; notification list populated state measured|Separate profile.html acceptance; empty/error states or notification actions|

The38–50-test suite numbers in these historical documents are historical runs, not today's suite size. Current214-test pass102s does not replace missing browser workflows. Contract tests assert scoped markup/styles; they do not prove every interactive state.

## Concrete remaining route batches

Use320/390/768/1440 for each containing layout and record guest/owner/reader state. Check local overflow and overlaps, readable actual child fill/background, reachable focus and safe navigation; capture the changed/relevant state. Reuse closed component evidence above instead of repeating its entire audit. Persistence tests use disposable synthetic data only, no real email/media or original DB. Account credentials and irreversible final actions require applicable permission handling; confirmation/cancel layouts can be checked independently.

| ID | Containing routes / state | Missing acceptance evidence |
|---|---|---|
|U01|Home `/`, `/search/` posts/users/tags; guest and following-owner states|Populated/empty results, long text, filters, pagination and search submitted from public shell; current four-width geometry|
|U02|`/login/`, `/register/`, `/password-reset/`|Form layout, validation/error messages, field/button reachability; registration terms and email side effects kept separate from layout checks|
|U03|`/aktivacija/`, activation/confirm-email/reactivation/reset token pages, password reset done/complete, resend confirmation|Success/invalid/expired rendered states using synthetic tokens and local mail; distinguish actions from standalone layouts|
|U04|`/o-autoru/`, `/blog/<username>/upoznaj-autora/`|Owner onboarding and public author page, long content, question form/validation, owner vs reader controls|
|U05|Designed blog/detail containing follow/restrict/block, likes, comments, quiz/poll|Current representative shared-component interaction states: reader/owner/guest, long comment, edit/cancel, validation and quiz/poll result. Per-design layout evidence is retained; do not rerun37 layouts|
|U06|`/add-box/`, `/box/<id>/edit/`, settings boxes|Editor fields/actions, long content, validation and resulting synthetic box; delete confirmation/cancel surface|
|U07|Settings post filters including new/drafts, direct `/new/`, `/post/<id>/edit/`|Missing768 dashboard new-form proof, post-list filters, draft/autosave/save and validation using synthetic content; existing field/toolbar closures retained|
|U08|Settings author/account/statistics and export|Each actual subtab state, populated statistics/empty state, long labels and export control; account deactivate/delete confirmation/cancel layouts; do not treat POST endpoint GET as test|
|U09|Settings design/ambience and live editor|Previously excluded cards/music switches, validation, synthetic save/reload; preserve closed preview geometry and unsaved-update evidence|
|U10|`/profile/edit/`, password change/done, profile menu|Profile validation/persistence on synthetic account; password form layout and done state (credential-change submission handled separately); long username menu|
|U11|`/notifications/` and shared dropdowns|Empty/populated list, reader navigation/read-state action using synthetic notification; retain81b2 closed positioning proof|
|U12|Terms/privacy/content rules and shared support/bug-report UI|Long-document layout and navigation; support form fields/validation without external message transmission|

These are12 finite verification batches, not12 predicted fixes and not an ETA. A newly demonstrated failure becomes a scoped implementation plus before/after and full-suite gate. Do not mark a batch complete from another batch's tests.

## URL inventory boundaries

`phase102t_route_inventory.json` records68 explicit path declarations and source lines. This is not68 pages: includes redirects, machine endpoints, action endpoints and includes. `ckeditor5/` and admin includes have their own routes; media/static patterns are separate. The export path appears twice in source: record first-match resolution when testing, do not silently count two screens. Staff admin/security/post-exports remain a separate staff audit. Sitemap, robots, favicon, verification, analytics and mention-search are not independent mobile layouts; test relevant UI controls where applicable.

## Next action

StartU01 with existing synthetic data and a fresh targeted four-width baseline. Continue photo/target/default requirements from remaining_verification_scope.md alongside this finite route list. This reconciliation closes only the task of mapping75 against76–81; none ofU01–U12 is newly declared passed. No application code/database modified and no new runtime test claimed.
