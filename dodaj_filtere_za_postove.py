from pathlib import Path
import shutil
import datetime

ROOT = Path.cwd()

if not (ROOT / "manage.py").exists():
    print("GREŠKA: Pokreni skriptu iz glavnog foldera projekta: C:\\Users\\mario\\blogplatform")
    raise SystemExit(1)

settings_views_path = ROOT / "blog" / "view_handlers" / "settings_views.py"
posts_tab_path = ROOT / "blog" / "templates" / "blog" / "settings" / "_posts_tab.html"

missing = [p for p in [settings_views_path, posts_tab_path] if not p.exists()]
if missing:
    print("GREŠKA: Ne nalazim ove datoteke:")
    for path in missing:
        print("-", path.relative_to(ROOT))
    raise SystemExit(1)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = ROOT / f"backup_prije_filtera_postova_{timestamp}"
backup_dir.mkdir(exist_ok=True)

for path in [settings_views_path, posts_tab_path]:
    backup_path = backup_dir / path.relative_to(ROOT)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)

print(f"Backup napravljen: {backup_dir.name}")

# ============================================================
# 1. SETTINGS_VIEWS.PY
# ============================================================

views_text = settings_views_path.read_text(encoding="utf-8")

old_vars = """    post_filter = request.GET.get('post_filter', 'published')
    post_id = request.GET.get('post_id')
    edit_post = None
    user_posts = None
    post_form = PostForm()
"""

new_vars = """    post_filter = request.GET.get('post_filter', 'published')
    post_id = request.GET.get('post_id')
    edit_post = None
    user_posts = None
    post_form = PostForm()

    post_search_query = request.GET.get('post_q', '').strip()
    post_category_filter = request.GET.get('post_category', '').strip()
    post_tag_filter = request.GET.get('post_tag', '').strip()
    post_type_filter = request.GET.get('post_type', '').strip()
    post_year_filter = request.GET.get('post_year', '').strip()
    post_month_filter = request.GET.get('post_month', '').strip()

    post_filter_values = {
        'q': post_search_query,
        'category': post_category_filter,
        'tag': post_tag_filter,
        'type': post_type_filter,
        'year': post_year_filter,
        'month': post_month_filter,
    }
"""

if "post_search_query = request.GET.get('post_q'" not in views_text:
    if old_vars not in views_text:
        print("GREŠKA: Ne nalazim početni blok za post_filter varijable.")
        raise SystemExit(1)

    views_text = views_text.replace(old_vars, new_vars, 1)
    print("Dodane GET varijable za filter postova u settings_views.py")
else:
    print("GET varijable za filter postova već postoje u settings_views.py")

old_user_posts = """    if post_filter == 'published':
        user_posts = annotate_publication_datetime(Post.objects.filter(author=request.user, status='published')).order_by('-publication_datetime_db', '-created_at')
    elif post_filter == 'draft':
        user_posts = Post.objects.filter(author=request.user, status='draft').order_by('-created_at')
    elif post_filter == 'scheduled':
        user_posts = Post.objects.filter(author=request.user, status='scheduled').order_by('publish_at', '-created_at')
    elif post_filter == 'deleted':
        user_posts = Post.objects.filter(author=request.user, status='deleted').order_by('-created_at')

"""

new_user_posts = """    if post_filter == 'published':
        user_posts = annotate_publication_datetime(Post.objects.filter(author=request.user, status='published')).order_by('-publication_datetime_db', '-created_at')
    elif post_filter == 'draft':
        user_posts = Post.objects.filter(author=request.user, status='draft').order_by('-created_at')
    elif post_filter == 'scheduled':
        user_posts = Post.objects.filter(author=request.user, status='scheduled').order_by('publish_at', '-created_at')
    elif post_filter == 'deleted':
        user_posts = Post.objects.filter(author=request.user, status='deleted').order_by('-created_at')

    if post_filter in {'published', 'draft', 'deleted'} and user_posts is not None:
        if post_search_query:
            user_posts = user_posts.filter(title__icontains=post_search_query)

        if post_category_filter.isdigit():
            user_posts = user_posts.filter(category_id=int(post_category_filter))

        if post_tag_filter:
            user_posts = user_posts.filter(tags__name__icontains=post_tag_filter).distinct()

        if post_type_filter in {'post', 'quiz', 'poll'}:
            user_posts = user_posts.filter(post_type=post_type_filter)

        year_value = int(post_year_filter) if post_year_filter.isdigit() else None
        month_value = int(post_month_filter) if post_month_filter.isdigit() else None

        if month_value is not None and not 1 <= month_value <= 12:
            month_value = None

        if year_value and month_value:
            user_posts = user_posts.filter(
                Q(created_at__year=year_value, created_at__month=month_value)
                | Q(publish_at__year=year_value, publish_at__month=month_value)
            )
        elif year_value:
            user_posts = user_posts.filter(
                Q(created_at__year=year_value)
                | Q(publish_at__year=year_value)
            )
        elif month_value:
            user_posts = user_posts.filter(
                Q(created_at__month=month_value)
                | Q(publish_at__month=month_value)
            )

    available_post_years = sorted({
        date_value.year
        for date_value in Post.objects.filter(
            author=request.user,
            status__in=['published', 'draft', 'deleted']
        ).dates('created_at', 'year', order='DESC')
    }, reverse=True)

    post_month_choices = [
        (1, 'Siječanj'),
        (2, 'Veljača'),
        (3, 'Ožujak'),
        (4, 'Travanj'),
        (5, 'Svibanj'),
        (6, 'Lipanj'),
        (7, 'Srpanj'),
        (8, 'Kolovoz'),
        (9, 'Rujan'),
        (10, 'Listopad'),
        (11, 'Studeni'),
        (12, 'Prosinac'),
    ]

    has_active_post_filters = any(post_filter_values.values())

"""

if "has_active_post_filters = any(post_filter_values.values())" not in views_text:
    if old_user_posts not in views_text:
        print("GREŠKA: Ne nalazim blok gdje se postavlja user_posts.")
        raise SystemExit(1)

    views_text = views_text.replace(old_user_posts, new_user_posts, 1)
    print("Dodana logika filtriranja user_posts u settings_views.py")
else:
    print("Logika filtriranja user_posts već postoji u settings_views.py")

old_context = """        'user_posts': user_posts,
        'post_filter': post_filter,
        'edit_post': edit_post,
"""

new_context = """        'user_posts': user_posts,
        'post_filter': post_filter,
        'post_filter_values': post_filter_values,
        'post_month_choices': post_month_choices,
        'available_post_years': available_post_years,
        'has_active_post_filters': has_active_post_filters,
        'edit_post': edit_post,
"""

if "'post_filter_values': post_filter_values" not in views_text:
    if old_context not in views_text:
        print("GREŠKA: Ne nalazim context blok za user_posts/post_filter.")
        raise SystemExit(1)

    views_text = views_text.replace(old_context, new_context, 1)
    print("Dodani filter podaci u context")
else:
    print("Filter podaci već postoje u contextu")

settings_views_path.write_text(views_text, encoding="utf-8")

# ============================================================
# 2. _POSTS_TAB.HTML
# ============================================================

posts_text = posts_tab_path.read_text(encoding="utf-8")

filter_panel = """
            {% if post_filter == "published" or post_filter == "draft" or post_filter == "deleted" %}
                <div class="card mb-4 shadow-sm post-filter-panel">
                    <div class="card-body">
                        <form method="GET" class="row g-3 align-items-end">
                            <input type="hidden" name="tab" value="postovi">
                            <input type="hidden" name="post_filter" value="{{ post_filter }}">

                            <div class="col-md-4">
                                <label class="form-label">Pretraga po naslovu</label>
                                <input
                                    type="text"
                                    name="post_q"
                                    value="{{ post_filter_values.q }}"
                                    class="form-control"
                                    placeholder="Upiši naziv objave">
                            </div>

                            <div class="col-md-4">
                                <label class="form-label">Kategorija</label>
                                <select name="post_category" class="form-select">
                                    <option value="">Sve kategorije</option>

                                    {% regroup categories by group as filter_category_groups %}

                                    {% for group in filter_category_groups %}
                                        <optgroup label="{{ group.list.0.get_group_display }}">
                                            {% for category in group.list %}
                                                <option value="{{ category.id }}"
                                                    {% if post_filter_values.category == category.id|stringformat:"s" %}selected{% endif %}>
                                                    {{ category.name }}
                                                </option>
                                            {% endfor %}
                                        </optgroup>
                                    {% endfor %}
                                </select>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label">Tag</label>
                                <input
                                    type="text"
                                    name="post_tag"
                                    value="{{ post_filter_values.tag }}"
                                    class="form-control"
                                    placeholder="npr. film_serije">
                            </div>

                            <div class="col-md-3">
                                <label class="form-label">Tip objave</label>
                                <select name="post_type" class="form-select">
                                    <option value="">Sve</option>
                                    <option value="post" {% if post_filter_values.type == "post" %}selected{% endif %}>Post</option>
                                    <option value="quiz" {% if post_filter_values.type == "quiz" %}selected{% endif %}>Kviz</option>
                                    <option value="poll" {% if post_filter_values.type == "poll" %}selected{% endif %}>Anketa</option>
                                </select>
                            </div>

                            <div class="col-md-3">
                                <label class="form-label">Godina</label>
                                <select name="post_year" class="form-select">
                                    <option value="">Sve godine</option>
                                    {% for year in available_post_years %}
                                        <option value="{{ year }}"
                                            {% if post_filter_values.year == year|stringformat:"s" %}selected{% endif %}>
                                            {{ year }}
                                        </option>
                                    {% endfor %}
                                </select>
                            </div>

                            <div class="col-md-3">
                                <label class="form-label">Mjesec</label>
                                <select name="post_month" class="form-select">
                                    <option value="">Svi mjeseci</option>
                                    {% for month_number, month_name in post_month_choices %}
                                        <option value="{{ month_number }}"
                                            {% if post_filter_values.month == month_number|stringformat:"s" %}selected{% endif %}>
                                            {{ month_name }}
                                        </option>
                                    {% endfor %}
                                </select>
                            </div>

                            <div class="col-md-3 d-flex gap-2">
                                <button type="submit" class="btn btn-primary flex-fill">
                                    Filtriraj
                                </button>

                                <a href="?tab=postovi&post_filter={{ post_filter }}" class="btn btn-outline-secondary flex-fill">
                                    Očisti
                                </a>
                            </div>
                        </form>

                        {% if has_active_post_filters %}
                            <div class="small text-muted mt-3">
                                Prikazani su rezultati prema odabranom filteru.
                            </div>
                        {% endif %}
                    </div>
                </div>
            {% endif %}
"""

if "post-filter-panel" not in posts_text:
    marker = """            </ul>

            <!-- EDIT POST -->"""
    replacement = """            </ul>
""" + filter_panel + """
            <!-- EDIT POST -->"""

    if marker not in posts_text:
        print("GREŠKA: Ne nalazim mjesto nakon tabova gdje treba ubaciti filter panel.")
        raise SystemExit(1)

    posts_text = posts_text.replace(marker, replacement, 1)
    print("Dodan filter panel u _posts_tab.html")
else:
    print("Filter panel već postoji u _posts_tab.html")

posts_tab_path.write_text(posts_text, encoding="utf-8")

print("\nGOTOVO.")
print("Dodan je filter panel za: Objavljeni, Skice i Otpad.")
print("Filteri: naslov, kategorija, tag, tip objave, godina i mjesec.")
print("\nSada pokreni:")
print("python manage.py runserver")
print("\nNe treba makemigrations ni migrate.")
