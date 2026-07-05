# Phase 24 — deep audit dizajna `magazin`

Izrađeno: 2026-07-05 11:59:48

## Cilj

Dubinski provjeriti `magazin.html` prije bilo kakvog refaktora. Ovaj audit samo čita stanje i generira dokumente. Ne mijenja kod aplikacije.

## Sažetak

- Datoteka: `C:\Users\mario\blogplatform\blog\templates\blog\designs\magazin.html`
- Broj linija: **729**
- CSS `<style>` blokova: **1**
- CSS selektora približno: **88**
- Includeova komponenti: **8**

## Postojeće zajedničke komponente u projektu

| Komponenta | Postoji |
|---|---|
| `post_card` | da |
| `blog_posts` | da |
| `blog_box` | da |
| `blog_left_sidebar` | da |
| `blog_right_sidebar` | da |
| `post_actions` | da |
| `post_comments` | da |
| `blog_interaction_scripts` | da |

## Includeovi u `magazin.html`

| Linija | Include |
|---:|---|
| 134 | `blog/components/live_analytics_widget.html` |
| 147 | `blog/components/live_analytics_widget.html` |
| 160 | `blog/components/live_analytics_widget.html` |
| 680 | `blog/components/post_meta.html` |
| 704 | `blog/components/post_body.html` |
| 707 | `blog/components/post_actions.html` |
| 708 | `blog/components/post_comments.html` |
| 728 | `blog/components/blog_interaction_scripts.html` |

## Hitovi po kategorijama

| Kategorija | Broj |
|---|---:|
| `page_obj_loop` | 1 |
| `article_post_entry` | 1 |
| `post_title` | 4 |
| `post_content` | 2 |
| `comments` | 5 |
| `actions` | 2 |
| `sidebar` | 157 |
| `forms_buttons` | 16 |
| `shared_includes` | 8 |

## CSS tokeni koji su bitni za refaktor

| Token | Ponavljanja |
|---|---:|
| `nav.navbar` | 2 |
| `.magazin-post-entry` | 9 |
| `.magazin-post-title` | 0 |
| `.magazin-posts-wrap` | 2 |
| `.magazin-sidebar` | 22 |
| `.sidebar-box` | 5 |
| `.form-control` | 2 |
| `textarea.form-control` | 2 |
| `input.form-control` | 0 |
| `.btn-outline-light` | 0 |
| `.blog-action-outline` | 0 |
| `.dropdown-menu` | 1 |
| `.comment-row` | 0 |

## Najvažniji pronađeni dijelovi

### `page_obj_loop`

Linija 675:
```txt
0672:     </div>
0673: 
0674:     <div class="magazin-posts-wrap">
0675:         {% for post in page_obj %}
0676:             <article class="magazin-post-entry">
0677:                 <div class="d-flex justify-content-between align-items-start gap-3">
0678:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
0679:                         <h4 class="mb-0">{{ post.title }}</h4>
0680:                         {% include "blog/components/post_meta.html" %}
0681:                     </div>
```

### `article_post_entry`

Linija 676:
```txt
0673: 
0674:     <div class="magazin-posts-wrap">
0675:         {% for post in page_obj %}
0676:             <article class="magazin-post-entry">
0677:                 <div class="d-flex justify-content-between align-items-start gap-3">
0678:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
0679:                         <h4 class="mb-0">{{ post.title }}</h4>
0680:                         {% include "blog/components/post_meta.html" %}
0681:                     </div>
0682: 
```

### `post_title`

Linija 179:
```txt
0176:     --magazin-section-bg: {{ blog_preferences.active_design_customization.box_background_color|default:'#f8f3ed' }};
0177:     --magazin-section-border: {{ blog_preferences.active_design_customization.box_border_color|default:'#e6dbcf' }};
0178:     --magazin-title-color: {{ blog_preferences.active_design_customization.blog_title_color|default:'#ffffff' }};
0179:     --magazin-post-title: {{ blog_preferences.active_design_customization.post_title_color|default:'#4f4136' }};
0180:     --magazin-box-title: {{ blog_preferences.active_design_customization.box_title_color|default:'#54463b' }};
0181:     --magazin-text: {{ blog_preferences.active_design_customization.body_text_color|default:'#5e5043' }};
0182:     --magazin-date: {{ blog_preferences.active_design_customization.post_date_color|default:'#9b7b5a' }};
0183:     --magazin-title-font: {{ blog_preferences.active_design_customization.blog_title_font_stack|default:'Georgia, Times New Roman, serif' }};
0184:     --magazin-post-font: {{ blog_preferences.active_design_customization.post_title_font_stack|default:'Georgia, Times New Roman, serif' }};
0185:     --magazin-box-font: {{ blog_preferences.active_design_customization.box_title_font_stack|default:'Garamond, Georgia, serif' }};
```
Linija 580:
```txt
0577: 
0578: .magazin-post-entry h4,
0579: .magazin-post-entry h4 a,
0580: .blog-post-title {
0581:     color: var(--magazin-post-title) !important;
0582:     font-family: var(--magazin-post-font) !important;
0583: }
0584: 
0585: .magazin-post-entry hr {
0586:     border-color: rgba(86, 72, 58, 0.12);
```
Linija 581:
```txt
0578: .magazin-post-entry h4,
0579: .magazin-post-entry h4 a,
0580: .blog-post-title {
0581:     color: var(--magazin-post-title) !important;
0582:     font-family: var(--magazin-post-font) !important;
0583: }
0584: 
0585: .magazin-post-entry hr {
0586:     border-color: rgba(86, 72, 58, 0.12);
0587: }
```
Linija 679:
```txt
0676:             <article class="magazin-post-entry">
0677:                 <div class="d-flex justify-content-between align-items-start gap-3">
0678:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
0679:                         <h4 class="mb-0">{{ post.title }}</h4>
0680:                         {% include "blog/components/post_meta.html" %}
0681:                     </div>
0682: 
0683:                     <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-style="{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }}" data-date-effect="{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}">
0684:                         <div class="blog-date-main">
0685:                             <div class="blog-date-day-wrap">
```

### `comments`

Linija 601:
```txt
0598: 
0599: .post-meta,
0600: .post-author-line,
0601: .comment-text,
0602: .comment-time,
0603: .sidebar-box-content,
0604: .comment-body {
0605:     color: var(--magazin-text);
0606: }
0607: 
```
Linija 602:
```txt
0599: .post-meta,
0600: .post-author-line,
0601: .comment-text,
0602: .comment-time,
0603: .sidebar-box-content,
0604: .comment-body {
0605:     color: var(--magazin-text);
0606: }
0607: 
0608: .comment-body {
```
Linija 604:
```txt
0601: .comment-text,
0602: .comment-time,
0603: .sidebar-box-content,
0604: .comment-body {
0605:     color: var(--magazin-text);
0606: }
0607: 
0608: .comment-body {
0609:     background: #fff;
0610:     border: 1px solid var(--magazin-content-border);
```
Linija 608:
```txt
0605:     color: var(--magazin-text);
0606: }
0607: 
0608: .comment-body {
0609:     background: #fff;
0610:     border: 1px solid var(--magazin-content-border);
0611: }
0612: 
0613: textarea.form-control {
0614:     background: #fff !important;
```
Linija 708:
```txt
0705:                 </div>
0706: 
0707:                 {% include "blog/components/post_actions.html" %}
0708:                 {% include "blog/components/post_comments.html" %}
0709:                 <hr>
0710:             </article>
0711:         {% empty %}
0712:             <p class="m-4">Nema postova.</p>
0713:         {% endfor %}
0714: 
```

### `actions`

Linija 670:
```txt
0667:         <div class="magazin-hero-overlay">
0668:             <h1 class="magazin-blog-title">{{ blog.profile.blog_name }}</h1>
0669: 
0670:     {% if blog.profile.blog_tagline %}<p class="blog-tagline-shared">{{ blog.profile.blog_tagline }}</p>{% endif %}
0671:         </div>
0672:     </div>
0673: 
0674:     <div class="magazin-posts-wrap">
0675:         {% for post in page_obj %}
0676:             <article class="magazin-post-entry">
```
Linija 707:
```txt
0704:                     {% include "blog/components/post_body.html" %}
0705:                 </div>
0706: 
0707:                 {% include "blog/components/post_actions.html" %}
0708:                 {% include "blog/components/post_comments.html" %}
0709:                 <hr>
0710:             </article>
0711:         {% empty %}
0712:             <p class="m-4">Nema postova.</p>
0713:         {% endfor %}
```

### `sidebar`

Linija 6:
```txt
0003: 
0004: {% block blog_header %}{% endblock %}
0005: 
0006: {% block left_sidebar %}
0007: <div class="magazin-sidebar">
0008:     <div class="magazin-sidebar-inner">
0009:         <div class="magazin-profile-block">
0010:             {% if blog.profile.avatar %}
0011:                 <img src="{{ blog.profile.avatar.url }}" alt="{{ blog.username }}" class="magazin-avatar">
0012:             {% else %}
```
Linija 7:
```txt
0004: {% block blog_header %}{% endblock %}
0005: 
0006: {% block left_sidebar %}
0007: <div class="magazin-sidebar">
0008:     <div class="magazin-sidebar-inner">
0009:         <div class="magazin-profile-block">
0010:             {% if blog.profile.avatar %}
0011:                 <img src="{{ blog.profile.avatar.url }}" alt="{{ blog.username }}" class="magazin-avatar">
0012:             {% else %}
0013:                 <img src="{% static 'images/default-avatar.jpg' %}" alt="{{ blog.username }}" class="magazin-avatar">
```
Linija 8:
```txt
0005: 
0006: {% block left_sidebar %}
0007: <div class="magazin-sidebar">
0008:     <div class="magazin-sidebar-inner">
0009:         <div class="magazin-profile-block">
0010:             {% if blog.profile.avatar %}
0011:                 <img src="{{ blog.profile.avatar.url }}" alt="{{ blog.username }}" class="magazin-avatar">
0012:             {% else %}
0013:                 <img src="{% static 'images/default-avatar.jpg' %}" alt="{{ blog.username }}" class="magazin-avatar">
0014:             {% endif %}
```
Linija 88:
```txt
0085:             {% endif %}
0086:         </div>
0087: 
0088:         {% if blog_preferences.blog_archive_mode == "both" or blog_preferences.blog_archive_mode == "calendar" %}
0089:         <section class="magazin-sidebar-section">
0090:             <div class="magazin-section-title">Kalendar</div>
0091:             <div class="magazin-calendar-title calendar-month-nav"><a href="{{ prev_month_url }}" class="calendar-month-nav-link" aria-label="Prethodni mjesec">&#8249;</a><span>{{ current_month_hr|upper }}, {{ current_year }}</span><a href="{{ next_month_url }}" class="calendar-month-nav-link" aria-label="Sljedeći mjesec">&#8250;</a></div>
0092:             <div class="magazin-calendar-weekdays">
0093:                 <div>P</div><div>U</div><div>S</div><div>Č</div><div>P</div><div>S</div><div>N</div>
0094:             </div>
```
Linija 88:
```txt
0085:             {% endif %}
0086:         </div>
0087: 
0088:         {% if blog_preferences.blog_archive_mode == "both" or blog_preferences.blog_archive_mode == "calendar" %}
0089:         <section class="magazin-sidebar-section">
0090:             <div class="magazin-section-title">Kalendar</div>
0091:             <div class="magazin-calendar-title calendar-month-nav"><a href="{{ prev_month_url }}" class="calendar-month-nav-link" aria-label="Prethodni mjesec">&#8249;</a><span>{{ current_month_hr|upper }}, {{ current_year }}</span><a href="{{ next_month_url }}" class="calendar-month-nav-link" aria-label="Sljedeći mjesec">&#8250;</a></div>
0092:             <div class="magazin-calendar-weekdays">
0093:                 <div>P</div><div>U</div><div>S</div><div>Č</div><div>P</div><div>S</div><div>N</div>
0094:             </div>
```
Linija 88:
```txt
0085:             {% endif %}
0086:         </div>
0087: 
0088:         {% if blog_preferences.blog_archive_mode == "both" or blog_preferences.blog_archive_mode == "calendar" %}
0089:         <section class="magazin-sidebar-section">
0090:             <div class="magazin-section-title">Kalendar</div>
0091:             <div class="magazin-calendar-title calendar-month-nav"><a href="{{ prev_month_url }}" class="calendar-month-nav-link" aria-label="Prethodni mjesec">&#8249;</a><span>{{ current_month_hr|upper }}, {{ current_year }}</span><a href="{{ next_month_url }}" class="calendar-month-nav-link" aria-label="Sljedeći mjesec">&#8250;</a></div>
0092:             <div class="magazin-calendar-weekdays">
0093:                 <div>P</div><div>U</div><div>S</div><div>Č</div><div>P</div><div>S</div><div>N</div>
0094:             </div>
```
Linija 89:
```txt
0086:         </div>
0087: 
0088:         {% if blog_preferences.blog_archive_mode == "both" or blog_preferences.blog_archive_mode == "calendar" %}
0089:         <section class="magazin-sidebar-section">
0090:             <div class="magazin-section-title">Kalendar</div>
0091:             <div class="magazin-calendar-title calendar-month-nav"><a href="{{ prev_month_url }}" class="calendar-month-nav-link" aria-label="Prethodni mjesec">&#8249;</a><span>{{ current_month_hr|upper }}, {{ current_year }}</span><a href="{{ next_month_url }}" class="calendar-month-nav-link" aria-label="Sljedeći mjesec">&#8250;</a></div>
0092:             <div class="magazin-calendar-weekdays">
0093:                 <div>P</div><div>U</div><div>S</div><div>Č</div><div>P</div><div>S</div><div>N</div>
0094:             </div>
0095:             <div class="magazin-calendar-grid">
```
Linija 90:
```txt
0087: 
0088:         {% if blog_preferences.blog_archive_mode == "both" or blog_preferences.blog_archive_mode == "calendar" %}
0089:         <section class="magazin-sidebar-section">
0090:             <div class="magazin-section-title">Kalendar</div>
0091:             <div class="magazin-calendar-title calendar-month-nav"><a href="{{ prev_month_url }}" class="calendar-month-nav-link" aria-label="Prethodni mjesec">&#8249;</a><span>{{ current_month_hr|upper }}, {{ current_year }}</span><a href="{{ next_month_url }}" class="calendar-month-nav-link" aria-label="Sljedeći mjesec">&#8250;</a></div>
0092:             <div class="magazin-calendar-weekdays">
0093:                 <div>P</div><div>U</div><div>S</div><div>Č</div><div>P</div><div>S</div><div>N</div>
0094:             </div>
0095:             <div class="magazin-calendar-grid">
0096:                 {% for week in month_calendar %}
```
_Još 149 hitova nalazi se u JSON dokumentu._

### `forms_buttons`

Linija 22:
```txt
0019:                 {% if request.user.is_authenticated and request.user != blog %}
0020:                 <div class="magazin-profile-actions">
0021:                     {% if not is_restricted %}
0022:                         <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0023:                             {% csrf_token %}
0024:                             <button type="submit" class="btn {% if is_following %}btn-outline-primary{% else %}btn-primary{% endif %} btn-sm">
0025:                                 {% if is_following %}Pratiš{% else %}Prati{% endif %}
0026:                             </button>
0027:                         </form>
0028:                     {% endif %}
```
Linija 24:
```txt
0021:                     {% if not is_restricted %}
0022:                         <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0023:                             {% csrf_token %}
0024:                             <button type="submit" class="btn {% if is_following %}btn-outline-primary{% else %}btn-primary{% endif %} btn-sm">
0025:                                 {% if is_following %}Pratiš{% else %}Prati{% endif %}
0026:                             </button>
0027:                         </form>
0028:                     {% endif %}
0029: 
0030:                     <div class="dropdown magazin-profile-dropdown">
```
Linija 43:
```txt
0040:                         <ul class="dropdown-menu dropdown-menu-end magazin-profile-dropdown-menu">
0041:                             {% if is_following %}
0042:                                 <li>
0043:                                     <form method="post" action="{% url 'unfollow_user' blog.username %}" class="m-0">
0044:                                         {% csrf_token %}
0045:                                         <button type="submit" class="dropdown-item">Prestani pratiti</button>
0046:                                     </form>
0047:                                 </li>
0048:                             {% else %}
0049:                                 <li>
```
Linija 45:
```txt
0042:                                 <li>
0043:                                     <form method="post" action="{% url 'unfollow_user' blog.username %}" class="m-0">
0044:                                         {% csrf_token %}
0045:                                         <button type="submit" class="dropdown-item">Prestani pratiti</button>
0046:                                     </form>
0047:                                 </li>
0048:                             {% else %}
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
```
Linija 45:
```txt
0042:                                 <li>
0043:                                     <form method="post" action="{% url 'unfollow_user' blog.username %}" class="m-0">
0044:                                         {% csrf_token %}
0045:                                         <button type="submit" class="dropdown-item">Prestani pratiti</button>
0046:                                     </form>
0047:                                 </li>
0048:                             {% else %}
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
```
Linija 50:
```txt
0047:                                 </li>
0048:                             {% else %}
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
0052:                                         <button type="submit" class="dropdown-item" {% if is_restricted %}disabled{% endif %}>Prati korisnika</button>
0053:                                     </form>
0054:                                 </li>
0055:                             {% endif %}
0056: 
```
Linija 52:
```txt
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
0052:                                         <button type="submit" class="dropdown-item" {% if is_restricted %}disabled{% endif %}>Prati korisnika</button>
0053:                                     </form>
0054:                                 </li>
0055:                             {% endif %}
0056: 
0057:                             <li>
0058:                                 <form method="post" action="{% url 'restrict_user' blog.username %}" class="m-0">
```
Linija 52:
```txt
0049:                                 <li>
0050:                                     <form method="post" action="{% url 'follow_toggle' blog.username %}" class="m-0">
0051:                                         {% csrf_token %}
0052:                                         <button type="submit" class="dropdown-item" {% if is_restricted %}disabled{% endif %}>Prati korisnika</button>
0053:                                     </form>
0054:                                 </li>
0055:                             {% endif %}
0056: 
0057:                             <li>
0058:                                 <form method="post" action="{% url 'restrict_user' blog.username %}" class="m-0">
```
_Još 8 hitova nalazi se u JSON dokumentu._

### `shared_includes`

Linija 134:
```txt
0131: 
0132:         {% if blog_preferences.analytics_widget_side == 'left_top' %}
0133:         <section class="magazin-sidebar-section">
0134:             {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
0135:         </section>
0136:         {% endif %}
0137: 
0138:         {% for box in left_boxes %}
0139:         <section class="magazin-sidebar-section magazin-sidebar-section--box">
0140:             <div class="magazin-section-title">{{ box.title }}</div>
```
Linija 147:
```txt
0144: 
0145:         {% if blog_preferences.analytics_widget_side == 'right_top' %}
0146:         <section class="magazin-sidebar-section">
0147:             {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
0148:         </section>
0149:         {% endif %}
0150: 
0151:         {% for box in right_boxes %}
0152:         <section class="magazin-sidebar-section magazin-sidebar-section--box">
0153:             <div class="magazin-section-title">{{ box.title }}</div>
```
Linija 160:
```txt
0157: 
0158:         {% if blog_preferences.analytics_widget_side == 'left_bottom' or blog_preferences.analytics_widget_side == 'right_bottom' %}
0159:         <section class="magazin-sidebar-section">
0160:             {% include "blog/components/live_analytics_widget.html" with analytics_widget_class="sidebar-left-align" %}
0161:         </section>
0162:         {% endif %}
0163:     </div>
0164: </div>
0165: {% endblock %}
0166: 
```
Linija 680:
```txt
0677:                 <div class="d-flex justify-content-between align-items-start gap-3">
0678:                     <div class="d-flex flex-column" style="gap:10px; min-width:0; flex:1;">
0679:                         <h4 class="mb-0">{{ post.title }}</h4>
0680:                         {% include "blog/components/post_meta.html" %}
0681:                     </div>
0682: 
0683:                     <div class="text-center ms-3 blog-date-shell blog-date-style-{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }} blog-date-effect-{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}" style="line-height:1;" data-date-style="{{ blog_preferences.active_design_customization.post_date_style|default:'classic_vertical' }}" data-date-effect="{{ blog_preferences.active_design_customization.post_date_effect|default:'solid' }}">
0684:                         <div class="blog-date-main">
0685:                             <div class="blog-date-day-wrap">
0686:                                 <div class="blog-date-day">{{ post.publication_datetime|date:"d" }}</div>
```
Linija 704:
```txt
0701:                 </div>
0702: 
0703:                 <div class="mt-4">
0704:                     {% include "blog/components/post_body.html" %}
0705:                 </div>
0706: 
0707:                 {% include "blog/components/post_actions.html" %}
0708:                 {% include "blog/components/post_comments.html" %}
0709:                 <hr>
0710:             </article>
```
Linija 707:
```txt
0704:                     {% include "blog/components/post_body.html" %}
0705:                 </div>
0706: 
0707:                 {% include "blog/components/post_actions.html" %}
0708:                 {% include "blog/components/post_comments.html" %}
0709:                 <hr>
0710:             </article>
0711:         {% empty %}
0712:             <p class="m-4">Nema postova.</p>
0713:         {% endfor %}
```
Linija 708:
```txt
0705:                 </div>
0706: 
0707:                 {% include "blog/components/post_actions.html" %}
0708:                 {% include "blog/components/post_comments.html" %}
0709:                 <hr>
0710:             </article>
0711:         {% empty %}
0712:             <p class="m-4">Nema postova.</p>
0713:         {% endfor %}
0714: 
```
Linija 728:
```txt
0725:         {% endif %}
0726:     </div>
0727: </div>
0728: {% include "blog/components/blog_interaction_scripts.html" %}
0729: {% endblock %}
```

## Procjena

- Magazin ima vlastiti `{% for post in page_obj %}` loop, znači postovi nisu kroz zajednički `blog_posts.html`.
- Ne koristi direktno zajednički `blog_posts.html` include.
- Ne koristi direktno zajednički `blog_box.html` include.
- Već koristi zajednički `blog_interaction_scripts.html`, što je dobar znak za postupni refaktor.

## Preporuka

1. Ne mijenjati `magazin` masovno.
2. Prvo izdvojiti samo prikaz jednog posta u posebnu zajedničku/parametriziranu komponentu ili provjeriti može li postojeći `post_card.html` primiti magazin klase.
3. Sidebar i boxeve dirati tek nakon postova, jer audit pokazuje puno sidebar/form hitova.
4. Ne čistiti CSS viškove sada; samo pripremiti siguran put refaktora.

## Zaključak

`magazin` je dobar kandidat za ručni, oprezni refaktor, ali nije kandidat za masovnu automatsku zamjenu. Prvo treba odlučiti hoće li zadržati poseban magazin layout, a zajedničke komponente koristiti samo za unutarnji prikaz posta/komentara.
