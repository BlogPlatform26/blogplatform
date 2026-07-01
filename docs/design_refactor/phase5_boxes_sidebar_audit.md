# Phase 5 — audit boxeva i sidebara

Izrađeno: 2026-07-01 13:25:42

## Sažetak

- Ukupno dizajnova: **42**
- Koriste zajednički layout: **31**
- Imaju posebnu strukturu: **11**
- Rizik `nizak`: **31**
- Rizik `visok`: **11**

## Layout grupe

- `magazine`: 1
- `right_boxes`: 3
- `simple`: 4
- `single_right_sidebar`: 9
- `standard`: 24
- `studio`: 1

## Zajednički layout

| Dio | Stanje |
|---|---:|
| `blog_design_base.html` postoji | DA |
| uključuje lijevi sidebar | DA |
| uključuje desni sidebar | DA |
| uključuje postove | DA |

## Zajedničke sidebar komponente

| Komponenta | Postoji | Lijevi boxevi | Desni boxevi | Kalendar | Arhiva | Analitika | Profil akcije |
|---|---:|---:|---:|---:|---:|---:|---:|
| `blog_left_sidebar.html` | DA | 2 | 0 | DA | DA | DA | NE |
| `blog_right_sidebar.html` | DA | 2 | 2 | DA | DA | DA | DA |
| `blog_profile_actions_sidebar.html` | DA | 0 | 0 | NE | NE | NE | NE |
| `live_analytics_widget.html` | DA | 0 | 0 | NE | NE | NE | NE |

## Tablica dizajnova

| Dizajn | Extends | Layout | Lijevi boxevi | Desni boxevi | Sidebar klase | Opis | Rizik |
|---|---|---|---:|---:|---:|---|---|
| `asfaltni_plamen` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 9 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `carobna_ljubicasta` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 18 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `classic` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 0 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `classic_right` | `blog/layouts/blog_design_base.html` | `right_boxes` | 0 | 0 | 0 | preko zajedničkog layouta; boxevi se spajaju/desno prema right varijanti | nizak |
| `dark` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 0 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `dark_right` | `blog/layouts/blog_design_base.html` | `right_boxes` | 0 | 0 | 0 | preko zajedničkog layouta; boxevi se spajaju/desno prema right varijanti | nizak |
| `default` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 0 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `default_right` | `blog/layouts/blog_design_base.html` | `right_boxes` | 0 | 0 | 0 | preko zajedničkog layouta; boxevi se spajaju/desno prema right varijanti | nizak |
| `dimni_akordi` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 9 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `iznad_oblaka` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `jedro_u_suton` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `kraljevska_pozornica` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 13 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `litica_noci` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 0 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `magazin` | `blog/base.html` | `magazine` | 1 | 1 | 11 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `misticno_jezero` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `mjesecev_ples` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 9 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `morski_prijelaz` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `nebeska_klasika` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `nebeski_mir` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 14 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `nebesko_polje` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 15 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `neonski_grad` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `planine_u_magli` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 14 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `podvodna_tisina` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `polarna_svjetlost` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `polje_lavande` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 16 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `ponocna_elegancija` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `ruzicasti_vrt` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `simple` | `blog/layouts/blog_design_base.html` | `simple` | 0 | 0 | 0 | preko zajedničkog layouta; simple varijanta koristi prilagođeni sidebar prikaz | nizak |
| `simple_image` | `blog/layouts/blog_design_base.html` | `simple` | 0 | 0 | 0 | preko zajedničkog layouta; simple varijanta koristi prilagođeni sidebar prikaz | nizak |
| `simple_pattern` | `blog/layouts/blog_design_base.html` | `simple` | 0 | 0 | 0 | preko zajedničkog layouta; simple varijanta koristi prilagođeni sidebar prikaz | nizak |
| `simple_retro` | `blog/layouts/blog_design_base.html` | `simple` | 0 | 0 | 0 | preko zajedničkog layouta; simple varijanta koristi prilagođeni sidebar prikaz | nizak |
| `sjene_ulice` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 9 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `stara_aleja` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `staza_prema_vrhovima` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `studio` | `blog/base.html` | `studio` | 1 | 1 | 11 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `sumska_svjetlost` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `svemirski_horizont` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `vecer_uz_jezero` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `vecer_zaljubljenih` | `blog/base.html` | `single_right_sidebar` | 1 | 1 | 0 | posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar | visok |
| `vodopad_u_magli` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 13 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `zlatni_horizont` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |
| `zlatno_polje` | `blog/layouts/blog_design_base.html` | `standard` | 0 | 0 | 12 | preko zajedničkog layouta; lijevi sidebar + sadržaj + desni sidebar | nizak |

## Dizajni visokog rizika

- `jedro_u_suton` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `magazin` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `misticno_jezero` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `nebeska_klasika` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `ponocna_elegancija` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `ruzicasti_vrt` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `stara_aleja` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `staza_prema_vrhovima` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `studio` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `vecer_uz_jezero` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar
- `vecer_zaljubljenih` — posebni dizajn; sam prikazuje lijeve i desne boxeve, često spojene u jedan sidebar

## Dizajni koje treba ručno provjeriti

Nema dizajnova za ručnu provjeru.

## Snippet za posebne dizajnove

### `jedro_u_suton`

File: `blog\templates\blog\designs\jedro_u_suton.html`

```html
th={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                        {% empty %}
                            <div class="jus-empty-copy">Nema postova.</div>
                        {% endfor %}
                    </div>
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

                {% if blog_preferences.analytics_widget_side == 'left_bottom' or
```

### `magazin`

File: `blog\templates\blog\designs\magazin.html`

```html
a in archives %}
                    <a class="magazin-archive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                {% empty %}
                    <div class="magazin-empty-copy">Nema postova.</div>
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
        <section class="magazin-side
```

### `misticno_jezero`

File: `blog\templates\blog\designs\misticno_jezero.html`

```html
ive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="mj-empty-copy">Nema postova.</div>
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
```

### `nebeska_klasika`

File: `blog\templates\blog\designs\nebeska_klasika.html`

```html
ive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="nk-empty-copy">Nema postova.</div>
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
```

### `ponocna_elegancija`

File: `blog\templates\blog\designs\ponocna_elegancija.html`

```html
ive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="pe-empty-copy">Nema postova.</div>
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
```

### `ruzicasti_vrt`

File: `blog\templates\blog\designs\ruzicasti_vrt.html`

```html
ive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="rv-empty-copy">Nema postova.</div>
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
```

### `stara_aleja`

File: `blog\templates\blog\designs\stara_aleja.html`

```html
onth={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                        {% empty %}
                            <div class="sa-empty-copy">Nema postova.</div>
                        {% endfor %}
                    </div>
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

                {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_
```

### `staza_prema_vrhovima`

File: `blog\templates\blog\designs\staza_prema_vrhovima.html`

```html
e-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="spv-empty-copy">Nema postova.</div>
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
```

### `studio`

File: `blog\templates\blog\designs\studio.html`

```html
{% for a in archives %}
                    <a class="soho-archive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                {% empty %}
                    <div class="soho-empty-copy">Nema postova.</div>
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
            <div class="soho-s
```

### `vecer_uz_jezero`

File: `blog\templates\blog\designs\vecer_uz_jezero.html`

```html
ive-link" href="{{ archive_base_url }}?year={{ a.year }}&month={{ a.month }}">{{ a.label }} ({{ a.count }})</a>
                    {% empty %}
                        <div class="vj-empty-copy">Nema postova.</div>
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
```

### `vecer_zaljubljenih`

File: `blog\templates\blog\designs\vecer_zaljubljenih.html`

```html
blog_archive_mode == "list" %}
            <div class="vz-side-card">
                <div class="vz-archive-title">Arhiva bloga</div>
                <div class="vz-archive-list">
                    {% for a in archives %}
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

## Preporuka

1. Prvo ne dirati posebne dizajne s vlastitim sidebarom.
2. Prvo izdvojiti zajednički prikaz jednog boxa u komponentu, bez promjene rasporeda.
3. Zatim pojednostaviti `blog_left_sidebar.html` i `blog_right_sidebar.html`.
4. Tek nakon toga prebacivati posebne dizajne jedan po jedan.
5. Banner, pozadinske slike i upload slika ne dirati u ovoj fazi.