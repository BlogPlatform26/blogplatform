# Phase103w — support baseline and native validation

Read-only browser audit on guest home at320/390/768/1440, baseline6dcc41a. No application changes. Raw C:/Users/mario/Documents/Codex/2026-10-10/z/work/u12-support/baseline.json and validation.json.

Document and sampled control local excess0 at all widths, but this is not acceptance. Radio labels are24px high; title/email37.333px; submit30.333px. Phone field widths223.333/293.333px; tablet768 width94.688px; desktop254.667px. Radio input13px is wrapped in a clickable label. Text controls use placeholders without explicit associated labels or aria-label; AX showed unnamed text fields. Next: scoped support control labels and phone target sizing, with before/after and desktop controls. Tablet narrow form remains a separate usability concern.

At390, empty submit keeps URL / and focuses title with valueMissing. With synthetic title only, submit focuses description with valueMissing. Invalid optional email reports typeMismatch while description remains empty; no valid submit attempted. No message/email/database mutation. These are native validation checks, not server error/success proof. No screenshot, full keyboard or contrast acceptance claimed. No suite rerun for documentation-only audit; last231 tests50.958s in103v.
