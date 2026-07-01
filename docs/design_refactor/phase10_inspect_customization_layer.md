# Phase 10 — pregled centralnog customization layera

Izrađeno: 2026-07-01 22:33:54

## Sažetak

Ova faza ne mijenja aplikaciju. Samo detaljnije pregledava gdje se trenutno nalaze korisničke postavke, CSS varijable i postojeći centralni layer.

Najvažnija datoteka za daljnji rad je:

```txt
blog/templates/blog/components/blog_design_styles.html
```

Ako je ta datoteka stvarno uključena u bazni template, onda je to najvjerojatnije mjesto gdje treba dodavati ili popravljati CSS varijable, umjesto da se ručno dira svaki dizajn.

## Gdje se uključuje `blog_design_styles.html`

### `design_refactor_phase10_inspect_customization_layer.py`

Linija oko 17:
```txt
0015: 
0016: TARGETS = [
0017:     "blog/templates/blog/components/blog_design_styles.html",
0018:     "blog/templates/blog/base.html",
0019:     "blog/static/blog/css/blog_settings.css",
```

Linija oko 106:
```txt
0104: project_files = all_project_files()
0105: 
0106: # Include/use map for blog_design_styles.html
0107: include_hits = []
0108: for p in project_files:
```

Linija oko 110:
```txt
0108: for p in project_files:
0109:     text = read_text(p)
0110:     if "blog_design_styles" in text or "components/blog_design_styles.html" in text:
0111:         include_hits.append({"file": rel(p), "hits": find_lines(text, r"blog_design_styles|components/blog_design_styles\.html", context=2, max_blocks=5)})
0112: 
```

Linija oko 111:
```txt
0109:     text = read_text(p)
0110:     if "blog_design_styles" in text or "components/blog_design_styles.html" in text:
0111:         include_hits.append({"file": rel(p), "hits": find_lines(text, r"blog_design_styles|components/blog_design_styles\.html", context=2, max_blocks=5)})
0112: 
0113: # Target details
```

Linija oko 142:
```txt
0140: 
0141: # Field mapping in central file
0142: central_path = ROOT / "blog/templates/blog/components/blog_design_styles.html"
0143: central_text = read_text(central_path)
0144: field_map = []
```
### `blog/templates/blog/author_detail.html`

Linija oko 9:
```txt
0007: 
0008: {% block content %}
0009:     {% include "blog/components/blog_design_styles.html" %}
0010: 
0011:     <div class="card shadow-sm border-0 mb-4 author-page-card">
```
### `blog/templates/blog/designs/asfaltni_plamen.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/carobna_ljubicasta.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/dimni_akordi.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/iznad_oblaka.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/kraljevska_pozornica.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/mjesecev_ples.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/morski_prijelaz.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007:     body {
```
### `blog/templates/blog/designs/nebeski_mir.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: /* Nebeski mir */
```
### `blog/templates/blog/designs/nebesko_polje.html`

Linija oko 13:
```txt
0011: 
0012: {% block content %}
0013:     {% include "blog/components/blog_design_styles.html" %}
0014:     <style>
0015: html,
```
### `blog/templates/blog/designs/neonski_grad.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/planine_u_magli.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/podvodna_tisina.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007:     body {
```
### `blog/templates/blog/designs/polarna_svjetlost.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/polje_lavande.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/sjene_ulice.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/sumska_svjetlost.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/svemirski_horizont.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/vodopad_u_magli.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/zlatni_horizont.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/designs/zlatno_polje.html`

Linija oko 5:
```txt
0003: 
0004: {% block content %}
0005:     {% include "blog/components/blog_design_styles.html" %}
0006:     <style>
0007: body {
```
### `blog/templates/blog/layouts/blog_design_base.html`

Linija oko 18:
```txt
0016: 
0017: {% block content %}
0018:     {% include "blog/components/blog_design_styles.html" %}
0019:     {% include "blog/components/blog_posts.html" %}
0020: {% endblock %}
```

## Pregled ključnih datoteka

| Datoteka | Postoji | Linija | Custom refs | Profile refs | CSS var refs | !important | Inline style |
|---|---:|---:|---:|---:|---:|---:|---:|
| `blog/templates/blog/components/blog_design_styles.html` | da | 2634 | 62 | 10 | 205 | 287 | 0 |
| `blog/templates/blog/base.html` | da | 3534 | 51 | 19 | 89 | 81 | 10 |
| `blog/static/blog/css/blog_settings.css` | da | 3258 | 0 | 31 | 0 | 35 | 22 |
| `blog/templates/blog/layouts/blog_design_base.html` | da | 20 | 0 | 0 | 0 | 0 | 0 |
| `blog/templates/blog/components/blog_posts.html` | da | 28 | 0 | 0 | 0 | 0 | 0 |
| `blog/templates/blog/components/post_card.html` | da | 72 | 4 | 0 | 0 | 0 | 3 |
| `blog/templates/blog/components/blog_box.html` | da | 10 | 0 | 0 | 0 | 0 | 0 |
| `blog/templates/blog/components/blog_left_sidebar.html` | da | 155 | 1 | 0 | 0 | 0 | 12 |
| `blog/templates/blog/components/blog_right_sidebar.html` | da | 175 | 1 | 0 | 0 | 0 | 12 |

## Fieldovi korisničkih postavki u centralnom layeru

| Field | U `blog_design_styles.html` | U projektu ukupno |
|---|---:|---:|
| `outer_background_pattern` | 12 | 50 |
| `outer_background_color_1` | 9 | 50 |
| `outer_background_mode` | 9 | 60 |
| `outer_background_asset` | 7 | 14 |
| `content_border_color` | 6 | 44 |
| `header_background_color_1` | 5 | 49 |
| `content_background_color` | 3 | 45 |
| `header_background_color_2` | 2 | 39 |
| `header_background_gradient_direction` | 2 | 38 |
| `header_background_mode` | 2 | 42 |
| `box_background_color` | 1 | 42 |
| `box_border_color` | 1 | 38 |
| `outer_background_color_2` | 1 | 40 |
| `outer_background_gradient_direction` | 1 | 40 |
| `right_box_columns` | 1 | 53 |
| `blog_title_color` | 0 | 58 |
| `blog_title_font` | 0 | 61 |
| `blog_title_font_stack` | 0 | 6 |
| `blog_title_size` | 0 | 31 |
| `body_font` | 0 | 48 |
| `body_font_stack` | 0 | 6 |
| `body_text_color` | 0 | 46 |
| `box_title_color` | 0 | 58 |
| `box_title_font` | 0 | 61 |
| `box_title_font_stack` | 0 | 6 |
| `box_title_size` | 0 | 31 |
| `outer_background_image` | 0 | 41 |
| `post_date_color` | 0 | 106 |
| `post_date_color_1` | 0 | 26 |
| `post_date_color_2` | 0 | 18 |
| `post_date_effect` | 0 | 35 |
| `post_date_size` | 0 | 26 |
| `post_date_style` | 0 | 34 |
| `post_title_color` | 0 | 58 |
| `post_title_font` | 0 | 61 |
| `post_title_font_stack` | 0 | 6 |
| `post_title_size` | 0 | 31 |

## CSS varijable

| CSS varijabla | Definicije u centralnom layeru | Upotrebe u centralnom layeru | U projektu ukupno |
|---|---:|---:|---:|
| `--date-scale-factor` | 1 | 27 | 29 |
| `--date-primary` | 1 | 20 | 22 |
| `--date-secondary` | 1 | 12 | 16 |
| `--body-text-color` | 0 | 10 | 30 |
| `--post-date-color` | 0 | 8 | 28 |
| `--blog-title-color` | 0 | 6 | 41 |
| `--box-title-color` | 0 | 5 | 41 |
| `--post-title-color` | 0 | 5 | 55 |
| `--body-font` | 0 | 2 | 9 |
| `--blog-title-font` | 0 | 1 | 13 |
| `--blog-title-size` | 0 | 1 | 13 |
| `--box-title-font` | 0 | 1 | 13 |
| `--box-title-size` | 0 | 1 | 13 |
| `--post-title-font` | 0 | 1 | 12 |
| `--post-title-size` | 0 | 1 | 13 |
| `--box-background-color` | 0 | 0 | 1 |
| `--box-border-color` | 0 | 0 | 1 |
| `--content-background-color` | 0 | 0 | 1 |
| `--content-border-color` | 0 | 0 | 1 |
| `--outer-background-color-1` | 0 | 0 | 1 |
| `--outer-background-color-2` | 0 | 0 | 1 |
| `--outer-background-image` | 0 | 0 | 1 |

## CSS varijable definirane u `blog_design_styles.html`

```txt
0041: .calendar-title--nav::after,
0192: --bs-gutter-x: 18px;
0332: --bs-gutter-x: 18px;
0580: --bs-gutter-x: 18px;
0991: --bs-gutter-x: 0;
1292: --analytics-stat-card-bg: rgba(0,0,0,0.22);
1293: --analytics-stat-card-border: rgba(203,220,255,0.16);
1294: --analytics-stat-card-color: #e8f1ff;
1295: --analytics-stat-value-color: #ffffff;
1296: --analytics-stat-label-color: rgba(232,241,255,0.72);
1297: --analytics-stat-card-shadow: none;
1298: --analytics-page-row-bg: rgba(0,0,0,0.18);
1299: --analytics-page-row-border: rgba(203,220,255,0.14);
1300: --analytics-page-row-color: #e8f1ff;
1301: --analytics-map-card-bg: rgba(0,0,0,0.18);
1302: --analytics-map-card-border: rgba(203,220,255,0.16);
1303: --analytics-map-card-shadow: none;
1350: --bs-gutter-x: 22px;
1652: --analytics-stat-card-bg: rgba(255,255,255,0.28);
1653: --analytics-stat-card-border: rgba(137,151,138,0.22);
1654: --analytics-stat-card-color: #4f5d51;
1655: --analytics-stat-value-color: #3f4f43;
1656: --analytics-stat-label-color: rgba(79,93,81,0.68);
1657: --analytics-stat-card-shadow: none;
1658: --analytics-page-row-bg: rgba(255,255,255,0.26);
1659: --analytics-page-row-border: rgba(137,151,138,0.18);
1660: --analytics-page-row-color: #4f5d51;
1661: --analytics-map-card-bg: rgba(255,255,255,0.24);
1662: --analytics-map-card-border: rgba(137,151,138,0.2);
1663: --analytics-map-card-shadow: none;
1710: --bs-gutter-x: 22px;
2016: body { background-color:#111; color:#fff; --analytics-stat-card-bg: rgba(255,255,255,0.035); --analytics-stat-card-border: rgba(255,255,255,0.06); --analytics-stat-card-color: #f5f7fb; --analytics-stat-value-color: #ffffff; --analytics-stat-label-color: rgba(255,255,255,0.68); --analytics-stat-card-shadow: inset 0 1px 0 rgba(255,255,255,0.025); --analytics-page-row-bg: rgba(255,255,255,0.035); --analytics-page-row-border: rgba(255,255,255,0.06); --analytics-page-row-color: rgba(255,255,255,0.9); --analytics-map-card-bg: linear-gradient(180deg, rgba(20,20,24,0.98) 0%, rgba(26,26,32,0.98) 100%); --analytics-map-card-border: rgba(255,255,255,0.08); --analytics-map-card-shadow: 0 10px 22px rgba(0,0,0,0.26); }
2078: body { background:#f6f6f4; color:#1f1f1f; --analytics-stat-card-bg: #fbf8f2; --analytics-stat-card-border: rgba(122,44,255,0.12); --analytics-stat-card-color: #34291f; --analytics-stat-value-color: #5b3a22; --analytics-stat-label-color: #7b6b5c; --analytics-stat-card-shadow: 0 5px 14px rgba(122,44,255,0.05); --analytics-page-row-bg: #fbf8f2; --analytics-page-row-border: rgba(122,44,255,0.12); --analytics-page-row-color: #34291f; --analytics-map-card-bg: linear-gradient(180deg, rgba(251,248,242,0.98) 0%, rgba(245,239,231,0.98) 100%); --analytics-map-card-border: rgba(122,44,255,0.12); --analytics-map-card-shadow: 0 10px 22px rgba(122,44,255,0.07); }
2140: body { background:#ffffff; color:#1f2937; --analytics-stat-card-bg: #fffaf4; --analytics-stat-card-border: rgba(122,44,255,0.10); --analytics-stat-card-color: #3f3128; --analytics-stat-value-color: #6b4b2f; --analytics-stat-label-color: #7a6a5c; --analytics-stat-card-shadow: 0 5px 14px rgba(122,44,255,0.04); --analytics-page-row-bg: #fffaf4; --analytics-page-row-border: rgba(122,44,255,0.10); --analytics-page-row-color: #3f3128; --analytics-map-card-bg: linear-gradient(180deg, rgba(255,250,244,0.99) 0%, rgba(250,243,234,0.99) 100%); --analytics-map-card-border: rgba(122,44,255,0.10); --analytics-map-card-shadow: 0 10px 22px rgba(122,44,255,0.05); }
2263: --date-primary: var(--post-date-color-1, var(--post-date-color, #d97706));
2264: --date-secondary: var(--post-date-color-2, var(--post-date-color, #ffd200));
2265: --date-scale-factor: calc(var(--post-date-scale, 100) / 100);
2326: --date-day-color: var(--date-primary);
2327: --date-text-color: var(--date-primary);
2328: --date-muted-color: var(--date-primary);
2329: --date-accent-color: var(--date-primary);
2330: --date-bg-soft: color-mix(in srgb, var(--date-primary) 10%, transparent);
2334: --date-day-color: var(--date-primary);
2335: --date-text-color: var(--date-secondary);
2336: --date-muted-color: var(--date-secondary);
2337: --date-accent-color: var(--date-secondary);
2338: --date-bg-soft: color-mix(in srgb, var(--date-secondary) 12%, transparent);
2380: --date-day-color: var(--date-primary);
2381: --date-text-color: var(--date-secondary);
2382: --date-muted-color: var(--date-secondary);
2383: --date-accent-color: var(--date-secondary);
2384: --date-bg-soft: linear-gradient(135deg, color-mix(in srgb, var(--date-primary) 12%, transparent), color-mix(in srgb, var(--date-secondary) 12%, transparent));
```

## Snippetovi — `blog/templates/blog/components/blog_design_styles.html`

### active_design_customization

Linija oko 179:
```txt
0177: {% if blog.profile.template == 'default_right' or blog.profile.template == 'dark_right' or blog.profile.template == 'classic_right' %}
0178: 
0179: {% if blog_preferences.active_design_customization.right_box_columns == '2' %}
0180: <style>
0181: @media (min-width: 768px) {
```

Linija oko 444:
```txt
0442:     font-family: var(--body-font, Arial, Helvetica, sans-serif);
0443:     color: var(--body-text-color, #57534e);
0444:     {% if blog_preferences.active_design_customization.outer_background_mode == 'color' %}
0445:     background: {{ blog_preferences.active_design_customization.outer_background_color_1|default:'#efe4c9' }};
0446:     {% elif blog_preferences.active_design_customization.outer_background_mode == 'gradient' %}
```

Linija oko 445:
```txt
0443:     color: var(--body-text-color, #57534e);
0444:     {% if blog_preferences.active_design_customization.outer_background_mode == 'color' %}
0445:     background: {{ blog_preferences.active_design_customization.outer_background_color_1|default:'#efe4c9' }};
0446:     {% elif blog_preferences.active_design_customization.outer_background_mode == 'gradient' %}
0447:     background: linear-gradient({{ blog_preferences.active_design_customization.outer_background_gradient_direction|default:'to bottom' }}, {{ blog_preferences.active_design_customization.outer_background_color_1|default:'#efe4c9' }}, {{ blog_preferences.active_design_customization.outer_background_color_2|default:'#e1d0ac' }});
```

Linija oko 446:
```txt
0444:     {% if blog_preferences.active_design_customization.outer_background_mode == 'color' %}
0445:     background: {{ blog_preferences.active_design_customization.outer_background_color_1|default:'#efe4c9' }};
0446:     {% elif blog_preferences.active_design_customization.outer_background_mode == 'gradient' %}
0447:     background: linear-gradient({{ blog_preferences.active_design_customization.outer_background_gradient_direction|default:'to bottom' }}, {{ blog_preferences.active_design_customization.outer_background_color_1|default:'#efe4c9' }}, {{ blog_preferences.active_design_customization.outer_background_color_2|default:'#e1d0ac' }});
0448:     {% elif blog_preferences.active_design_customization.outer_background_mode == 'pattern' %}
```

### blog_title

Linija oko 10:
```txt
0008: .blog-page-title,
0009: .blog-page-title a {
0010:     font-family: var(--blog-title-font, Georgia, "Times New Roman", serif);
0011:     color: var(--blog-title-color, #3f3128) !important;
0012:     font-size: var(--blog-title-size, 32px);
```

Linija oko 11:
```txt
0009: .blog-page-title a {
0010:     font-family: var(--blog-title-font, Georgia, "Times New Roman", serif);
0011:     color: var(--blog-title-color, #3f3128) !important;
0012:     font-size: var(--blog-title-size, 32px);
0013:     line-height: 1.08;
```

Linija oko 12:
```txt
0010:     font-family: var(--blog-title-font, Georgia, "Times New Roman", serif);
0011:     color: var(--blog-title-color, #3f3128) !important;
0012:     font-size: var(--blog-title-size, 32px);
0013:     line-height: 1.08;
0014: }
```

Linija oko 21:
```txt
0019:     font-size: clamp(0.95rem, 0.9rem + 0.22vw, 1.12rem);
0020:     line-height: 1.45;
0021:     color: var(--blog-title-color, #3f3128) !important;
0022:     opacity: 0.82;
0023: }
```

### post_title

Linija oko 76:
```txt
0074: 
0075: .blog-post-entry h4,
0076: .blog-post-title {
0077:     font-family: var(--post-title-font, Georgia, "Times New Roman", serif) !important;
0078:     color: var(--post-title-color, #111827) !important;
```

Linija oko 77:
```txt
0075: .blog-post-entry h4,
0076: .blog-post-title {
0077:     font-family: var(--post-title-font, Georgia, "Times New Roman", serif) !important;
0078:     color: var(--post-title-color, #111827) !important;
0079:     font-size: var(--post-title-size, 24px) !important;
```

Linija oko 78:
```txt
0076: .blog-post-title {
0077:     font-family: var(--post-title-font, Georgia, "Times New Roman", serif) !important;
0078:     color: var(--post-title-color, #111827) !important;
0079:     font-size: var(--post-title-size, 24px) !important;
0080:     line-height: 1.18;
```

Linija oko 79:
```txt
0077:     font-family: var(--post-title-font, Georgia, "Times New Roman", serif) !important;
0078:     color: var(--post-title-color, #111827) !important;
0079:     font-size: var(--post-title-size, 24px) !important;
0080:     line-height: 1.18;
0081: }
```

### box

Linija oko 85:
```txt
0083: .calendar-title,
0084: .archive-title,
0085: .sidebar-box-title,
0086: .blog-box-title {
0087:     font-family: var(--box-title-font, Georgia, "Times New Roman", serif) !important;
```

Linija oko 86:
```txt
0084: .archive-title,
0085: .sidebar-box-title,
0086: .blog-box-title {
0087:     font-family: var(--box-title-font, Georgia, "Times New Roman", serif) !important;
0088:     color: var(--box-title-color, #3f3128) !important;
```

Linija oko 87:
```txt
0085: .sidebar-box-title,
0086: .blog-box-title {
0087:     font-family: var(--box-title-font, Georgia, "Times New Roman", serif) !important;
0088:     color: var(--box-title-color, #3f3128) !important;
0089:     font-size: var(--box-title-size, 13px) !important;
```

Linija oko 88:
```txt
0086: .blog-box-title {
0087:     font-family: var(--box-title-font, Georgia, "Times New Roman", serif) !important;
0088:     color: var(--box-title-color, #3f3128) !important;
0089:     font-size: var(--box-title-size, 13px) !important;
0090:     line-height: 1.18;
```

### banner

Linija oko 191:
```txt
0189:     .blog-main-layout-row,
0190:     .blog-header-wrap > .row,
0191:     .blog-banner-strip > .row {
0192:         --bs-gutter-x: 18px;
0193:         padding-left: 8px;
```

Linija oko 301:
```txt
0299:     .blog-main-layout-row,
0300:     .blog-header-wrap > .row,
0301:     .blog-banner-strip > .row {
0302:         padding-left: 12px;
0303:         padding-right: 12px;
```

Linija oko 331:
```txt
0329:     .blog-main-layout-row,
0330:     .blog-header-wrap > .row,
0331:     .blog-banner-strip > .row {
0332:         --bs-gutter-x: 18px;
0333:         padding-left: 8px;
```

Linija oko 417:
```txt
0415:     .blog-main-layout-row,
0416:     .blog-header-wrap > .row,
0417:     .blog-banner-strip > .row {
0418:         padding-left: 12px;
0419:         padding-right: 12px;
```

### css_vars

Linija oko 4:
```txt
0002: <style>
0003: body {
0004:     font-family: var(--body-font, Arial, Helvetica, sans-serif);
0005:     color: var(--body-text-color, #1f2937);
0006: }
```

Linija oko 5:
```txt
0003: body {
0004:     font-family: var(--body-font, Arial, Helvetica, sans-serif);
0005:     color: var(--body-text-color, #1f2937);
0006: }
0007: 
```

Linija oko 10:
```txt
0008: .blog-page-title,
0009: .blog-page-title a {
0010:     font-family: var(--blog-title-font, Georgia, "Times New Roman", serif);
0011:     color: var(--blog-title-color, #3f3128) !important;
0012:     font-size: var(--blog-title-size, 32px);
```

Linija oko 11:
```txt
0009: .blog-page-title a {
0010:     font-family: var(--blog-title-font, Georgia, "Times New Roman", serif);
0011:     color: var(--blog-title-color, #3f3128) !important;
0012:     font-size: var(--blog-title-size, 32px);
0013:     line-height: 1.08;
```

## Snippetovi — `blog/templates/blog/base.html`

### active_design_customization

Linija oko 1145:
```txt
1143: 
1144: <body class="{% if request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'register' and request.resolver_match.url_name != 'activation_sent' and request.resolver_match.url_name != 'author_onboarding' and request.resolver_match.url_name != 'password_reset' and request.resolver_match.url_name != 'password_reset_done' and request.resolver_match.url_name != 'password_reset_confirm' and request.resolver_match.url_name != 'password_reset_complete' %}blog-cursor-theme blog-cursor-{{ blog_preferences.cursor_style|default:'default' }} blog-cursor-effect-{{ blog_preferences.cursor_effect|default:'none' }}{% if blog_preferences.cursor_stylesheet_url %} blog-cursor-external-style{% endif %}{% endif %}" data-blog-cursor-effect="{{ blog_preferences.cursor_effect|default:'none' }}" style="
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
```

Linija oko 1146:
```txt
1144: <body class="{% if request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'register' and request.resolver_match.url_name != 'activation_sent' and request.resolver_match.url_name != 'author_onboarding' and request.resolver_match.url_name != 'password_reset' and request.resolver_match.url_name != 'password_reset_done' and request.resolver_match.url_name != 'password_reset_confirm' and request.resolver_match.url_name != 'password_reset_complete' %}blog-cursor-theme blog-cursor-{{ blog_preferences.cursor_style|default:'default' }} blog-cursor-effect-{{ blog_preferences.cursor_effect|default:'none' }}{% if blog_preferences.cursor_stylesheet_url %} blog-cursor-external-style{% endif %}{% endif %}" data-blog-cursor-effect="{{ blog_preferences.cursor_effect|default:'none' }}" style="
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
```

Linija oko 1147:
```txt
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
```

Linija oko 1148:
```txt
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
```

### blog_title

Linija oko 1145:
```txt
1143: 
1144: <body class="{% if request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'register' and request.resolver_match.url_name != 'activation_sent' and request.resolver_match.url_name != 'author_onboarding' and request.resolver_match.url_name != 'password_reset' and request.resolver_match.url_name != 'password_reset_done' and request.resolver_match.url_name != 'password_reset_confirm' and request.resolver_match.url_name != 'password_reset_complete' %}blog-cursor-theme blog-cursor-{{ blog_preferences.cursor_style|default:'default' }} blog-cursor-effect-{{ blog_preferences.cursor_effect|default:'none' }}{% if blog_preferences.cursor_stylesheet_url %} blog-cursor-external-style{% endif %}{% endif %}" data-blog-cursor-effect="{{ blog_preferences.cursor_effect|default:'none' }}" style="
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
```

Linija oko 1146:
```txt
1144: <body class="{% if request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'register' and request.resolver_match.url_name != 'activation_sent' and request.resolver_match.url_name != 'author_onboarding' and request.resolver_match.url_name != 'password_reset' and request.resolver_match.url_name != 'password_reset_done' and request.resolver_match.url_name != 'password_reset_confirm' and request.resolver_match.url_name != 'password_reset_complete' %}blog-cursor-theme blog-cursor-{{ blog_preferences.cursor_style|default:'default' }} blog-cursor-effect-{{ blog_preferences.cursor_effect|default:'none' }}{% if blog_preferences.cursor_stylesheet_url %} blog-cursor-external-style{% endif %}{% endif %}" data-blog-cursor-effect="{{ blog_preferences.cursor_effect|default:'none' }}" style="
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
```

Linija oko 1147:
```txt
1145:     --blog-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
```

Linija oko 1584:
```txt
1582:                         <div class="d-flex justify-content-between align-items-center mb-2">
1583:                             <a href="{% url 'user_blog' item.user.username %}" class="text-decoration-none">
1584:                                 {{ item.user.profile.blog_name }}
1585:                             </a>
1586:                 
```

### post_title

Linija oko 1148:
```txt
1146:     --blog-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#3f3128' }};
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
```

Linija oko 1149:
```txt
1147:     --blog-title-size: {{ blog_preferences.active_design_customization.blog_title_size|default:'32' }}px;
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
1151:     --box-title-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
```

Linija oko 1150:
```txt
1148:     --post-title-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
1151:     --box-title-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1152:     --box-title-color: {{ blog_preferences.active_design_customization.box_title_color|default:'#3f3128' }};
```

Linija oko 1641:
```txt
1639:                                 <div class="small text-muted">
1640:                                     <a href="{% url 'post_detail' c.post.id %}" class="text-decoration-none">
1641:                                         {{ c.post.title|truncatechars:35 }}
1642:                                     </a>
1643:                                 </div>
```

### box

Linija oko 1151:
```txt
1149:     --post-title-color: {{ blog_preferences.active_design_customization.post_title_color|default:'#111827' }};
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
1151:     --box-title-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1152:     --box-title-color: {{ blog_preferences.active_design_customization.box_title_color|default:'#3f3128' }};
1153:     --box-title-size: {{ blog_preferences.active_design_customization.box_title_size|default:'13' }}px;
```

Linija oko 1152:
```txt
1150:     --post-title-size: {{ blog_preferences.active_design_customization.post_title_size|default:'24' }}px;
1151:     --box-title-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1152:     --box-title-color: {{ blog_preferences.active_design_customization.box_title_color|default:'#3f3128' }};
1153:     --box-title-size: {{ blog_preferences.active_design_customization.box_title_size|default:'13' }}px;
1154:     --post-date-color: {{ blog_preferences.active_design_customization.post_date_color_1|default:blog_preferences.active_design_customization.post_date_color|default:'#d97706' }};
```

Linija oko 1153:
```txt
1151:     --box-title-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Georgia, Times New Roman, serif'|safe }};
1152:     --box-title-color: {{ blog_preferences.active_design_customization.box_title_color|default:'#3f3128' }};
1153:     --box-title-size: {{ blog_preferences.active_design_customization.box_title_size|default:'13' }}px;
1154:     --post-date-color: {{ blog_preferences.active_design_customization.post_date_color_1|default:blog_preferences.active_design_customization.post_date_color|default:'#d97706' }};
1155:     --post-date-color-1: {{ blog_preferences.active_design_customization.post_date_color_1|default:blog_preferences.active_design_customization.post_date_color|default:'#d97706' }};
```

Linija oko 3314:
```txt
3312:     --blog-title-color: {{ c.blog_title_color|default:'#3f3128' }};
3313:     --post-title-color: {{ c.post_title_color|default:'#111827' }};
3314:     --box-title-color: {{ c.box_title_color|default:'#3f3128' }};
3315:     --post-date-color: {{ c.post_date_color|default:'#7a2cff' }};
3316:     --body-text-color: {{ c.body_text_color|default:'#1f2937' }};
```

### css_vars

Linija oko 131:
```txt
0129:     }
0130:     .live-analytics-stats{
0131:         --analytics-stat-gap: 6px;
0132:         --analytics-stat-card-padding-y: 5px;
0133:         --analytics-stat-card-padding-x: 4px;
```

Linija oko 132:
```txt
0130:     .live-analytics-stats{
0131:         --analytics-stat-gap: 6px;
0132:         --analytics-stat-card-padding-y: 5px;
0133:         --analytics-stat-card-padding-x: 4px;
0134:         --analytics-stat-value-size: 0.88rem;
```

Linija oko 133:
```txt
0131:         --analytics-stat-gap: 6px;
0132:         --analytics-stat-card-padding-y: 5px;
0133:         --analytics-stat-card-padding-x: 4px;
0134:         --analytics-stat-value-size: 0.88rem;
0135:         --analytics-stat-label-size: 9px;
```

Linija oko 134:
```txt
0132:         --analytics-stat-card-padding-y: 5px;
0133:         --analytics-stat-card-padding-x: 4px;
0134:         --analytics-stat-value-size: 0.88rem;
0135:         --analytics-stat-label-size: 9px;
0136:         --analytics-stat-radius: 11px;
```

## Snippetovi — `blog/static/blog/css/blog_settings.css`

### blog_title

Linija oko 559:
```txt
0557: }
0558: 
0559: .design-live-preview-blog-title {
0560:     font-size: 3.1rem;
0561:     line-height: 1.04;
```

Linija oko 744:
```txt
0742:     }
0743: 
0744:     .design-live-preview-blog-title {
0745:         font-size: 2.1rem;
0746:     }
```

Linija oko 1762:
```txt
1760: }
1761: 
1762: .ambience-blog-title {
1763:     font-size: 1.45rem;
1764:     line-height: 1.05;
```

### post_title

Linija oko 646:
```txt
0644: }
0645: 
0646: .design-live-preview-post-title {
0647:     font-size: 2rem;
0648:     line-height: 1.16;
```

Linija oko 1827:
```txt
1825: }
1826: 
1827: .ambience-blog-post-title {
1828:     font-size: 1.12rem;
1829:     line-height: 1.15;
```

### box

Linija oko 592:
```txt
0590: }
0591: 
0592: .design-live-preview-box-title {
0593:     font-size: 0.98rem;
0594:     line-height: 1.2;
```

Linija oko 1804:
```txt
1802: }
1803: 
1804: .ambience-blog-box-title {
1805:     font-size: 0.98rem;
1806:     font-weight: 700;
```

### css_vars

Linija oko 484:
```txt
0482:     position: relative;
0483:     isolation: isolate;
0484:     --design-live-side-image: none;
0485:     border-radius: 18px;
0486:     padding: 16px;
```

Linija oko 504:
```txt
0502:     transition: opacity 0.18s ease;
0503:     background-color: transparent;
0504:     background-image: var(--design-live-side-image);
0505:     background-repeat: no-repeat;
0506:     background-position: center top;
```

Linija oko 2160:
```txt
2158: }
2159: 
2160: .ambience-effect-demo--none::before {
2161:     content: '';
2162:     position: absolute;
```

Linija oko 2169:
```txt
2167: }
2168: 
2169: .ambience-effect-demo--glow::before {
2170:     content: '';
2171:     position: absolute;
```

## Snippetovi — `blog/templates/blog/layouts/blog_design_base.html`

## Snippetovi — `blog/templates/blog/components/blog_posts.html`

## Snippetovi — `blog/templates/blog/components/post_card.html`

### active_design_customization

Linija oko 17:
```txt
0015: 
0016: 
0017:         <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-style="{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }}" data-date-effect="{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}">
0018: 
0019:             <div class="blog-date-main">
```

### post_title

Linija oko 9:
```txt
0007:         <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
0008: 
0009:             <h4 class="mb-0">{{ post.title }}</h4>
0010: 
0011:             {% include "blog/components/post_meta.html" %}
```

## Snippetovi — `blog/templates/blog/components/blog_box.html`

### box

Linija oko 8:
```txt
0006: {% endcomment %}
0007: <div class="sidebar-box {{ box_align|default:'sidebar-left-align' }}{% if blog.profile.template == 'simple_pattern' or blog.profile.template == 'simple_image' or blog.profile.template == 'simple_retro' %} sidebar-box--simple{% endif %}">
0008:     <div class="sidebar-box-title">{{ box.title }}</div>
0009:     <div class="sidebar-box-content">{{ box.content|safe }}</div>
0010: </div>
```

## Snippetovi — `blog/templates/blog/components/blog_left_sidebar.html`

### active_design_customization

Linija oko 2:
```txt
0001: {% load custom_tags %}
0002: {% with plus_columns=blog_preferences.active_design_customization.right_box_columns|default:'2' %}
0003: {% if blog.profile.template == 'default_right' or blog.profile.template == 'dark_right' or blog.profile.template == 'classic_right' %}
0004:     {% if plus_columns == '2' %}
```

### box

Linija oko 70:
```txt
0068: 
0069:         {% for box in left_boxes %}
0070:             {% include "blog/components/blog_box.html" with box=box box_align="sidebar-left-align" %}
0071:         {% endfor %}
0072: 
```

Linija oko 145:
```txt
0143:     {% for box in left_boxes %}
0144:         <div class="sidebar-box sidebar-left-align{% if blog.profile.template == 'simple_pattern' or blog.profile.template == 'simple_image' or blog.profile.template == 'simple_retro' %} sidebar-box--simple{% endif %}">
0145:             <div class="sidebar-box-title">{{ box.title }}</div>
0146:             <div class="sidebar-box-content">{{ box.content|safe }}</div>
0147:         </div>
```

## Snippetovi — `blog/templates/blog/components/blog_right_sidebar.html`

### active_design_customization

Linija oko 2:
```txt
0001: {% load custom_tags %}
0002: {% with plus_columns=blog_preferences.active_design_customization.right_box_columns|default:'2' %}
0003: {% if blog.profile.template == 'default_right' or blog.profile.template == 'dark_right' or blog.profile.template == 'classic_right' %}
0004: <div class="page-top-align blog-sidebar-stack--wide blog-sidebar-stack--right">
```

### box

Linija oko 72:
```txt
0070: 
0071:         {% for box in left_boxes %}
0072:             {% include "blog/components/blog_box.html" with box=box box_align="sidebar-left-align" %}
0073:         {% endfor %}
0074: 
```

Linija oko 85:
```txt
0083: 
0084:     {% for box in right_boxes %}
0085:         {% include "blog/components/blog_box.html" with box=box box_align="sidebar-right-align" %}
0086:     {% endfor %}
0087: 
```

Linija oko 162:
```txt
0160:     {% if blog.profile.template == 'simple_retro' %}
0161:         {% for box in left_boxes %}
0162:             {% include "blog/components/blog_box.html" with box=box box_align="sidebar-right-align" %}
0163:         {% endfor %}
0164:     {% endif %}
```

Linija oko 167:
```txt
0165: 
0166:     {% for box in right_boxes %}
0167:         {% include "blog/components/blog_box.html" with box=box box_align="sidebar-right-align" %}
0168:     {% endfor %}
0169: 
```

## Što ovo znači

- Ako `blog_design_styles.html` već prima `active_design_customization`, to je najbolje mjesto za centralno postavljanje korisničkih CSS varijabli.
- Sljedeća promjena koda treba biti mala i ograničena na centralni layer, ne na pojedinačne dizajne.
- Prvo treba testirati obične dizajne koji koriste zajednički layout.
- Posebni dizajni neće automatski sve slušati dok se njihove klase ne povežu s istim varijablama.

## Preporučeni sljedeći korak

1. Spremiti ovaj audit u git.
2. Otvoriti `blog/templates/blog/components/blog_design_styles.html`.
3. Napraviti jednu malu promjenu u centralnom layeru: jasnije definirati CSS varijable za naslov bloga, naslov posta, tekst, boxeve i datum.
4. Ne dirati posebne dizajne u toj promjeni.
5. Testirati `default`, `classic`, `simple`, jedan srednji tematski dizajn i tek onda pogledati jedan posebni dizajn.