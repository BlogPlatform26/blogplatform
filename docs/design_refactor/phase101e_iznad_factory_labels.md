# Phase101e - Iznad factory sidebar labels

Phase101d confirmed mobile archive1.201:1. The first color-only patch still looked pale in a screenshot: inherited -webkit-text-fill-color was #f0dbe9 despite computed color#514956. The final factory-only rule updates both actual fill and color for month/archive/sidebar labels, with opaque#fff7fc surface. Calendar arrow links reset fill to their existing currentColor without changing their existing shape/surface.

Condition requires iznad_oblaka and exact factory box_title_color#f0dbe9. Django Template/Context checks confirmed override present for factory and absent for custom#123456; this is a template-level custom-color check, not a new browser custom-palette scenario.

Final16 blog/detail states, both Zlatni control and Iznad,320/390/768/1440 with Bootstrap. Month/archive and arrow text now have actual fill#514956 on opaque#fff7fc,8.190:1. All sampled geometry matches101d within0.05px and document overflow0. Native screenshot390 inspected: labels/arrows visibly dark and circular button shape retained. Safe post-open61/62 with2comments and previous/next month navigation passed. Raw measurements include fill read via getPropertyValue('-webkit-text-fill-color'); property camelCase returned empty and was insufficient.

Check/migration clean;214 tests passed46.479s in final validation run. Earlier runs58.855s/49.383s also passed. No changes to schema or customization storage. Server/tab closed and fixtures retained.

IMPORTANT evidence correction: prior audits generally measured color only. This phase exposes a gap for inherited text fill, especially calendar labels/links. Future final matrix MUST collect actual text fill (plus opacity/surfaces), and reconcile older contrast passes where fill differs; do not treat a color-only ratio as final rendered proof. Current extended observations show remaining Zlatni arrow fill differs from color and photo evidence is unresolved. No claim all themes pass. Next reconcile this gap while continuing18 remaining themes and user pages.
