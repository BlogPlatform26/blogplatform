# Phase102z — home fallback image

A missing images/default-post.jpg caused broken images in all three home fallback branches. Add a small local SVG article placeholder and reference it from primary all-post cards, primary featured cards and secondary featured cards. Empty alt text makes this generic decoration silent beside the existing linked post title. Uploaded and configured image branches are untouched.

## Evidence

Isolated .qa100e.sqlite3, QA port8017, synthetic102y posts221–228. Measurements captured24Oct2026; underlying posts dated23Oct. Four featured before states at320/390/768/1440 each had8 failed images (naturalWidth0). After restarting the template-caching QA server, all8 load at each width with naturalWidth640 and empty alt. Four all-post after controls each contain5 loaded fallback images. Document overflow0 throughout; image parent overflow is recorded. Raw results and after text/color/fill/font samples are in phase102z_measurements.json. No CSS text color was changed; this phase does not establish composed text contrast or photographic acceptance.

Safe featured next navigation reached page2; previous returned before switching through Svi postovi. The new image deliberately restores a visible image area: card heights and downstream positions can change relative to the collapsed broken image. Do not claim identical desktop geometry. Existing column rules and actual-photo branches remain unchanged.

Viewport capture: C:/Users/mario/Documents/Codex/2026-10-10/z/outputs/phase102z-featured-phone.png (390 requested viewport, not full page). Capture appears scaled within a wider white canvas; it is limited visual evidence, not proof of a complete phone layout. DOM asset dimensions and load state provide the specific missing-asset evidence.

## Validation

Django check and makemigrations --check --dry-run green. Full217 tests passed in57.361s. No schema change. No production database/media or port8000 used.

## Remaining

U01 empty following/owner distinctions, keyboard order, actual contrast and tablet secondary-card usability remain open, along with U02–U12 and the design acceptance gaps in remaining_verification_scope.md. This closes only the missing home fallback asset.
