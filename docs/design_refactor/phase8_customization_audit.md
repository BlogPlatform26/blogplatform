# Phase 8 — audit korisničkih postavki dizajna

Izrađeno: 2026-07-01 22:18:35

## Sažetak

- Skenirano dizajnova: **42**
- Skenirano HTML template datoteka: **114**
- Posebnih dizajnova: **11**
- Cilj audita: pronaći gdje dizajn može pregaziti korisničke postavke.

### Grupe dizajnova

- `posebni_hero`: **2**
- `posebni_single_sidebar`: **9**
- `right_sidebar`: **3**
- `simple`: **4**
- `zajednicki_layout`: **24**

### Procjena rizika

- nizak: **11**
- srednji: **20**
- visok: **11**

## Najčešće korištene postavke / varijable

### active_design_customization

- `blog_title_color`: 5
- `box_title_color`: 5
- `post_date_effect`: 5
- `post_date_style`: 5
- `post_title_color`: 5
- `content_background_color`: 5
- `post_date_color`: 4
- `box_background_color`: 4
- `content_border_color`: 4
- `outer_background_color_1`: 4
- `blog_title_font_stack`: 3
- `blog_title_size`: 3
- `body_font_stack`: 3
- `body_text_color`: 3
- `box_title_font_stack`: 3
- `box_title_size`: 3
- `post_title_font_stack`: 3
- `post_title_size`: 3
- `box_border_color`: 3
- `header_background_color_1`: 3
- `outer_background_asset`: 3
- `right_box_columns`: 3
- `post_date_color_1`: 2
- `post_date_color_2`: 2
- `post_date_size`: 2

### blog_preferences

- `analytics_widget_side`: 15
- `blog_archive_mode`: 14
- `active_design_customization`: 8
- `analytics_active_pages_enabled`: 3
- `analytics_live_counter_enabled`: 3
- `analytics_map_enabled`: 3
- `analytics_map_variant`: 3
- `ambient_music_enabled`: 2
- `ambient_music_track_data`: 2
- `ambient_music_volume`: 2
- `cursor_effect`: 2
- `cursor_style`: 2
- `analytics_stat_card_size`: 2
- `analytics_geo_enabled`: 2
- `cursor_css`: 1
- `cursor_pointer_css`: 1
- `cursor_stylesheet_url`: 1
- `ambient_music_track`: 1
- `allow_comments`: 1
- `posts_per_page`: 1
- `show_post_comments`: 1

### blog.profile

- `blog_name`: 15
- `blog_tagline`: 13
- `blog_banner`: 11
- `template`: 8
- `simple_background_image`: 3
- `has_active_premium`: 3
- `avatar`: 3
- `blog_banner_position`: 2
- `allow_author_questions`: 1
- `blog_banner_display`: 1
- `blog_banner_focus`: 1
- `blog_banner_size`: 1

### CSS varijable

- `post-title-color`: 31
- `blog-title-color`: 23
- `box-title-color`: 23
- `body-text-color`: 7
- `post-date-color`: 6
- `blog-title-font`: 3
- `box-title-font`: 3
- `blog-title-size`: 2
- `box-title-size`: 2
- `post-title-font`: 2
- `post-title-size`: 2
- `analytics-map-card-bg`: 1
- `analytics-map-card-border`: 1
- `analytics-map-card-shadow`: 1
- `analytics-page-row-bg`: 1
- `analytics-page-row-border`: 1
- `analytics-page-row-color`: 1
- `analytics-stat-card-bg`: 1
- `analytics-stat-card-border`: 1
- `analytics-stat-card-color`: 1
- `analytics-stat-card-padding-x`: 1
- `analytics-stat-card-padding-y`: 1
- `analytics-stat-card-shadow`: 1
- `analytics-stat-gap`: 1
- `analytics-stat-label-color`: 1

## Tablica dizajnova

| Dizajn | Grupa | Extends | Rizik | Custom fields | CSS var | !important | Inline style | Direktne boje/pozadine | Razlog |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| `jedro_u_suton` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 30 | 3 | 63 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `magazin` | `posebni_hero` | `blog/base.html` | **visok** | 18 | 15 | 52 | 3 | 39 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `misticno_jezero` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 1 | 72 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `nebeska_klasika` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 26 | 1 | 64 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `ponocna_elegancija` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 1 | 70 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `ruzicasti_vrt` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 1 | 69 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `stara_aleja` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 30 | 1 | 63 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `staza_prema_vrhovima` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 2 | 61 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `studio` | `posebni_hero` | `blog/base.html` | **visok** | 15 | 13 | 41 | 3 | 35 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `vecer_uz_jezero` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 1 | 70 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `vecer_zaljubljenih` | `posebni_single_sidebar` | `blog/base.html` | **visok** | 0 | 1 | 28 | 1 | 71 | poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila |
| `asfaltni_plamen` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 47 | 0 | 38 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `carobna_ljubicasta` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 51 | 0 | 56 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `dimni_akordi` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 47 | 0 | 37 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `iznad_oblaka` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 45 | 0 | 48 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `kraljevska_pozornica` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 30 | 0 | 53 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `mjesecev_ples` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 48 | 0 | 39 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `morski_prijelaz` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 4 | 45 | 0 | 40 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `nebeski_mir` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 5 | 42 | 0 | 41 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `nebesko_polje` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 4 | 12 | 36 | 0 | 50 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `neonski_grad` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 50 | 0 | 50 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `planine_u_magli` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 5 | 45 | 0 | 46 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `podvodna_tisina` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 4 | 37 | 0 | 37 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `polarna_svjetlost` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 48 | 0 | 48 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `polje_lavande` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 53 | 0 | 50 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `sjene_ulice` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 53 | 0 | 39 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `sumska_svjetlost` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 52 | 0 | 51 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `svemirski_horizont` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 48 | 0 | 48 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `vodopad_u_magli` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 5 | 32 | 0 | 42 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `zlatni_horizont` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 3 | 48 | 0 | 48 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `zlatno_polje` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **srednji** | 0 | 5 | 59 | 0 | 50 | više !important pravila, mnogo direktnih boja/pozadina u CSS-u |
| `classic` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `classic_right` | `right_sidebar` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `dark` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `dark_right` | `right_sidebar` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `default` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `default_right` | `right_sidebar` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `litica_noci` | `zajednicki_layout` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `simple` | `simple` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `simple_image` | `simple` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `simple_pattern` | `simple` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |
| `simple_retro` | `simple` | `blog/layouts/blog_design_base.html` | **nizak** | 0 | 0 | 0 | 0 | 0 | — |

## Dizajni koji imaju malo customization/css-var referenci

Ovo ne znači automatski da su pokvareni, ali su kandidati da dizajn jače nameće svoj stil i slabije sluša korisničke postavke.

- `jedro_u_suton` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `misticno_jezero` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `nebeska_klasika` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `ponocna_elegancija` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `ruzicasti_vrt` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `stara_aleja` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `staza_prema_vrhovima` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `vecer_uz_jezero` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `vecer_zaljubljenih` — grupa `posebni_single_sidebar`, rizik **visok**, custom refs 0, css vars 1
- `classic` — grupa `zajednicki_layout`, rizik **nizak**, custom refs 0, css vars 0
- `classic_right` — grupa `right_sidebar`, rizik **nizak**, custom refs 0, css vars 0
- `dark` — grupa `zajednicki_layout`, rizik **nizak**, custom refs 0, css vars 0
- `dark_right` — grupa `right_sidebar`, rizik **nizak**, custom refs 0, css vars 0
- `default` — grupa `zajednicki_layout`, rizik **nizak**, custom refs 0, css vars 0
- `default_right` — grupa `right_sidebar`, rizik **nizak**, custom refs 0, css vars 0
- `litica_noci` — grupa `zajednicki_layout`, rizik **nizak**, custom refs 0, css vars 0
- `simple` — grupa `simple`, rizik **nizak**, custom refs 0, css vars 0
- `simple_image` — grupa `simple`, rizik **nizak**, custom refs 0, css vars 0
- `simple_pattern` — grupa `simple`, rizik **nizak**, custom refs 0, css vars 0
- `simple_retro` — grupa `simple`, rizik **nizak**, custom refs 0, css vars 0

## Posebni dizajni

Ove dizajne treba popravljati jedan po jedan, jer imaju vlastiti HTML/CSS i veći rizik da pregaze korisničke postavke.

### `jedro_u_suton`

- File: `blog/templates/blog/designs/jedro_u_suton.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 63
- `!important`: 30
- Inline style: 3

### `magazin`

- File: `blog/templates/blog/designs/magazin.html`
- Grupa: `posebni_hero`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove
- Custom fields: `blog_title_color`, `blog_title_font_stack`, `body_font_stack`, `body_text_color`, `box_background_color`, `box_border_color`, `box_title_color`, `box_title_font_stack`, `content_background_color`, `content_border_color`, +8
- Profile fields: `avatar`, `blog_name`, `blog_tagline`, `simple_background_image`
- CSS varijable: `magazin-body-font`, `magazin-box-font`, `magazin-box-title`, `magazin-content-bg`, `magazin-content-border`, `magazin-date`, `magazin-main-bg`, `magazin-post-font`, `magazin-post-title`, `magazin-section-bg`, +5
- Direktne boje/pozadine: 39
- `!important`: 52
- Inline style: 3

### `misticno_jezero`

- File: `blog/templates/blog/designs/misticno_jezero.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 72
- `!important`: 28
- Inline style: 1

### `nebeska_klasika`

- File: `blog/templates/blog/designs/nebeska_klasika.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 64
- `!important`: 26
- Inline style: 1

### `ponocna_elegancija`

- File: `blog/templates/blog/designs/ponocna_elegancija.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 70
- `!important`: 28
- Inline style: 1

### `ruzicasti_vrt`

- File: `blog/templates/blog/designs/ruzicasti_vrt.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 69
- `!important`: 28
- Inline style: 1

### `stara_aleja`

- File: `blog/templates/blog/designs/stara_aleja.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 63
- `!important`: 30
- Inline style: 1

### `staza_prema_vrhovima`

- File: `blog/templates/blog/designs/staza_prema_vrhovima.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 61
- `!important`: 28
- Inline style: 2

### `studio`

- File: `blog/templates/blog/designs/studio.html`
- Grupa: `posebni_hero`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove
- Custom fields: `blog_title_color`, `blog_title_font_stack`, `body_font_stack`, `body_text_color`, `box_title_color`, `box_title_font_stack`, `content_background_color`, `content_border_color`, `outer_background_asset`, `outer_background_color_1`, +5
- Profile fields: `avatar`, `blog_banner`, `blog_banner_position`, `blog_name`, `blog_tagline`, `simple_background_image`
- CSS varijable: `soho-body-font`, `soho-box-font`, `soho-box-title`, `soho-content-bg`, `soho-content-border`, `soho-date`, `soho-main-gap`, `soho-page-bg`, `soho-post-font`, `soho-post-title`, +3
- Direktne boje/pozadine: 35
- `!important`: 41
- Inline style: 3

### `vecer_uz_jezero`

- File: `blog/templates/blog/designs/vecer_uz_jezero.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 70
- `!important`: 28
- Inline style: 1

### `vecer_zaljubljenih`

- File: `blog/templates/blog/designs/vecer_zaljubljenih.html`
- Grupa: `posebni_single_sidebar`
- Rizik: **visok**
- Razlozi: poseban dizajn, ne koristi zajednički blog_design_base layout, više !important pravila, ima inline style, mnogo direktnih boja/pozadina u CSS-u, dizajn direktno nameće fontove, malo customization/css-var referenci
- Custom fields: —
- Profile fields: `blog_banner`, `blog_name`, `blog_tagline`
- CSS varijable: `post-title-color`
- Direktne boje/pozadine: 71
- `!important`: 28
- Inline style: 1

## Što ovo znači

- Dizajn smije imati svoj zadani izgled, ali korisnikova postavka mora imati prednost.
- Najveći rizik su posebni dizajni koji imaju vlastiti HTML/CSS, direktne boje, inline style i `!important` pravila.
- Ne treba sve dizajne popravljati odjednom.
- Prvo treba napraviti centralno mjesto za korisničke postavke, pa zatim dizajne provjeravati po grupama.

## Preporučeni sljedeći korak

1. Ne popravljati više banner napamet.
2. Napraviti plan koje postavke moraju raditi svugdje.
3. Prvo provjeriti zajednički layout, jer on pokriva najviše dizajnova.
4. Posebne dizajne raditi jedan po jedan tek nakon što znamo koje postavke moraju pobijediti dizajn.

## Datoteke

- JSON: `docs/design_refactor/phase8_customization_audit.json`
- Markdown: `docs/design_refactor/phase8_customization_audit.md`
