# Phase 22 — audit customization layera i hook klasa

Izrađeno: 2026-07-04 19:46:51

## Cilj

Provjeriti jesu li nove stabilne hook klase iz zajedničkih komponenti već povezane s centralnim customization layerom (`blog_design_styles.html`) i korisničkim CSS varijablama iz `base.html`. Ovo je read-only audit i ne mijenja aplikaciju.

## Sažetak

- Komponentne datoteke provjerene: **post_card, blog_box**
- Ukupno pronađenih class tokena u komponentama: **34**
- Hook-like klasa: **8**
- Hook-like klasa koje se već pojavljuju u `blog_design_styles.html`: **5**
- Hook-like klasa koje se još ne pojavljuju u `blog_design_styles.html`: **3**
- CSS varijabli korištenih u `blog_design_styles.html`: **23**
- `--blog-*` varijabli korištenih u `blog_design_styles.html`: **3**
- `--blog-*` varijabli korištenih u style layeru i definiranih u `base.html`: **3**

## Klase u komponentama

### `post_card`

| Klasa | Ponavljanja |
|---|---:|
| `align-items-start` | 1 |
| `blog-date-day` | 1 |
| `blog-date-day-wrap` | 1 |
| `blog-date-inline` | 1 |
| `blog-date-inline-day` | 1 |
| `blog-date-inline-month` | 1 |
| `blog-date-inline-sep` | 2 |
| `blog-date-inline-year` | 1 |
| `blog-date-main` | 1 |
| `blog-date-month` | 1 |
| `blog-date-shell` | 1 |
| `blog-date-text` | 1 |
| `blog-date-year` | 1 |
| `blog-post-card` ✅ hook | 1 |
| `blog-post-entry` ✅ hook | 1 |
| `blog-post-title` ✅ hook | 1 |
| `d-flex` | 2 |
| `flex-column` | 1 |
| `gap-3` | 1 |
| `justify-content-between` | 1 |
| `mb-0` | 1 |
| `mb-4` | 1 |
| `ms-3` | 1 |
| `mt-4` | 1 |
| `text-center` | 1 |

### `blog_box`

| Klasa | Ponavljanja |
|---|---:|
| `blog-box` ✅ hook | 1 |
| `blog-box-content` ✅ hook | 1 |
| `blog-box-title` ✅ hook | 1 |
| `endif` | 1 |
| `if` | 1 |
| `or` | 2 |
| `sidebar-box` | 1 |
| `sidebar-box-content` ✅ hook | 1 |
| `sidebar-box-title` ✅ hook | 1 |

## Hook-like klase i centralni style layer

### Već pokrivene u `blog_design_styles.html`

- `blog-box-title`
- `blog-post-entry`
- `blog-post-title`
- `sidebar-box-content`
- `sidebar-box-title`

### Još nisu direktno pokrivene u `blog_design_styles.html`

- `blog-box`
- `blog-box-content`
- `blog-post-card`

## `--blog-*` varijable koje koristi centralni style layer

| Varijabla | Definirana u `base.html` |
|---|---|
| `--blog-title-color` | da |
| `--blog-title-font` | da |
| `--blog-title-size` | da |

## Pravila koja već koriste `--blog-*` varijable

| Selector | Varijable |
|---|---|
| `.blog-page-title, .blog-page-title a` | `--blog-title-color`, `--blog-title-font`, `--blog-title-size` |
| `.blog-page-subtitle` | `--blog-title-color` |
| `.blog-page-title a, .blog-page-title` | `--blog-title-color` |
| `.blog-header-main--simple-retro .blog-page-title, .blog-header-main--simple-retro .blog-page-title a` | `--blog-title-color` |
| `.blog-page-title, .blog-page-title a` | `--blog-title-color` |
| `.blog-page-title, .blog-page-title a` | `--blog-title-color` |

## Preporuka

1. Ne dirati pojedinačne dizajne u ovoj fazi.
2. Sljedeći siguran korak je povezati hook klase iz `post_card.html` i `blog_box.html` s postojećim `--blog-*` varijablama u `blog_design_styles.html`.
3. Ako neka hook klasa nije direktno pokrivena, ne znači odmah da je bug; moguće je da je pokrivena preko starog selektora. Zato prvo raditi mali, centralni fix, pa testirati nekoliko dizajnova.
4. Čišćenje viška CSS-a iz dizajnova ostaje za kasnije, nakon glavnog sređivanja.

## Napomena

Ovaj audit samo čita stanje i generira dokumente. Ne mijenja kod aplikacije.