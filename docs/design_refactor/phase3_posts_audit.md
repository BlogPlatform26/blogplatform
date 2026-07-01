# Phase 3 — audit prikaza postova

Izrađeno: 2026-07-01 12:43:15

## Sažetak

- Ukupno dizajnova: **42**
- Rizik `nizak`: **20**
- Rizik `visok`: **11**
- Rizik `provjeriti`: **11**

## Zajedničke komponente

| Komponenta | Postoji | Petlje | Include | Markeri |
|---|---:|---|---|---|
| `blog_posts.html` | DA | post in page_obj | blog/components/post_meta.html, blog/components/post_body.html, blog/components/post_actions.html, blog/components/post_comments.html, blog/components/blog_interaction_scripts.html | blog-post, post-entry |
| `post_body.html` | DA | opt in post.quiz_options.all, opt in post.quiz_options.all, r in post.poll_results, opt in post.poll_options.all, img in post.images.all | - | poll, quiz |
| `post_meta.html` | DA | tag in post.tags.all | - | post-meta |
| `post_actions.html` | DA | - | - | post-actions, Komentari, Sviđa mi se, Otvori post |
| `post_comments.html` | DA | comment in comments, comment in post.comments.all | - | Komentari |
| `blog_interaction_scripts.html` | DA | - | - | poll |

## Tablica dizajnova

| Dizajn | Extends | Koristi blog_posts | Ima svoju petlju postova | Scripts include | Rizik |
|---|---|---:|---:|---:|---|
| `asfaltni_plamen` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `carobna_ljubicasta` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `classic` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `classic_right` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `dark` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `dark_right` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `default` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `default_right` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `dimni_akordi` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `iznad_oblaka` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `jedro_u_suton` | `blog/base.html` | NE | DA | DA | visok |
| `kraljevska_pozornica` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `litica_noci` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `magazin` | `blog/base.html` | NE | DA | DA | visok |
| `misticno_jezero` | `blog/base.html` | NE | DA | DA | visok |
| `mjesecev_ples` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `morski_prijelaz` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `nebeska_klasika` | `blog/base.html` | NE | DA | DA | visok |
| `nebeski_mir` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `nebesko_polje` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `neonski_grad` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `planine_u_magli` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `podvodna_tisina` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `polarna_svjetlost` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `polje_lavande` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `ponocna_elegancija` | `blog/base.html` | NE | DA | DA | visok |
| `ruzicasti_vrt` | `blog/base.html` | NE | DA | DA | visok |
| `simple` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `simple_image` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `simple_pattern` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `simple_retro` | `blog/layouts/blog_design_base.html` | NE | NE | NE | provjeriti |
| `sjene_ulice` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `stara_aleja` | `blog/base.html` | NE | DA | DA | visok |
| `staza_prema_vrhovima` | `blog/base.html` | NE | DA | DA | visok |
| `studio` | `blog/base.html` | NE | DA | DA | visok |
| `sumska_svjetlost` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `svemirski_horizont` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `vecer_uz_jezero` | `blog/base.html` | NE | DA | DA | visok |
| `vecer_zaljubljenih` | `blog/base.html` | NE | DA | NE | visok |
| `vodopad_u_magli` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `zlatni_horizont` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |
| `zlatno_polje` | `blog/layouts/blog_design_base.html` | DA | NE | NE | nizak |

## Dizajni s vlastitom petljom postova

### `jedro_u_suton`

File: `blog\templates\blog\designs\jedro_u_suton.html`

Markeri: `blog-post` (2), `post-title` (4), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
{% endif %}
            {% if active_tag %}
                <span class="jus-filter-chip">#{{ active_tag }}</span>
            {% endif %}
            <a class="jus-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
        </div>
        {% endif %}

        <div class="jus-layout">
            <main class="jus-main">
                {% for post in page_obj %}
                    <article class="jus-post">
                        <div class="jus-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                        <div class="jus-post-divider"></div>
                        <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                            <h4 class="mb-0">{{ post.title }}</h4>
                            {% include "blog/components/post_meta.html" %}
                        </div>

                        <div class="mt-4">
                            {% include "blog/components/post_body.html" %}
                        </div>

                        {% include "blog/components/post_actions.html" %}
                        {% include "blog/components/post_comments.html" %}
                    </article>
                {% empty %}
                    <article class="jus-post">
                        <p class="mb-0">Nema postova.</p>
                    </article>
                {% endfor %}

                {% if page_obj.has_other_pages %}
                <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                    {% if page_obj.has_previous %}
                        <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
```

### `magazin`

File: `blog\templates\blog\designs\magazin.html`

Markeri: `blog-post` (1), `post-entry` (10), `post-title` (3), `post-meta` (1)

Petlja 1: `post in page_obj`

```html
>
            {% endif %}
        </div>
        <div class="magazin-hero-overlay">
            <h1 class="magazin-blog-title">{{ blog.profile.blog_name }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}
        </div>
    </div>

    <div class="magazin-posts-wrap">
        {% for post in page_obj %}
            <article class="magazin-post-entry">
                <div class="d-flex justify-content-between align-items-start gap-3">
                    <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-style="{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }}" data-date-effect="{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}">
                        <div class="blog-date-main">
                            <div class="blog-date-day-wrap">
                                <div class="blog-date-day">{{ post.publication_datetime|date:"d" }}</div>
                            </div>
                            <div class="blog-date-text">
                                <div class="blog-date-month">{{ post.publication_datetime|month_hr|upper }}</div>
                                <div class=
```

### `misticno_jezero`

File: `blog\templates\blog\designs\misticno_jezero.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2), `poll` (1)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="mj-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="mj-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="mj-post">
                    <div class="mj-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="mj-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="mj-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

### `nebeska_klasika`

File: `blog\templates\blog\designs\nebeska_klasika.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="nk-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="nk-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="nk-post">
                    <div class="nk-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="nk-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="nk-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

### `ponocna_elegancija`

File: `blog\templates\blog\designs\ponocna_elegancija.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="pe-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="pe-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="pe-post">
                    <div class="pe-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="pe-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="pe-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

### `ruzicasti_vrt`

File: `blog\templates\blog\designs\ruzicasti_vrt.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="rv-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="rv-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="rv-post">
                    <div class="rv-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="rv-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="rv-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

### `stara_aleja`

File: `blog\templates\blog\designs\stara_aleja.html`

Markeri: `blog-post` (2), `post-title` (4), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
{% endif %}
            {% if active_tag %}
                <span class="sa-filter-chip">#{{ active_tag }}</span>
            {% endif %}
            <a class="sa-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
        </div>
        {% endif %}

        <div class="sa-layout">
            <main class="sa-main">
                {% for post in page_obj %}
                    <article class="sa-post">
                        <div class="sa-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                        <div class="sa-post-divider"></div>
                        <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                            <h4 class="mb-0">{{ post.title }}</h4>
                            {% include "blog/components/post_meta.html" %}
                        </div>

                        <div class="mt-4">
                            {% include "blog/components/post_body.html" %}
                        </div>

                        {% include "blog/components/post_actions.html" %}
                        {% include "blog/components/post_comments.html" %}
                    </article>
                {% empty %}
                    <article class="sa-post">
                        <p class="mb-0">Nema postova.</p>
                    </article>
                {% endfor %}

                {% if page_obj.has_other_pages %}
                <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                    {% if page_obj.has_previous %}
                        <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                    {% e
```

### `staza_prema_vrhovima`

File: `blog\templates\blog\designs\staza_prema_vrhovima.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="spv-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="spv-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="spv-post">
                    <div class="spv-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="spv-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="spv-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span clas
```

### `studio`

File: `blog\templates\blog\designs\studio.html`

Markeri: `blog-post` (1), `post-entry` (9), `post-title` (3), `post-meta` (1)

Petlja 1: `post in page_obj`

```html
" alt="Naslovna slika bloga">
            {% elif blog_preferences.active_design_customization.outer_background_asset %}
                <img src="{% static blog_preferences.active_design_customization.outer_background_asset %}" alt="Naslovna slika bloga">
            {% endif %}
        </div>
    </div>

    <div class="soho-posts-wrap">
        {% for post in page_obj %}
            <article class="soho-post-entry">
                <div class="d-flex justify-content-between align-items-start gap-3">
                    <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-style="{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }}" data-date-effect="{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}">
                        <div class="blog-date-main">
                            <div class="blog-date-day-wrap">
                                <div class="blog-date-day">{{ post.publication_datetime|date:"d" }}</div>
                            </div>
                            <div class="blog-date-text">
                                <div class="blog-date-month">{{ post.publication_datetime|month_hr|upper }}</div>
                                <div class="bl
```

### `vecer_uz_jezero`

File: `blog\templates\blog\designs\vecer_uz_jezero.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="vj-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="vj-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="vj-post">
                    <div class="vj-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="vj-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="vj-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

### `vecer_zaljubljenih`

File: `blog\templates\blog\designs\vecer_zaljubljenih.html`

Markeri: `blog-post` (1), `post-title` (3), `post-date` (2), `post-meta` (4), `post-actions` (2)

Petlja 1: `post in page_obj`

```html
er-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="vz-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="vz-filter-clear" href="{{ archive_base_url }}">Makni filter</a>
            </div>
            {% endif %}

            {% for post in page_obj %}
                <article class="vz-post">
                    <div class="vz-post-date">{{ post.publication_datetime|date:"d.m.Y" }}</div>
                    <div class="vz-post-divider"></div>
                    <div class="d-flex flex-column" style="gap: 10px; min-width: 0;">
                        <h4 class="mb-0">{{ post.title }}</h4>
                        {% include "blog/components/post_meta.html" %}
                    </div>

                    <div class="mt-4">
                        {% include "blog/components/post_body.html" %}
                    </div>

                    {% include "blog/components/post_actions.html" %}
                    {% include "blog/components/post_comments.html" %}
                </article>
            {% empty %}
                <div class="vz-post">
                    <p class="mb-0">Nema postova.</p>
                </div>
            {% endfor %}

            {% if page_obj.has_other_pages %}
            <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mt-3">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}{{ pagination_query }}" class="btn btn-sm btn-outline-secondary">Prethodna</a>
                {% else %}
                    <span></span>
                {% endif %}

                <span class="s
```

## Preporuka

1. Prvo srediti samo dizajnove s niskim rizikom i zajedničkim `blog_posts.html`.
2. Zatim napraviti jedan zajednički `post_card`/`post_list` sustav, ali bez promjene posebnih dizajnova.
3. Posebne dizajnove s vlastitom petljom prebacivati jedan po jedan.
4. Banner, slike i boxeve ne dirati u ovoj fazi.
