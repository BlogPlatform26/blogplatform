# Phase 26A — audit stvarne strukture komentara

Izrađeno: 2026-07-06 21:13:17

## Cilj

Pročitati stvarni `post_comments.html` prije nove promjene. Ovo ništa ne mijenja u aplikaciji.

## Sažetak

- File: `C:\Users\mario\blogplatform\blog\templates\blog\components\post_comments.html`
- Broj linija: **620**
- Broj različitih class tokena: **38**
- Zanimljive comment/form/button klase: **22**
- CSS hitovi u `blog_design_styles.html`: **100**

## Zanimljive klase u `post_comments.html`

| Klasa | Ponavljanja |
|---|---:|
| `blog-action-outline` | 1 |
| `bp-comment-text` | 2 |
| `btn` | 5 |
| `btn-outline-secondary` | 2 |
| `btn-primary` | 2 |
| `btn-sm` | 4 |
| `comment-action-btn` | 4 |
| `comment-action-danger` | 2 |
| `comment-actions` | 2 |
| `comment-author` | 4 |
| `comment-avatar` | 10 |
| `comment-body` | 2 |
| `comment-edit-form` | 2 |
| `comment-header` | 2 |
| `comment-item` | 2 |
| `comment-row` | 1 |
| `comment-text` | 2 |
| `comment-time` | 2 |
| `form-check` | 1 |
| `form-check-label` | 1 |
| `form-control` | 2 |
| `premium-avatar-wrap` | 2 |

## Hitovi po kategorijama

| Kategorija | Linije |
|---|---|
| `for_comments_loop` | 298, 399 |
| `comment_body` | 4, 9, 243, 300, 302, 305, 309, 311, 321, 322, 330, 332, 336, 341, 359, 364, 368, 372, 374, 375 ... (+21) |
| `comment_text` | 248, 260, 270, 372, 377, 474, 479, 579, 596, 610 |
| `textarea` | 70, 80, 81, 82, 99, 100, 109, 117, 121, 122, 125, 128, 129, 163, 164, 171, 175, 199, 201, 205 ... (+13) |
| `submit_button` | 345, 379, 447, 481, 533 |
| `edit_delete` | 336, 337, 341, 347, 375, 380, 438, 440, 444, 449, 477, 482, 566, 570, 573, 574, 578, 580, 582, 584 ... (+6) |
| `button` | 336, 345, 379, 380, 438, 447, 481, 482, 533 |
| `form` | 341, 351, 375, 382, 444, 453, 477, 484, 526, 549 |
| `avatar` | 304, 307, 309, 311, 315, 321, 322, 326, 406, 410, 412, 413, 417, 423, 425, 429 |
| `url_tags` | 69, 341, 375, 444, 477, 503, 526, 553 |

## Najvažniji snippetovi

### `for_comments_loop`

Linija 298:
```txt
0292:   <h6>Komentari:</h6>
0293: 
0294:   {% if post.author.profile.show_post_comments %}
0295: 
0296:   {% if is_detail %}
0297: 
0298:   {% for comment in comments %}
0299: 
0300:   <div id="comment-{{ comment.id }}" class="comment-item mb-3 d-flex gap-2">
0301: 
0302:   {% if comment.author.username == anonymous_comment_username %}
0303: 
0304:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
```

Linija 399:
```txt
0393:   {% endfor %}
0394: 
0395:   {% else %}
0396: 
0397:   {% with COMMENT_LIMIT=5 %}
0398: 
0399:   {% for comment in post.comments.all %}
0400:   {% if forloop.counter <= COMMENT_LIMIT %}
0401: 
0402:   <div id="comment-{{ comment.id }}" class="comment-item mb-3 d-flex gap-2">
0403: 
0404:   {% if comment.author.username == anonymous_comment_username %}
0405: 
```

### `avatar`

Linija 304:
```txt
0298:   {% for comment in comments %}
0299: 
0300:   <div id="comment-{{ comment.id }}" class="comment-item mb-3 d-flex gap-2">
0301: 
0302:   {% if comment.author.username == anonymous_comment_username %}
0303: 
0304:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
0305:   {% elif comment.author.profile.has_active_premium %}
0306: 
0307:   <span class="premium-avatar-wrap">
0308: 
0309:   {% if comment.author.profile.avatar %}
0310: 
```

Linija 307:
```txt
0301: 
0302:   {% if comment.author.username == anonymous_comment_username %}
0303: 
0304:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
0305:   {% elif comment.author.profile.has_active_premium %}
0306: 
0307:   <span class="premium-avatar-wrap">
0308: 
0309:   {% if comment.author.profile.avatar %}
0310: 
0311:   <img src="{{ comment.author.profile.avatar.url }}" class="comment-avatar" width="35" height="35">
0312: 
0313:   {% else %}
```

Linija 309:
```txt
0303: 
0304:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
0305:   {% elif comment.author.profile.has_active_premium %}
0306: 
0307:   <span class="premium-avatar-wrap">
0308: 
0309:   {% if comment.author.profile.avatar %}
0310: 
0311:   <img src="{{ comment.author.profile.avatar.url }}" class="comment-avatar" width="35" height="35">
0312: 
0313:   {% else %}
0314: 
0315:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
```

Linija 311:
```txt
0305:   {% elif comment.author.profile.has_active_premium %}
0306: 
0307:   <span class="premium-avatar-wrap">
0308: 
0309:   {% if comment.author.profile.avatar %}
0310: 
0311:   <img src="{{ comment.author.profile.avatar.url }}" class="comment-avatar" width="35" height="35">
0312: 
0313:   {% else %}
0314: 
0315:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
0316: 
0317:   {% endif %}
```

Linija 315:
```txt
0309:   {% if comment.author.profile.avatar %}
0310: 
0311:   <img src="{{ comment.author.profile.avatar.url }}" class="comment-avatar" width="35" height="35">
0312: 
0313:   {% else %}
0314: 
0315:   <img src="{% static 'images/default-avatar.jpg' %}" class="comment-avatar" width="35" height="35">
0316: 
0317:   {% endif %}
0318: 
0319:   </span>
0320: 
0321:   {% elif comment.author.profile.avatar %}
```

### `edit_delete`

Linija 336:
```txt
0330:   <div class="comment-body flex-grow-1">
0331: 
0332:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0333: 
0334:   <div class="comment-actions">
0335: 
0336:   <button type="button" class="comment-action-btn" title="Uredi" data-edit-comment-toggle="{{ comment.id }}">
0337:   <i class="bi bi-pencil"></i>
0338: 
0339:   </button>
0340: 
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
```

Linija 337:
```txt
0331: 
0332:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0333: 
0334:   <div class="comment-actions">
0335: 
0336:   <button type="button" class="comment-action-btn" title="Uredi" data-edit-comment-toggle="{{ comment.id }}">
0337:   <i class="bi bi-pencil"></i>
0338: 
0339:   </button>
0340: 
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
0343:   {% csrf_token %}
```

Linija 341:
```txt
0335: 
0336:   <button type="button" class="comment-action-btn" title="Uredi" data-edit-comment-toggle="{{ comment.id }}">
0337:   <i class="bi bi-pencil"></i>
0338: 
0339:   </button>
0340: 
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
0343:   {% csrf_token %}
0344: 
0345:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0346: 
0347:   <i class="bi bi-trash"></i>
```

Linija 347:
```txt
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
0343:   {% csrf_token %}
0344: 
0345:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0346: 
0347:   <i class="bi bi-trash"></i>
0348: 
0349:   </button>
0350: 
0351:   </form>
0352: 
0353:   </div>
```

Linija 375:
```txt
0369: 
0370:   </div>
0371: 
0372:   <div class="comment-text" data-comment-text="{{ comment.id }}" id="comment-{{ comment.id }}"><span class="bp-comment-text">{{ comment.content|link_mentions }}</span></div>
0373: 
0374:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0375:   <form method="POST" action="{% url 'edit_comment' comment.id %}" class="comment-edit-form mt-2 d-none" data-edit-comment-form="{{ comment.id }}">
0376:     {% csrf_token %}
0377:     <textarea name="content" class="form-control" rows="3">{{ comment.content }}</textarea>
0378:     <div class="d-flex gap-2 mt-2">
0379:       <button type="submit" class="btn btn-sm btn-primary">Spremi</button>
0380:       <button type="button" class="btn btn-sm btn-outline-secondary" data-edit-comment-cancel="{{ comment.id }}">Odustani</button>
0381:     </div>
```

### `textarea`

Linija 70:
```txt
0064: }
0065: </style>
0066: 
0067: <script id="bp-mention-script">
0068: (function () {
0069:     const searchUrl = "{% url 'mention_search' %}";
0070:     let activeTextarea = null;
0071:     let activeStart = null;
0072:     let activeEnd = null;
0073:     let results = [];
0074:     let selectedIndex = 0;
0075: 
0076:     const box = document.createElement("div");
```

Linija 80:
```txt
0074:     let selectedIndex = 0;
0075: 
0076:     const box = document.createElement("div");
0077:     box.className = "bp-mention-box";
0078:     document.body.appendChild(box);
0079: 
0080:     function getMentionInfo(textarea) {
0081:         const cursor = textarea.selectionStart;
0082:         const textBeforeCursor = textarea.value.slice(0, cursor);
0083:         const match = textBeforeCursor.match(/(^|\s)@([A-Za-z0-9_.+-]{0,40})$/);
0084: 
0085:         if (!match) {
0086:             return null;
```

Linija 81:
```txt
0075: 
0076:     const box = document.createElement("div");
0077:     box.className = "bp-mention-box";
0078:     document.body.appendChild(box);
0079: 
0080:     function getMentionInfo(textarea) {
0081:         const cursor = textarea.selectionStart;
0082:         const textBeforeCursor = textarea.value.slice(0, cursor);
0083:         const match = textBeforeCursor.match(/(^|\s)@([A-Za-z0-9_.+-]{0,40})$/);
0084: 
0085:         if (!match) {
0086:             return null;
0087:         }
```

Linija 82:
```txt
0076:     const box = document.createElement("div");
0077:     box.className = "bp-mention-box";
0078:     document.body.appendChild(box);
0079: 
0080:     function getMentionInfo(textarea) {
0081:         const cursor = textarea.selectionStart;
0082:         const textBeforeCursor = textarea.value.slice(0, cursor);
0083:         const match = textBeforeCursor.match(/(^|\s)@([A-Za-z0-9_.+-]{0,40})$/);
0084: 
0085:         if (!match) {
0086:             return null;
0087:         }
0088: 
```

Linija 99:
```txt
0093:             query: query,
0094:             start: start,
0095:             end: cursor
0096:         };
0097:     }
0098: 
0099:     function positionBox(textarea) {
0100:         const rect = textarea.getBoundingClientRect();
0101:         box.style.left = (window.scrollX + rect.left) + "px";
0102:         box.style.top = (window.scrollY + rect.bottom + 6) + "px";
0103:         box.style.width = Math.min(rect.width, 320) + "px";
0104:     }
0105: 
```

### `submit_button`

Linija 345:
```txt
0339:   </button>
0340: 
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
0343:   {% csrf_token %}
0344: 
0345:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0346: 
0347:   <i class="bi bi-trash"></i>
0348: 
0349:   </button>
0350: 
0351:   </form>
```

Linija 379:
```txt
0373: 
0374:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0375:   <form method="POST" action="{% url 'edit_comment' comment.id %}" class="comment-edit-form mt-2 d-none" data-edit-comment-form="{{ comment.id }}">
0376:     {% csrf_token %}
0377:     <textarea name="content" class="form-control" rows="3">{{ comment.content }}</textarea>
0378:     <div class="d-flex gap-2 mt-2">
0379:       <button type="submit" class="btn btn-sm btn-primary">Spremi</button>
0380:       <button type="button" class="btn btn-sm btn-outline-secondary" data-edit-comment-cancel="{{ comment.id }}">Odustani</button>
0381:     </div>
0382:   </form>
0383:   {% endif %}
0384: 
0385:   </div>
```

Linija 447:
```txt
0441: 
0442:   </button>
0443: 
0444:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0445: 
0446:   {% csrf_token %}
0447:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0448: 
0449:   <i class="bi bi-trash"></i>
0450: 
0451:   </button>
0452: 
0453:   </form>
```

Linija 481:
```txt
0475: 
0476:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0477:   <form method="POST" action="{% url 'edit_comment' comment.id %}" class="comment-edit-form mt-2 d-none" data-edit-comment-form="{{ comment.id }}">
0478:     {% csrf_token %}
0479:     <textarea name="content" class="form-control" rows="3">{{ comment.content }}</textarea>
0480:     <div class="d-flex gap-2 mt-2">
0481:       <button type="submit" class="btn btn-sm btn-primary">Spremi</button>
0482:       <button type="button" class="btn btn-sm btn-outline-secondary" data-edit-comment-cancel="{{ comment.id }}">Odustani</button>
0483:     </div>
0484:   </form>
0485:   {% endif %}
0486: 
0487:   </div>
```

Linija 533:
```txt
0527: 
0528:   {% csrf_token %}
0529: 
0530:   <div class="comment-row">
0531: 
0532:   {{ form.content }}
0533:   <button type="submit" class="btn blog-action-outline">Komentiraj</button>
0534: 
0535:   </div>
0536: 
0537:   {% if post.allow_anonymous_comments %}
0538: 
0539:   <div class="form-check mt-2">
```

### `form`

Linija 341:
```txt
0335: 
0336:   <button type="button" class="comment-action-btn" title="Uredi" data-edit-comment-toggle="{{ comment.id }}">
0337:   <i class="bi bi-pencil"></i>
0338: 
0339:   </button>
0340: 
0341:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0342: 
0343:   {% csrf_token %}
0344: 
0345:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0346: 
0347:   <i class="bi bi-trash"></i>
```

Linija 351:
```txt
0345:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0346: 
0347:   <i class="bi bi-trash"></i>
0348: 
0349:   </button>
0350: 
0351:   </form>
0352: 
0353:   </div>
0354: 
0355:   {% endif %}
0356: 
0357:   <div class="comment-header">
```

Linija 375:
```txt
0369: 
0370:   </div>
0371: 
0372:   <div class="comment-text" data-comment-text="{{ comment.id }}" id="comment-{{ comment.id }}"><span class="bp-comment-text">{{ comment.content|link_mentions }}</span></div>
0373: 
0374:   {% if user.is_authenticated and user == comment.author and comment.author.username != anonymous_comment_username %}
0375:   <form method="POST" action="{% url 'edit_comment' comment.id %}" class="comment-edit-form mt-2 d-none" data-edit-comment-form="{{ comment.id }}">
0376:     {% csrf_token %}
0377:     <textarea name="content" class="form-control" rows="3">{{ comment.content }}</textarea>
0378:     <div class="d-flex gap-2 mt-2">
0379:       <button type="submit" class="btn btn-sm btn-primary">Spremi</button>
0380:       <button type="button" class="btn btn-sm btn-outline-secondary" data-edit-comment-cancel="{{ comment.id }}">Odustani</button>
0381:     </div>
```

Linija 382:
```txt
0376:     {% csrf_token %}
0377:     <textarea name="content" class="form-control" rows="3">{{ comment.content }}</textarea>
0378:     <div class="d-flex gap-2 mt-2">
0379:       <button type="submit" class="btn btn-sm btn-primary">Spremi</button>
0380:       <button type="button" class="btn btn-sm btn-outline-secondary" data-edit-comment-cancel="{{ comment.id }}">Odustani</button>
0381:     </div>
0382:   </form>
0383:   {% endif %}
0384: 
0385:   </div>
0386: 
0387:   </div>
0388: 
```

Linija 444:
```txt
0438:   <button type="button" class="comment-action-btn" title="Uredi" data-edit-comment-toggle="{{ comment.id }}">
0439: 
0440:   <i class="bi bi-pencil"></i>
0441: 
0442:   </button>
0443: 
0444:   <form method="POST" action="{% url 'delete_comment' comment.id %}" class="d-inline">
0445: 
0446:   {% csrf_token %}
0447:   <button type="submit" class="comment-action-btn comment-action-danger" title="Izbriši" onclick="return confirm('Jeste li sigurni da želite izbrisati komentar?')">
0448: 
0449:   <i class="bi bi-trash"></i>
0450: 
```

## CSS hitovi u `blog_design_styles.html`

| Linija | Tekst |
|---:|---|
| 94 | `.comment-item {` |
| 102 | `.comment-avatar {` |
| 113 | `.comment-body {` |
| 119 | `.comment-header {` |
| 127 | `.comment-author,` |
| 128 | `.comment-author a {` |
| 133 | `.comment-text {` |
| 140 | `.comment-row {` |
| 147 | `.comment-row textarea {` |
| 153 | `.comment-item {` |
| 157 | `.comment-avatar {` |
| 164 | `.comment-row {` |
| 170 | `.comment-row .btn,` |
| 171 | `.comment-row button {` |
| 851 | `.comment-body {` |
| 856 | `textarea.form-control {` |
| 862 | `textarea.form-control:focus {` |
| 869 | `.comment-text,` |
| 872 | `.comment-time {` |
| 946 | `.comment-author a,` |
| 1229 | `.blog-main-right-column--simple-retro .comment-action-btn,` |
| 1231 | `.blog-posts-shell--simple-retro .comment-action-btn,` |
| 1234 | `.blog-posts-shell--simple-retro .comment-author a,` |
| 1399 | `.comment-body {` |
| 1536 | `.comment-text,` |
| 1537 | `.comment-time {` |
| 1556 | `.comment-body {` |
| 1560 | `textarea.form-control {` |
| 1567 | `textarea.form-control:focus {` |
| 1579 | `.btn-outline-light {` |
| 1585 | `.btn-outline-light:hover {` |
| 1603 | `.comment-author a,` |
| 1612 | `.comment-author a:hover,` |
| 1758 | `.comment-body {` |
| 1897 | `.comment-text,` |
| 1898 | `.comment-time {` |
| 1917 | `.comment-body {` |
| 1921 | `textarea.form-control {` |
| 1928 | `textarea.form-control:focus {` |
| 1940 | `.btn-outline-light {` |
| 1946 | `.btn-outline-light:hover {` |
| 1972 | `.comment-author a,` |
| 1981 | `.comment-author a:hover,` |
| 2041 | `.comment-row{ display:flex; align-items:center; gap:10px; max-width:520px; }` |
| 2042 | `.comment-row textarea{ flex:1; }` |
| 2043 | `.blog-action-outline,.btn-outline-light{ border-color:#4da3ff !important; color:#4da3ff !important; }` |
| 2044 | `.blog-action-outline:hover,.btn-outline-light:hover{ background-color:#4da3ff !important; color:#000 !important; box-shadow:0 0 8px rgba(77,163,255,0.5); }` |
| 2045 | `textarea.form-control{ background-color:#1a1a1a !important; color:#fff !important; border:1px solid #444 !important; border-radius:10px; padding:10px; resize:none; height:50px; }` |
| 2046 | `textarea.form-control:focus{ background-color:#1a1a1a !important; color:#fff !important; border-color:#4da3ff !important; box-shadow:0 0 6px rgba(77,163,255,0.4) !important; outline:none; }` |
| 2050 | `.comment-item{ align-items:flex-start; }` |
| 2051 | `.comment-avatar{ border-radius:50%; object-fit:cover; margin-top:2px; }` |
| 2052 | `.comment-body{ position:relative; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:10px 44px 10px 12px; }` |
| 2053 | `.comment-header{ display:flex; gap:10px; align-items:baseline; margin-bottom:2px; }` |
| 2054 | `.comment-author a{ color:#4da3ff; text-decoration:none; }` |
| 2055 | `.comment-time{ font-size:12px; color:rgba(255,255,255,0.45); }` |
| 2056 | `.comment-text{ color:rgba(255,255,255,0.92); line-height:1.3; }` |
| 2057 | `.comment-actions{ position:absolute; top:8px; right:10px; display:flex; gap:8px; align-items:center; opacity:0; transition:opacity 120ms ease-in-out; }` |
| 2058 | `.comment-item:hover .comment-actions{ opacity:0.9; }` |
| 2059 | `.comment-action-btn{ width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:transparent; border:1px solid rgba(255,255,255,0.10); border-radius:8px; cursor:pointer; color:rgba(255,255,255,0.60); padding:0; margin:0; line-height:1; }` |
| 2060 | `.comment-action-btn i{ font-size:14px; line-height:1; display:block; }` |
| 2061 | `.comment-action-btn:hover{ color:rgba(255,255,255,0.95); border-color:rgba(255,255,255,0.18); background:rgba(255,255,255,0.04); }` |
| 2062 | `.comment-action-danger:hover{ color:#ff6b6b; border-color:rgba(255,107,107,0.35); background:rgba(255,107,107,0.08); }` |
| 2103 | `.comment-row{ display:flex; align-items:center; gap:10px; max-width:520px; }` |
| 2104 | `.comment-row textarea{ flex:1; }` |
| 2105 | `.blog-action-outline,.btn-outline-light{ border-color:#7a2cff !important; color:#7a2cff !important; }` |
| 2106 | `.blog-action-outline:hover,.btn-outline-light:hover{ background-color:#7a2cff !important; color:#fff !important; box-shadow:0 0 8px rgba(122,44,255,0.35); }` |
| 2107 | `textarea.form-control{ background:#ece8df !important; color:#111 !important; border:1px solid #d7d0c5 !important; border-radius:10px; padding:10px; resize:none; height:50px; }` |
| 2108 | `textarea.form-control:focus{ background:#f6f4ef !important; color:#111 !important; border-color:#7a2cff !important; box-shadow:0 0 6px rgba(122,44,255,0.25) !important; outline:none; }` |
| 2112 | `.comment-item{ align-items:flex-start; }` |
| 2113 | `.comment-avatar{ border-radius:50%; object-fit:cover; margin-top:2px; }` |
| 2114 | `.comment-body{ position:relative; background:#f6f4ef; border:1px solid #d7d0c5; border-radius:12px; padding:10px 44px 10px 12px; }` |
| 2115 | `.comment-header{ display:flex; gap:10px; align-items:baseline; margin-bottom:2px; }` |
| 2116 | `.comment-author a{ color:#7a2cff; text-decoration:none; }` |
| 2117 | `.comment-time{ font-size:12px; color:#777; }` |
| 2118 | `.comment-text{ color:#1f1f1f; line-height:1.3; }` |
| 2119 | `.comment-actions{ position:absolute; top:8px; right:10px; display:flex; gap:8px; align-items:center; opacity:0; transition:opacity 120ms ease-in-out; }` |
| 2120 | `.comment-item:hover .comment-actions{ opacity:0.9; }` |
| 2121 | `.comment-action-btn{ width:28px; height:28px; display:flex; align-items:center; justify-content:center; background:transparent; border:1px solid rgba(0,0,0,0.12); border-radius:8px; cursor:pointer; color:rgba(0,0,0,0.60); padding:0; margin:0; line-height:1; }` |
| 2122 | `.comment-action-btn i{ font-size:14px; line-height:1; display:block; }` |
| 2123 | `.comment-action-btn:hover{ color:#111; border-color:rgba(0,0,0,0.20); background:rgba(0,0,0,0.04); }` |

_Još 20 hitova nalazi se u JSON dokumentu._

## Preporuka

1. Ne raditi novu promjenu dok se ne vidi stvarni HTML iz ovog audita.
2. Sljedeća skripta treba ciljati postojeće klase i strukturu iz `post_comments.html`, ne generičke pretpostavke.
3. Ako se komentari u nekom posebnom dizajnu ne prikazuju kroz ovu komponentu, to treba posebno zabilježiti.