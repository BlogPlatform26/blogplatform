# Phase 23 — audit posebnih dizajna i zajedničkih komponenti

Izrađeno: 2026-07-04 19:52:49

## Cilj

Provjeriti koji dizajni već koriste zajednički layout/komponente, a koji još imaju vlastiti prikaz postova, boxeva, gumba, komentara ili formi. Ovo je read-only audit i ne mijenja aplikaciju.

## Sažetak

- Template dizajna ukupno: **42**
- Dizajni koji su posebni ili djelomično posebni: **11**
- `common_layout_with_custom_bits`: **31**
- `special_full_custom`: **11**

## Rizik

- nizak: **0**
- srednji: **31**
- visok: **11**

## Pregled dizajnova

| Dizajn | Grupa | Rizik | Common layout | Shared posts | Shared box/sidebar | Direct post loop | Sidebar/form hitovi |
|---|---|---|---:|---:|---:|---:|---:|
| `asfaltni_plamen` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 39 |
| `carobna_ljubicasta` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 59 |
| `classic` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `classic_right` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `dark` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `dark_right` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `default` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `default_right` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `dimni_akordi` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 39 |
| `iznad_oblaka` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `jedro_u_suton` | `special_full_custom` | visok | ne | ne | ne | 2 | 61 |
| `kraljevska_pozornica` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 44 |
| `litica_noci` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `magazin` | `special_full_custom` | visok | ne | ne | ne | 2 | 68 |
| `misticno_jezero` | `special_full_custom` | visok | ne | ne | ne | 2 | 57 |
| `mjesecev_ples` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 39 |
| `morski_prijelaz` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 45 |
| `nebeska_klasika` | `special_full_custom` | visok | ne | ne | ne | 2 | 55 |
| `nebeski_mir` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `nebesko_polje` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 47 |
| `neonski_grad` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 49 |
| `planine_u_magli` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 47 |
| `podvodna_tisina` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 45 |
| `polarna_svjetlost` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `polje_lavande` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 53 |
| `ponocna_elegancija` | `special_full_custom` | visok | ne | ne | ne | 2 | 57 |
| `ruzicasti_vrt` | `special_full_custom` | visok | ne | ne | ne | 2 | 57 |
| `simple` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `simple_image` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `simple_pattern` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `simple_retro` | `common_layout_with_custom_bits` | srednji | da | ne | ne | 0 | 0 |
| `sjene_ulice` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 38 |
| `stara_aleja` | `special_full_custom` | visok | ne | ne | ne | 2 | 62 |
| `staza_prema_vrhovima` | `special_full_custom` | visok | ne | ne | ne | 2 | 59 |
| `studio` | `special_full_custom` | visok | ne | ne | ne | 2 | 68 |
| `sumska_svjetlost` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `svemirski_horizont` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `vecer_uz_jezero` | `special_full_custom` | visok | ne | ne | ne | 2 | 57 |
| `vecer_zaljubljenih` | `special_full_custom` | visok | ne | ne | ne | 2 | 57 |
| `vodopad_u_magli` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 43 |
| `zlatni_horizont` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |
| `zlatno_polje` | `common_layout_with_custom_bits` | srednji | da | da | ne | 0 | 46 |

## Kandidati za kasniji ručni refaktor

### `jedro_u_suton`

- Datoteka: `blog\templates\blog\designs\jedro_u_suton.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 606)
  - `direct_post_title`: 1 (linije: 611)
  - `direct_comments`: 24 (linije: 187, 196, 412, 419, 420, 430, 431, 436)
  - `direct_actions`: 1 (linije: 580)
  - `sidebar_markup`: 49 (linije: 188, 189, 198, 199, 222, 224, 278, 287)
  - `raw_forms_buttons`: 12 (linije: 256, 262, 268, 273, 397, 398, 405, 406)

Primjer:
```txt
0603: 
0604:         <div class="jus-layout">
0605:             <main class="jus-main">
0606:                 {% for post in page_obj %}
0607:                     <article class="jus-post">
0608:                         <div class="jus-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0609:                         <div class="jus-post-divider"></div>
```

### `magazin`

- Datoteka: `blog\templates\blog\designs\magazin.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 675)
  - `direct_post_title`: 1 (linije: 679)
  - `direct_comments`: 6 (linije: 601, 602, 604, 608, 708)
  - `direct_actions`: 1 (linije: 670)
  - `sidebar_markup`: 52 (linije: 88, 90, 91, 92, 95, 96, 99, 104)
  - `raw_forms_buttons`: 16 (linije: 22, 24, 43, 45, 50, 52, 58, 60)

Primjer:
```txt
0672:     </div>
0673: 
0674:     <div class="magazin-posts-wrap">
0675:         {% for post in page_obj %}
0676:             <article class="magazin-post-entry">
0677:                 <div class="d-flex justify-content-between align-items-start gap-3">
0678:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
```

### `misticno_jezero`

- Datoteka: `blog\templates\blog\designs\misticno_jezero.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 613)
  - `direct_post_title`: 1 (linije: 618)
  - `direct_comments`: 25 (linije: 422, 429, 430, 440, 441, 446, 447, 451)
  - `direct_actions`: 2 (linije: 418, 588)
  - `sidebar_markup`: 46 (linije: 244, 246, 255, 264, 265, 272, 278, 279)
  - `raw_forms_buttons`: 11 (linije: 222, 228, 234, 239, 401, 408, 430, 441)

Primjer:
```txt
0610:             </div>
0611:             {% endif %}
0612: 
0613:             {% for post in page_obj %}
0614:                 <article class="mj-post">
0615:                     <div class="mj-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0616:                     <div class="mj-post-divider"></div>
```

### `nebeska_klasika`

- Datoteka: `blog\templates\blog\designs\nebeska_klasika.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 574)
  - `direct_post_title`: 1 (linije: 579)
  - `direct_comments`: 23 (linije: 384, 391, 392, 402, 403, 408, 412, 418)
  - `direct_actions`: 1 (linije: 549)
  - `sidebar_markup`: 47 (linije: 221, 223, 232, 241, 242, 249, 255, 256)
  - `raw_forms_buttons`: 8 (linije: 211, 216, 371, 378, 392, 403, 599, 607)

Primjer:
```txt
0571:             </div>
0572:             {% endif %}
0573: 
0574:             {% for post in page_obj %}
0575:                 <article class="nk-post">
0576:                     <div class="nk-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0577:                     <div class="nk-post-divider"></div>
```

### `ponocna_elegancija`

- Datoteka: `blog\templates\blog\designs\ponocna_elegancija.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 601)
  - `direct_post_title`: 1 (linije: 606)
  - `direct_comments`: 25 (linije: 411, 418, 419, 429, 430, 435, 436, 440)
  - `direct_actions`: 1 (linije: 576)
  - `sidebar_markup`: 46 (linije: 242, 244, 253, 262, 263, 270, 276, 277)
  - `raw_forms_buttons`: 11 (linije: 220, 226, 232, 237, 398, 405, 419, 430)

Primjer:
```txt
0598:             </div>
0599:             {% endif %}
0600: 
0601:             {% for post in page_obj %}
0602:                 <article class="pe-post">
0603:                     <div class="pe-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0604:                     <div class="pe-post-divider"></div>
```

### `ruzicasti_vrt`

- Datoteka: `blog\templates\blog\designs\ruzicasti_vrt.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 603)
  - `direct_post_title`: 1 (linije: 608)
  - `direct_comments`: 25 (linije: 412, 419, 420, 430, 431, 436, 437, 441)
  - `direct_actions`: 1 (linije: 578)
  - `sidebar_markup`: 46 (linije: 242, 244, 253, 262, 263, 270, 276, 277)
  - `raw_forms_buttons`: 11 (linije: 221, 227, 232, 237, 399, 406, 420, 431)

Primjer:
```txt
0600:             </div>
0601:             {% endif %}
0602: 
0603:             {% for post in page_obj %}
0604:                 <article class="rv-post">
0605:                     <div class="rv-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0606:                     <div class="rv-post-divider"></div>
```

### `stara_aleja`

- Datoteka: `blog\templates\blog\designs\stara_aleja.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 611)
  - `direct_post_title`: 1 (linije: 616)
  - `direct_comments`: 24 (linije: 196, 203, 417, 424, 425, 435, 436, 441)
  - `direct_actions`: 1 (linije: 585)
  - `sidebar_markup`: 50 (linije: 197, 198, 205, 206, 227, 229, 283, 292)
  - `raw_forms_buttons`: 12 (linije: 261, 267, 273, 278, 402, 403, 410, 411)

Primjer:
```txt
0608: 
0609:         <div class="sa-layout">
0610:             <main class="sa-main">
0611:                 {% for post in page_obj %}
0612:                     <article class="sa-post">
0613:                         <div class="sa-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0614:                         <div class="sa-post-divider"></div>
```

### `staza_prema_vrhovima`

- Datoteka: `blog\templates\blog\designs\staza_prema_vrhovima.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 560)
  - `direct_post_title`: 1 (linije: 565)
  - `direct_comments`: 26 (linije: 160, 169, 376, 383, 384, 394, 395, 400)
  - `direct_actions`: 1 (linije: 537)
  - `sidebar_markup`: 48 (linije: 161, 162, 171, 172, 189, 191, 242, 251)
  - `raw_forms_buttons`: 11 (linije: 220, 226, 232, 237, 363, 370, 384, 395)

Primjer:
```txt
0557:             </div>
0558:             {% endif %}
0559: 
0560:             {% for post in page_obj %}
0561:                 <article class="spv-post">
0562:                     <div class="spv-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0563:                     <div class="spv-post-divider"></div>
```

### `studio`

- Datoteka: `blog\templates\blog\designs\studio.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 664)
  - `direct_post_title`: 1 (linije: 668)
  - `direct_comments`: 6 (linije: 582, 583, 585, 589, 697)
  - `direct_actions`: 1 (linije: 650)
  - `sidebar_markup`: 52 (linije: 91, 93, 94, 95, 98, 99, 102, 107)
  - `raw_forms_buttons`: 16 (linije: 27, 29, 48, 50, 55, 57, 63, 65)

Primjer:
```txt
0661:     </div>
0662: 
0663:     <div class="soho-posts-wrap">
0664:         {% for post in page_obj %}
0665:             <article class="soho-post-entry">
0666:                 <div class="d-flex justify-content-between align-items-start gap-3">
0667:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
```

### `vecer_uz_jezero`

- Datoteka: `blog\templates\blog\designs\vecer_uz_jezero.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: interaction_scripts
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 603)
  - `direct_post_title`: 1 (linije: 608)
  - `direct_comments`: 25 (linije: 412, 419, 420, 430, 431, 436, 437, 441)
  - `direct_actions`: 1 (linije: 578)
  - `sidebar_markup`: 46 (linije: 242, 244, 253, 262, 263, 270, 276, 277)
  - `raw_forms_buttons`: 11 (linije: 220, 226, 232, 237, 399, 406, 420, 431)

Primjer:
```txt
0600:             </div>
0601:             {% endif %}
0602: 
0603:             {% for post in page_obj %}
0604:                 <article class="vj-post">
0605:                     <div class="vj-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0606:                     <div class="vj-post-divider"></div>
```

### `vecer_zaljubljenih`

- Datoteka: `blog\templates\blog\designs\vecer_zaljubljenih.html`
- Grupa: `special_full_custom`
- Rizik: **visok**
- Common layout: ne
- Shared components: nema
- Direktni hitovi:
  - `direct_post_loop`: 2 (linije: 617)
  - `direct_post_title`: 1 (linije: 622)
  - `direct_comments`: 25 (linije: 426, 433, 434, 444, 445, 450, 451, 455)
  - `direct_actions`: 1 (linije: 592)
  - `sidebar_markup`: 46 (linije: 256, 258, 267, 276, 277, 284, 290, 291)
  - `raw_forms_buttons`: 11 (linije: 234, 240, 246, 251, 413, 420, 434, 445)

Primjer:
```txt
0614:             </div>
0615:             {% endif %}
0616: 
0617:             {% for post in page_obj %}
0618:                 <article class="vz-post">
0619:                     <div class="vz-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
0620:                     <div class="vz-post-divider"></div>
```

## Preporuka

1. Ne dirati sve posebne dizajne odjednom.
2. Sljedeći korak neka bude jedan probni posebni dizajn s najnižim rizikom.
3. Cilj probnog refaktora nije promijeniti izgled, nego zamijeniti kopirani prikaz postova/boxeva zajedničkim komponentama gdje je moguće.
4. Čišćenje starog CSS-a iz dizajnova ostaje kasnije, nakon što glavna struktura bude stabilna.

## Napomena

Ovaj audit samo čita stanje i generira dokumente. Ne radi izmjene u kodu.