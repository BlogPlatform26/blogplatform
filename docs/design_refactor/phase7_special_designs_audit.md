# Phase 7 — audit posebnih dizajnova

Izrađeno: 2026-07-01 19:42:00

## Sažetak

- Pronađeno posebnih dizajnova: **11**
- Nedostaju iz poznatog popisa: **0**

## Tablica

| Dizajn | Layout | Post petlja | Lijevi boxevi | Desni boxevi | Banner | Pozadina/slika | Analitika | Arhiva | Kalendar |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `jedro_u_suton` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 31 |
| `magazin` | `magazine` | 1 | 1 | 1 | 0 | 23 | 7 | 4 | 28 |
| `misticno_jezero` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 30 |
| `nebeska_klasika` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 30 |
| `ponocna_elegancija` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 30 |
| `ruzicasti_vrt` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 30 |
| `stara_aleja` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 31 |
| `staza_prema_vrhovima` | `single_right_sidebar` | 1 | 1 | 1 | 1 | 0 | 6 | 5 | 31 |
| `studio` | `studio` | 1 | 1 | 1 | 3 | 20 | 7 | 4 | 28 |
| `vecer_uz_jezero` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 6 | 5 | 30 |
| `vecer_zaljubljenih` | `single_right_sidebar` | 1 | 1 | 1 | 2 | 0 | 0 | 5 | 30 |

## Što ovo znači

- Ovi dizajni imaju poseban HTML i ne treba ih prebacivati sve odjednom.
- Prvo treba izdvojiti male zajedničke dijelove koji ne mijenjaju izgled.
- Banner, pozadina/slika i sidebar se moraju provjeravati po dizajnu.
- Najsigurnije je prvo srediti jedan dizajn, testirati, pa tek onda drugi.

## Preporučeni redoslijed

1. `jedro_u_suton` — prvo jer već znamo da ima problem s bannerom.
2. `misticno_jezero`, `nebeska_klasika`, `ponocna_elegancija`, `ruzicasti_vrt`, `stara_aleja`, `staza_prema_vrhovima`, `vecer_uz_jezero` — slična single-right-sidebar grupa.
3. `magazin` i `studio` — kasnije jer imaju poseban magazin/studio prikaz i slike.

## `jedro_u_suton`

File: `blog\templates\blog\designs\jedro_u_suton.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`jus-archive-link`, `jus-archive-list`, `jus-archive-title`, `jus-box-content`, `jus-box-title`, `jus-calendar-day`, `jus-calendar-day--has-post`, `jus-calendar-empty`, `jus-calendar-grid`, `jus-calendar-month`, `jus-calendar-title`, `jus-calendar-weekdays`, `jus-empty-copy`, `jus-filter-bar`, `jus-filter-chip`, `jus-filter-clear`, `jus-layout`, `jus-main`, `jus-post`, `jus-post-date`, `jus-post-divider`, `jus-profile-wrap`, `jus-section`, `jus-shell`, `jus-side-stack`

### Banner snippet

```html
font-size: 1.12rem;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="jus-theme">
    <h1 class="jus-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="sa-banner" style="margin-top: 6px; background: rgba(58, 34, 24, 0.12); border: 1px solid rgba(255, 232, 208, 0.10); padding: 8px; box-shadow: 0 12px 28px rgba(17, 10, 8, 0.12); backdrop-filter: blur(5px);">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga" style="width: 100%; max-height: 220px; object-fit: cover; display: block;">
    </div>
    {% endif %}

    <div class="jus-shell">
        {% if active_category or active_tag %}
        <div class="jus-filter-bar">
            <span>Filtrirano:</span>
            {% if active_category_name %}
                <span class="jus-filter-chip">{{ active_category_name }}</span>
            {% elif activ
```

### Box/sidebar snippet

```html
</section>
                {% endif %}

                {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
                <section class="jus-section">
                    {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
                </section>
                {% endif %}

                {% for box in left_boxes %}
                <section class="jus-section">
                    <div class="jus-box-title">{{ box.title }}</div>
                    <div class="jus-box-content">{{ box.content|safe }}</div>
                </section>
                {% endfor %}

                {% for box in right_boxes %}
                <section class="jus-section">
                    <div class="jus-box-title">{{ box.title }}</div>
                    <div class="jus-box-content">{{ box.content|safe }}</div>
                </section>
                {% endfor %}

                {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
```

### Post loop snippet

```html
<span class="jus-filter-chip">{{ active_category }}</span>
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
```

## `magazin`

File: `blog\templates\blog\designs\magazin.html`

Extends: `blog/base.html`

Layout procjena: `magazine`

Klase uzorka:

`magazin-archive-link`, `magazin-archive-list`, `magazin-avatar`, `magazin-blog-title`, `magazin-calendar-day`, `magazin-calendar-day--has-post`, `magazin-calendar-empty`, `magazin-calendar-grid`, `magazin-calendar-title`, `magazin-calendar-weekdays`, `magazin-empty-copy`, `magazin-hero`, `magazin-hero-media`, `magazin-hero-overlay`, `magazin-main-shell`, `magazin-post-entry`, `magazin-posts-wrap`, `magazin-profile-actions`, `magazin-profile-author-link`, `magazin-profile-block`, `magazin-profile-dropdown`, `magazin-profile-dropdown-menu`, `magazin-profile-dropdown-toggle`, `magazin-profile-meta`, `magazin-profile-name`

### Box/sidebar snippet

```html
ss="magazin-empty-copy">Nema postova.</div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if blog_preferences.analytics_widget_side == 'left_top' %}
        <section class="magazin-sidebar-section">
            {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
        </section>
        {% endif %}

        {% for box in left_boxes %}
        <section class="magazin-sidebar-section magazin-sidebar-section--box">
            <div class="magazin-section-title">{{ box.title }}</div>
            <div class="magazin-sidebar-box-content">{{ box.content|safe }}</div>
        </section>
        {% endfor %}

        {% if blog_preferences.analytics_widget_side == 'right_top' %}
        <section class="magazin-sidebar-section">
            {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
        </section>
        {% endif %}

        {% for box in right_boxes %}
        <section class="magazin-sidebar-section magazin-sidebar-section--box">
            <div class="magazin
```

### Post loop snippet

```html
gn_customization.outer_background_asset %}" alt="Naslovna slika bloga">
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

                    <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-s
```

## `misticno_jezero`

File: `blog\templates\blog\designs\misticno_jezero.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`mj-archive-link`, `mj-archive-list`, `mj-archive-title`, `mj-banner`, `mj-box-content`, `mj-box-title`, `mj-calendar-day`, `mj-calendar-day--has-post`, `mj-calendar-empty`, `mj-calendar-grid`, `mj-calendar-month`, `mj-calendar-title`, `mj-calendar-weekdays`, `mj-empty-copy`, `mj-filter-bar`, `mj-filter-chip`, `mj-filter-clear`, `mj-layout`, `mj-post`, `mj-post-date`, `mj-post-divider`, `mj-profile-wrap`, `mj-side-card`, `mj-side-stack`, `mj-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="mj-theme">
    <h1 class="mj-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="mj-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="mj-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="mj-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="mj-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="mj-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="mj-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="mj-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="mj-side-card">
                <div class="mj-box-title">{{ box.title }}</div>
                <div class="mj-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="mj-side-card">
                <div class="mj-box-title">{{ box.title }}</div>
                <div class="mj-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="mj-side-card">
                {% include "blog/compone
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="mj-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```

## `nebeska_klasika`

File: `blog\templates\blog\designs\nebeska_klasika.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`nk-archive-link`, `nk-archive-list`, `nk-archive-title`, `nk-banner`, `nk-box-content`, `nk-box-title`, `nk-calendar-day`, `nk-calendar-day--has-post`, `nk-calendar-empty`, `nk-calendar-grid`, `nk-calendar-month`, `nk-calendar-title`, `nk-calendar-weekdays`, `nk-empty-copy`, `nk-filter-bar`, `nk-filter-chip`, `nk-filter-clear`, `nk-layout`, `nk-post`, `nk-post-date`, `nk-post-divider`, `nk-profile-wrap`, `nk-side-card`, `nk-side-stack`, `nk-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="nk-theme">
    <h1 class="nk-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="nk-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="nk-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="nk-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="nk-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="nk-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="nk-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="nk-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="nk-side-card">
                <div class="nk-box-title">{{ box.title }}</div>
                <div class="nk-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="nk-side-card">
                <div class="nk-box-title">{{ box.title }}</div>
                <div class="nk-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="nk-side-card">
                {% include "blog/compone
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="nk-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```

## `ponocna_elegancija`

File: `blog\templates\blog\designs\ponocna_elegancija.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`pe-archive-link`, `pe-archive-list`, `pe-archive-title`, `pe-banner`, `pe-box-content`, `pe-box-title`, `pe-calendar-day`, `pe-calendar-day--has-post`, `pe-calendar-empty`, `pe-calendar-grid`, `pe-calendar-month`, `pe-calendar-title`, `pe-calendar-weekdays`, `pe-empty-copy`, `pe-filter-bar`, `pe-filter-chip`, `pe-filter-clear`, `pe-layout`, `pe-post`, `pe-post-date`, `pe-post-divider`, `pe-profile-wrap`, `pe-side-card`, `pe-side-stack`, `pe-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="pe-theme">
    <h1 class="pe-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="pe-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="pe-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="pe-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="pe-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="pe-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="pe-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="pe-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="pe-side-card">
                <div class="pe-box-title">{{ box.title }}</div>
                <div class="pe-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="pe-side-card">
                <div class="pe-box-title">{{ box.title }}</div>
                <div class="pe-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="pe-side-card">
                {% include "blog/compone
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="pe-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```

## `ruzicasti_vrt`

File: `blog\templates\blog\designs\ruzicasti_vrt.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`rv-archive-link`, `rv-archive-list`, `rv-archive-title`, `rv-banner`, `rv-box-content`, `rv-box-title`, `rv-calendar-day`, `rv-calendar-day--has-post`, `rv-calendar-empty`, `rv-calendar-grid`, `rv-calendar-month`, `rv-calendar-title`, `rv-calendar-weekdays`, `rv-empty-copy`, `rv-filter-bar`, `rv-filter-chip`, `rv-filter-clear`, `rv-layout`, `rv-post`, `rv-post-date`, `rv-post-divider`, `rv-profile-wrap`, `rv-side-card`, `rv-side-stack`, `rv-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="rv-theme">
    <h1 class="rv-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="rv-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="rv-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="rv-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="rv-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="rv-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="rv-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="rv-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="rv-side-card">
                <div class="rv-box-title">{{ box.title }}</div>
                <div class="rv-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="rv-side-card">
                <div class="rv-box-title">{{ box.title }}</div>
                <div class="rv-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="rv-side-card">
                {% include "blog/compone
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="rv-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```

## `stara_aleja`

File: `blog\templates\blog\designs\stara_aleja.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`sa-archive-link`, `sa-archive-list`, `sa-archive-title`, `sa-banner`, `sa-box-content`, `sa-box-title`, `sa-calendar-day`, `sa-calendar-day--has-post`, `sa-calendar-empty`, `sa-calendar-grid`, `sa-calendar-month`, `sa-calendar-title`, `sa-calendar-weekdays`, `sa-empty-copy`, `sa-filter-bar`, `sa-filter-chip`, `sa-filter-clear`, `sa-layout`, `sa-main`, `sa-post`, `sa-post-date`, `sa-post-divider`, `sa-profile-wrap`, `sa-section`, `sa-shell`

### Banner snippet

```html
{
        font-size: 1.55rem;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="sa-theme">
    <h1 class="sa-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="sa-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="sa-shell">
        {% if active_category or active_tag %}
        <div class="sa-filter-bar">
            <span>Filtrirano:</span>
            {% if active_category_name %}
                <span class="sa-filter-chip">{{ active_category_name }}</span>
            {% elif active_category %}
                <span class="sa-filter-chip">{{ active_category }}</span>
            {% endif %}
            {% if active_tag %}
                <span class="sa-filter-chip">#{{ active_tag }}</span>
            {% endif %}
            <a class="sa-filter-cle
```

### Box/sidebar snippet

```html
>
                </section>
                {% endif %}

                {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
                <section class="sa-section">
                    {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
                </section>
                {% endif %}

                {% for box in left_boxes %}
                <section class="sa-section">
                    <div class="sa-box-title">{{ box.title }}</div>
                    <div class="sa-box-content">{{ box.content|safe }}</div>
                </section>
                {% endfor %}

                {% for box in right_boxes %}
                <section class="sa-section">
                    <div class="sa-box-title">{{ box.title }}</div>
                    <div class="sa-box-content">{{ box.content|safe }}</div>
                </section>
                {% endfor %}

                {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
                <se
```

### Post loop snippet

```html
<span class="sa-filter-chip">{{ active_category }}</span>
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
```

## `staza_prema_vrhovima`

File: `blog\templates\blog\designs\staza_prema_vrhovima.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`spv-archive-link`, `spv-archive-list`, `spv-archive-title`, `spv-banner`, `spv-box-content`, `spv-box-title`, `spv-calendar-day`, `spv-calendar-day--has-post`, `spv-calendar-empty`, `spv-calendar-grid`, `spv-calendar-month`, `spv-calendar-title`, `spv-calendar-weekdays`, `spv-empty-copy`, `spv-filter-bar`, `spv-filter-chip`, `spv-filter-clear`, `spv-layout`, `spv-post`, `spv-post-date`, `spv-post-divider`, `spv-profile-wrap`, `spv-side-card`, `spv-side-stack`, `spv-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="spv-theme">
    <h1 class="spv-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="spv-banner" style="display:none;"></div>
    {% endif %}

    <div class="spv-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="spv-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="spv-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="spv-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="spv-filter-chip">#{{ active_tag }}</span>
                {% endif %}
                <a class="
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="spv-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="spv-side-card">
                <div class="spv-box-title">{{ box.title }}</div>
                <div class="spv-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="spv-side-card">
                <div class="spv-box-title">{{ box.title }}</div>
                <div class="spv-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="spv-side-card">
                {% include "blog/
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="spv-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/componen
```

## `studio`

File: `blog\templates\blog\designs\studio.html`

Extends: `blog/base.html`

Layout procjena: `studio`

Klase uzorka:

`soho-archive-link`, `soho-archive-list`, `soho-avatar`, `soho-blog-title`, `soho-calendar-day`, `soho-calendar-day--has-post`, `soho-calendar-empty`, `soho-calendar-grid`, `soho-calendar-title`, `soho-calendar-weekdays`, `soho-empty-copy`, `soho-hero`, `soho-hero-media`, `soho-main-shell`, `soho-post-entry`, `soho-posts-wrap`, `soho-profile-actions`, `soho-profile-author-link`, `soho-profile-block`, `soho-profile-dropdown`, `soho-profile-dropdown-menu`, `soho-profile-dropdown-toggle`, `soho-profile-meta`, `soho-profile-name`, `soho-profile-note`

### Banner snippet

```html
{% extends "blog/base.html" %}
{% load static custom_tags %}

{% block blog_header %}{% endblock %}

{% block left_sidebar %}
<div class="soho-sidebar">
    {% if blog.profile.blog_banner %}
    <div class="soho-sidebar-banner soho-sidebar-banner--{{ blog.profile.blog_banner_position|default:'center' }}">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="soho-sidebar-inner">
        <div class="soho-profile-block">
            {% if blog.profile.avatar %}
                <img src="{{ blog.profile.avatar.url }}" alt="{{ blog.username }}" class="soho-avatar">
            {% else %}
                <img src="{% static 'images/default-avatar.jpg' %}" alt="{{ blog.username }}" class="soho-avatar">
            {% endif %}
            <div class="soho-profile-top-row">
                <div class="soho-profile-name"
```

### Box/sidebar snippet

```html
iv class="soho-empty-copy">Nema postova.</div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        {% if blog_preferences.analytics_widget_side == 'left_top' %}
        <section class="soho-sidebar-section">
            {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
        </section>
        {% endif %}

        {% for box in left_boxes %}
        <section class="soho-sidebar-section">
            <div class="soho-section-title">{{ box.title }}</div>
            <div class="soho-sidebar-box-content">{{ box.content|safe }}</div>
        </section>
        {% endfor %}

        {% if blog_preferences.analytics_widget_side == 'right_top' %}
        <section class="soho-sidebar-section">
            {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
        </section>
        {% endif %}

        {% for box in right_boxes %}
        <section class="soho-sidebar-section">
            <div class="soho-section-title">{{ box.title }}</div>
            <div class="soho-sidebar-b
```

### Post loop snippet

```html
<img src="{{ blog.profile.simple_background_image.url }}" alt="Naslovna slika bloga">
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

                    <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-styl
```

## `vecer_uz_jezero`

File: `blog\templates\blog\designs\vecer_uz_jezero.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`vj-archive-link`, `vj-archive-list`, `vj-archive-title`, `vj-banner`, `vj-box-content`, `vj-box-title`, `vj-calendar-day`, `vj-calendar-day--has-post`, `vj-calendar-empty`, `vj-calendar-grid`, `vj-calendar-month`, `vj-calendar-title`, `vj-calendar-weekdays`, `vj-empty-copy`, `vj-filter-bar`, `vj-filter-chip`, `vj-filter-clear`, `vj-layout`, `vj-post`, `vj-post-date`, `vj-post-divider`, `vj-profile-wrap`, `vj-side-card`, `vj-side-stack`, `vj-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="vj-theme">
    <h1 class="vj-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="vj-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="vj-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="vj-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="vj-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="vj-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="vj-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
{% endfor %}
                </div>
            </div>
            {% endif %}

            {% if blog_preferences.analytics_widget_side == 'left_top' or blog_preferences.analytics_widget_side == 'right_top' %}
            <div class="vj-side-card">
                {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="" %}
            </div>
            {% endif %}

            {% for box in left_boxes %}
            <div class="vj-side-card">
                <div class="vj-box-title">{{ box.title }}</div>
                <div class="vj-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% for box in right_boxes %}
            <div class="vj-side-card">
                <div class="vj-box-title">{{ box.title }}</div>
                <div class="vj-box-content">{{ box.content|safe }}</div>
            </div>
            {% endfor %}

            {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
            <div class="vj-side-card">
                {% include "blog/compone
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="vj-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```

## `vecer_zaljubljenih`

File: `blog\templates\blog\designs\vecer_zaljubljenih.html`

Extends: `blog/base.html`

Layout procjena: `single_right_sidebar`

Klase uzorka:

`vz-archive-link`, `vz-archive-list`, `vz-archive-title`, `vz-banner`, `vz-box-content`, `vz-box-title`, `vz-calendar-day`, `vz-calendar-day--has-post`, `vz-calendar-empty`, `vz-calendar-grid`, `vz-calendar-month`, `vz-calendar-title`, `vz-calendar-weekdays`, `vz-empty-copy`, `vz-filter-bar`, `vz-filter-chip`, `vz-filter-clear`, `vz-layout`, `vz-post`, `vz-post-date`, `vz-post-divider`, `vz-profile-wrap`, `vz-side-card`, `vz-side-stack`, `vz-side-title`

### Banner snippet

```html
padding: 18px 16px 16px;
    }

    .comment-row {
        flex-direction: column;
        align-items: stretch;
    }

    .comment-row .btn {
        width: 100%;
    }
}
</style>

<div class="vz-theme">
    <h1 class="vz-title">{{ blog.profile.blog_name|default:blog.username }}</h1>

    {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}

    {% if blog.profile.blog_banner %}
    <div class="vz-banner">
        <img src="{{ blog.profile.blog_banner.url }}" alt="Banner bloga">
    </div>
    {% endif %}

    <div class="vz-layout">
        <main>
            {% if active_category or active_tag %}
            <div class="vz-filter-bar">
                <span>Filtrirano:</span>
                {% if active_category_name %}
                    <span class="vz-filter-chip">{{ active_category_name }}</span>
                {% elif active_category %}
                    <span class="vz-filter-chip">{{ active_category }}</span>
                {% endif %}
                {% if active_tag %}
                    <span class="vz-filter-chip">#{{ active_tag }}</span>
```

### Box/sidebar snippet

```html
<a class="vz-archive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">
                            {{ a.label }} ({{ a.count }})
                        </a>
                    {% empty %}
                        <div class="vz-empty-copy">Nema postova.</div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% for box in left_boxes %}
                <div class="vz-side-card">
                    <div class="vz-box-title">{{ box.title }}</div>
                    <div class="vz-box-content">{{ box.content|safe }}</div>
                </div>
            {% endfor %}

            {% for box in right_boxes %}
                <div class="vz-side-card">
                    <div class="vz-box-title">{{ box.title }}</div>
                    <div class="vz-box-content">{{ box.content|safe }}</div>
                </div>
            {% endfor %}
        </aside>
    </div>
</div>
{% endblock %}
```

### Post loop snippet

```html
{% elif active_category %}
                    <span class="vz-filter-chip">{{ active_category }}</span>
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
                    {% include "blog/components/
```
