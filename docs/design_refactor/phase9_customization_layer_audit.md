# Phase 9 — audit centralnog customization layera

Izrađeno: 2026-07-01 22:29:08

## Sažetak

- Skenirano datoteka: **183**
- Skenirano dizajnova: **42**
- Rizik nizak: **0**
- Rizik srednji: **31**
- Rizik visok: **11**

## Grupe dizajnova

- `zajednicki_layout`: **24**
- `posebni`: **9**
- `simple`: **4**
- `right_sidebar`: **3**
- `posebni_hero`: **2**

## Najjači kandidati za centralni customization layer

Ovo su datoteke u kojima se najviše pojavljuju customization fieldovi ili CSS varijable. Tu najvjerojatnije treba tražiti postojeći mehanizam i tu ga kasnije nadograditi, umjesto da se svaka tema ručno popravlja.

| Datoteka | Score | Custom refs | CSS var defs | CSS var uses | Preferences | Profile |
|---|---:|---:|---:|---:|---:|---:|
| `blog/templates/blog/components/blog_design_styles.html` | 262 | 62 | 85 | 115 | 62 | 22 |
| `blog/templates/blog/base.html` | 195 | 19 | 62 | 114 | 42 | 4 |
| `blog/static/blog/css/blog_settings.css` | 96 | 0 | 95 | 1 | 0 | 0 |
| `blog/templates/blog/designs/magazin.html` | 76 | 21 | 17 | 38 | 29 | 7 |
| `blog/templates/blog/designs/studio.html` | 74 | 18 | 16 | 40 | 26 | 10 |
| `blog/templates/blog/design_live_editor.html` | 47 | 47 | 0 | 0 | 0 | 0 |
| `blog/templates/blog/designs/nebesko_polje.html` | 41 | 4 | 20 | 17 | 4 | 0 |
| `blog/static/css/style.css` | 34 | 0 | 18 | 16 | 0 | 0 |
| `blog/static/blog/css/style.css` | 31 | 0 | 16 | 15 | 0 | 0 |
| `blog/templates/blog/designs/zlatno_polje.html` | 26 | 0 | 15 | 11 | 0 | 0 |
| `blog/templates/blog/designs/nebeski_mir.html` | 21 | 0 | 13 | 8 | 0 | 0 |
| `blog/templates/blog/designs/planine_u_magli.html` | 21 | 0 | 13 | 8 | 0 | 0 |
| `blog/templates/blog/designs/vodopad_u_magli.html` | 21 | 0 | 13 | 8 | 0 | 0 |
| `blog/templates/blog/designs/morski_prijelaz.html` | 19 | 0 | 13 | 6 | 0 | 0 |
| `blog/templates/blog/designs/podvodna_tisina.html` | 19 | 0 | 13 | 6 | 0 | 0 |
| `blog/templates/blog/designs/asfaltni_plamen.html` | 16 | 0 | 13 | 3 | 0 | 0 |
| `blog/templates/blog/designs/carobna_ljubicasta.html` | 16 | 0 | 13 | 3 | 0 | 0 |
| `blog/templates/blog/designs/dimni_akordi.html` | 16 | 0 | 13 | 3 | 0 | 0 |
| `blog/templates/blog/designs/iznad_oblaka.html` | 16 | 0 | 13 | 3 | 0 | 0 |
| `blog/templates/blog/designs/kraljevska_pozornica.html` | 16 | 0 | 13 | 3 | 0 | 0 |

## Ključna polja korisničkih postavki

### Najčešće pronađeni active_design_customization fieldovi

- `outer_background_pattern`: 13
- `outer_background_mode`: 12
- `outer_background_color_1`: 12
- `outer_background_asset`: 11
- `post_date_style`: 9
- `post_date_effect`: 9
- `content_border_color`: 9
- `header_background_color_1`: 7
- `content_background_color`: 7
- `blog_title_color`: 6
- `blog_title_size`: 6
- `post_title_color`: 6
- `post_title_size`: 6
- `box_title_color`: 6
- `box_title_size`: 6
- `post_date_color`: 6
- `post_date_color_1`: 4
- `post_date_size`: 4
- `box_background_color`: 4
- `blog_title_font_stack`: 3
- `post_title_font_stack`: 3
- `box_title_font_stack`: 3
- `post_date_color_2`: 3
- `body_font_stack`: 3
- `body_text_color`: 3
- `right_box_columns`: 3
- `box_border_color`: 3
- `blog_title_font`: 3
- `post_title_font`: 3
- `box_title_font`: 3
- `outer_background_image`: 3
- `outer_background_gradient_direction`: 2
- `outer_background_color_2`: 2
- `header_background_mode`: 2
- `header_background_gradient_direction`: 2
- `header_background_color_2`: 2

### Slaba ili nedostajuća ključna polja

Nema potpuno nedostajućih ključnih polja iz osnovnog popisa.

Nema vrlo rijetkih ključnih polja iz osnovnog popisa.

## Banner i profile fieldovi

- `blog_banner`: 21
- `blog_banner_display`: 1
- `blog_banner_size`: 1
- `blog_banner_position`: 2
- `blog_banner_focus`: 1
- `simple_background_image`: 9

## CSS varijable

### Najčešće korištene varijable
- `post-title-color`: 46
- `blog-title-color`: 32
- `box-title-color`: 32
- `date-scale-factor`: 27
- `body-text-color`: 26
- `date-primary`: 20
- `dx`: 15
- `dy`: 15
- `post-date-color`: 14
- `size`: 13
- `rotate`: 12
- `date-secondary`: 12
- `soho-text`: 10
- `magazin-text`: 9
- `soho-main-gap`: 7
- `sd-x`: 6
- `sd-y`: 6
- `sd-rotate`: 6
- `sd-scale`: 6
- `magazin-box-title`: 6
- `soho-box-title`: 6
- `date-bg-soft`: 5
- `soho-content-border`: 5
- `bulb-color`: 4
- `blog-title-font`: 4
- `box-title-font`: 4
- `date-accent-color`: 4
- `magazin-main-bg`: 4
- `nebesko-content-border`: 4
- `panel-bg`: 4
- `panel-border`: 4
- `blog-title-size`: 3
- `post-title-font`: 3
- `post-title-size`: 3
- `box-title-size`: 3

### Najčešće definirane varijable
- `bulb-color`: 32
- `bs-gutter-x`: 30
- `analytics-stat-card-bg`: 25
- `analytics-stat-card-border`: 25
- `analytics-stat-card-color`: 25
- `analytics-stat-value-color`: 25
- `analytics-stat-label-color`: 25
- `analytics-stat-card-shadow`: 25
- `analytics-page-row-bg`: 25
- `analytics-page-row-border`: 25
- `analytics-page-row-color`: 25
- `analytics-map-card-bg`: 25
- `analytics-map-card-border`: 25
- `analytics-map-card-shadow`: 25
- `rainbow-orbit`: 6
- `silk-tail`: 6
- `ocean-tail`: 6
- `ember-tail`: 6
- `moon-tail`: 6
- `forest-tail`: 6
- `stardust`: 5
- `sparkles`: 4
- `dots`: 4
- `mist`: 4
- `rings`: 4
- `hearts`: 4
- `embers`: 4
- `neon`: 4
- `electric`: 4
- `crystals`: 4
- `comet-trail`: 4
- `love-shot`: 4
- `confetti-burst`: 4
- `bubble-pop`: 4
- `analytics-stat-gap`: 3

## Dizajni — pregled rizika

| Dizajn | Grupa | Rizik | Ključni custom fields | Ključni profile fields | CSS var uses | !important | Direktne boje | Razlog |
|---|---|---|---:|---:|---:|---:|---:|---|
| `asfaltni_plamen` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 47 | 66 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `carobna_ljubicasta` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 51 | 131 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `classic` | `zajednicki_layout` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `classic_right` | `right_sidebar` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `dark` | `zajednicki_layout` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `dark_right` | `right_sidebar` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `default` | `zajednicki_layout` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `default_right` | `right_sidebar` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `dimni_akordi` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 47 | 65 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `iznad_oblaka` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 45 | 72 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `jedro_u_suton` | `posebni` | **visok** | 0 | 1 | 2 | 30 | 97 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `kraljevska_pozornica` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 30 | 117 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `litica_noci` | `zajednicki_layout` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `magazin` | `posebni_hero` | **visok** | 17 | 1 | 38 | 52 | 33 | poseban layout, puno !important, mnogo direktnih boja, inline style |
| `misticno_jezero` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 109 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `mjesecev_ples` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 48 | 67 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `morski_prijelaz` | `zajednicki_layout` | **srednji** | 0 | 0 | 6 | 45 | 69 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `nebeska_klasika` | `posebni` | **visok** | 0 | 1 | 2 | 26 | 95 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `nebeski_mir` | `zajednicki_layout` | **srednji** | 0 | 0 | 8 | 42 | 61 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `nebesko_polje` | `zajednicki_layout` | **srednji** | 4 | 0 | 17 | 36 | 116 | puno !important, mnogo direktnih boja |
| `neonski_grad` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 50 | 105 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `planine_u_magli` | `zajednicki_layout` | **srednji** | 0 | 0 | 8 | 45 | 77 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `podvodna_tisina` | `zajednicki_layout` | **srednji** | 0 | 0 | 6 | 37 | 61 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `polarna_svjetlost` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 48 | 73 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `polje_lavande` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 53 | 76 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `ponocna_elegancija` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 103 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `ruzicasti_vrt` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 103 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `simple` | `simple` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `simple_image` | `simple` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `simple_pattern` | `simple` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `simple_retro` | `simple` | **srednji** | 0 | 0 | 0 | 0 | 0 | nema ključnih customization fieldova, malo CSS varijabli |
| `sjene_ulice` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 53 | 70 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `stara_aleja` | `posebni` | **visok** | 0 | 1 | 2 | 30 | 97 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `staza_prema_vrhovima` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 92 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `studio` | `posebni_hero` | **visok** | 15 | 3 | 40 | 41 | 25 | poseban layout, puno !important, inline style |
| `sumska_svjetlost` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 52 | 74 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `svemirski_horizont` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 48 | 73 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `vecer_uz_jezero` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 104 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `vecer_zaljubljenih` | `posebni` | **visok** | 0 | 1 | 2 | 28 | 105 | poseban layout, nema ključnih customization fieldova, malo CSS varijabli, puno !important, mnogo direktnih boja, inline style |
| `vodopad_u_magli` | `zajednicki_layout` | **srednji** | 0 | 0 | 8 | 32 | 70 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `zlatni_horizont` | `zajednicki_layout` | **srednji** | 0 | 0 | 3 | 48 | 73 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |
| `zlatno_polje` | `zajednicki_layout` | **srednji** | 0 | 0 | 11 | 59 | 73 | nema ključnih customization fieldova, puno !important, mnogo direktnih boja |

## Što ovo znači

- Prvo treba pronaći i ojačati centralno mjesto koje generira CSS varijable iz korisničkih postavki.
- Dizajni koji već koriste zajednički layout trebaju dobiti korisničke postavke bez ručnog popravljanja svakog dizajna.
- Posebni dizajni trebaju se kasnije prilagoditi da koriste iste CSS varijable, ali jedan po jedan.
- Ne treba sada dodavati nove vizualne opcije poput rubova dok osnovna pravila ne rade svugdje.

## Preporučeni sljedeći korak

1. Otvoriti datoteke iz tablice 'Najjači kandidati za centralni customization layer'.
2. Provjeriti gdje se već postavljaju CSS varijable za naslov bloga, naslov posta, tekst, boxeve i pozadinu.
3. Napraviti malu promjenu samo u centralnom layeru, ne u pojedinačnim dizajnima.
4. Testirati na `default`, `classic`, `simple`, jednom srednjem tematskom dizajnu i jednom posebnom dizajnu bez očekivanja da posebni odmah radi savršeno.

## Datoteke

- Markdown: `docs/design_refactor/phase9_customization_layer_audit.md`
- JSON: `docs/design_refactor/phase9_customization_layer_audit.json`
