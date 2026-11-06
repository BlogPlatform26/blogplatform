# Onboarding hidden-error baseline

On b777585, native390 owner2673 login and /o-autoru/: Enter Dalje to step2, date10000-01-01, Enter Dalje to step3, Enter Spremi. The server returns the bound form, but the browser shows step1 with no error text or alert. The date retains10000-01-01 and aria-invalid=true in hidden step2. Raw z/work/onboarding-error-baseline.json records visibleSteps=['1'], errors=[], dateVisible=false.

This is distinct from the settings retry fixed by a8d00aa: onboarding retains data but hides the invalid field and provides no explanation. Next fix must render field errors and open/focus the erroneous step, preserving ordinary step layout and testing keyboard transitions. No application change or test rerun in this baseline; latest250tests64.172/check/migration green remains a8d00aa. No valid profile save, no screenshot, no email. Logout verified, tab6 closed, viewport reset, server72648 stopped.
