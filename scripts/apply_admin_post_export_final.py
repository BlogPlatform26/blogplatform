from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

POST_EXPORT_VIEWS = ROOT / "blog" / "view_handlers" / "post_export_views.py"
VIEWS_PY = ROOT / "blog" / "views.py"
URLS_PY = ROOT / "blogplatform" / "urls.py"
ADMIN_PY = ROOT / "blog" / "admin.py"
ADMIN_TEMPLATE = ROOT / "blog" / "templates" / "admin" / "post_exports.html"
BASE_HTML = ROOT / "blog" / "templates" / "blog" / "base.html"

def backup(path: Path, suffix: str):
    if path.exists():
        backup_path = path.with_name(path.name + suffix)
        if not backup_path.exists():
            backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        return backup_path
    return None

def require_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Ne postoji: {path}")

for p in (POST_EXPORT_VIEWS, VIEWS_PY, URLS_PY, ADMIN_PY):
    require_file(p)

# 1) Dodaj admin viewove u post_export_views.py.
backup(POST_EXPORT_VIEWS, ".bak_before_admin_post_export_final")
text = POST_EXPORT_VIEWS.read_text(encoding="utf-8")

admin_views_marker = "# === ADMIN POST EXPORT VIEWS ==="
if admin_views_marker not in text:
    if "_build_user_posts_zip" not in text:
        raise RuntimeError("Nisam našao _build_user_posts_zip u post_export_views.py. Prvo mora raditi korisnički export.")

    text += r'''

# === ADMIN POST EXPORT VIEWS ===
from django.contrib import admin as _post_export_admin
from django.contrib.admin.views.decorators import staff_member_required as _post_export_staff_member_required
from django.contrib.auth import get_user_model as _post_export_get_user_model
from django.shortcuts import get_object_or_404 as _post_export_get_object_or_404
from django.shortcuts import render as _post_export_render
from django.views.decorators.http import require_GET as _post_export_require_GET

try:
    from blog.security import log_security_event as _post_export_log_security_event
except Exception:
    _post_export_log_security_event = None


def _admin_export_filename_for_user(user):
    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M")
    username = _safe_filename(getattr(user, "username", "") or "korisnik", fallback="korisnik")
    return f"postovi_{username}_{timestamp}.zip"


@_post_export_staff_member_required
@_post_export_require_GET
def admin_post_exports(request):
    User = _post_export_get_user_model()
    q = (request.GET.get("q") or "").strip()

    users = User.objects.all().order_by("username")
    if q:
        users = users.filter(username__icontains=q)

    users = users[:100]

    users_with_counts = []
    for user in users:
        users_with_counts.append({
            "user": user,
            "post_count": Post.objects.filter(author=user).count(),
        })

    context = {
        **_post_export_admin.site.each_context(request),
        "title": "Izvoz postova korisnika",
        "q": q,
        "users_with_counts": users_with_counts,
    }
    return _post_export_render(request, "admin/post_exports.html", context)


@_post_export_staff_member_required
@_post_export_require_GET
def admin_export_user_posts(request, user_id):
    User = _post_export_get_user_model()
    target_user = _post_export_get_object_or_404(User, pk=user_id)

    archive = _build_user_posts_zip(target_user)
    filename = _admin_export_filename_for_user(target_user)

    if _post_export_log_security_event:
        try:
            _post_export_log_security_event(
                request=request,
                event_type="admin_post_export",
                user=request.user,
                severity="info",
                message=f"Admin je izvezao postove korisnika: {target_user.username}",
                metadata={
                    "target_user_id": target_user.id,
                    "target_username": target_user.username,
                },
            )
        except Exception:
            pass

    response = HttpResponse(archive.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
'''
    POST_EXPORT_VIEWS.write_text(text, encoding="utf-8")

# 2) Osiguraj da blog/views.py uvozi post_export_views.
backup(VIEWS_PY, ".bak_before_admin_post_export_final")
views_text = VIEWS_PY.read_text(encoding="utf-8")
import_line = "from blog.view_handlers.post_export_views import *"
if import_line not in views_text:
    if views_text and not views_text.endswith("\n"):
        views_text += "\n"
    views_text += import_line + "\n"
    VIEWS_PY.write_text(views_text, encoding="utf-8")

# 3) Dodaj URL rute prije Django admin rute.
backup(URLS_PY, ".bak_before_admin_post_export_final")
urls_text = URLS_PY.read_text(encoding="utf-8")

if "admin_post_exports" not in urls_text:
    if "from blog import views" not in urls_text:
        urls_text = urls_text.replace("from django.urls import path, include", "from django.urls import path, include\nfrom blog import views", 1)

    routes = (
        '    path("admin/post-exports/", views.admin_post_exports, name="admin_post_exports"),\n'
        '    path("admin/post-exports/<int:user_id>/download/", views.admin_export_user_posts, name="admin_export_user_posts"),\n'
    )

    admin_patterns = [
        'path("admin/", admin.site.urls)',
        "path('admin/', admin.site.urls)",
        'path("admin/", admin.site.urls),',
        "path('admin/', admin.site.urls),",
    ]

    inserted = False
    for pattern in admin_patterns:
        if pattern in urls_text:
            urls_text = urls_text.replace(pattern, routes + "    " + pattern, 1)
            inserted = True
            break

    if not inserted:
        raise RuntimeError("Nisam našao path('admin/', admin.site.urls) u blogplatform/urls.py.")

    URLS_PY.write_text(urls_text, encoding="utf-8")

# 4) Dodaj template za admin stranicu.
ADMIN_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)
backup(ADMIN_TEMPLATE, ".bak_before_admin_post_export_final")
ADMIN_TEMPLATE.write_text(r'''{% extends "admin/base_site.html" %}

{% block content %}
<div id="content-main">
    <h1>Izvoz postova korisnika</h1>

    <p>
        Ovdje administrator može preuzeti ZIP s postovima odabranog korisnika.
        Izvoz uključuje HTML postove i slike koje pripadaju postovima.
    </p>

    <p>
        Ne izvoze se komentari drugih korisnika, notifikacije, IP adrese ni sigurnosni događaji.
    </p>

    <form method="get" style="margin: 20px 0;">
        <label for="q"><strong>Pretraži korisnika:</strong></label>
        <input type="text" name="q" id="q" value="{{ q }}" style="min-width: 280px;">
        <button type="submit" class="button">Traži</button>
    </form>

    <table>
        <thead>
            <tr>
                <th>Korisnik</th>
                <th>Email</th>
                <th>Broj postova</th>
                <th>Akcija</th>
            </tr>
        </thead>
        <tbody>
            {% for row in users_with_counts %}
                <tr>
                    <td>{{ row.user.username }}</td>
                    <td>{{ row.user.email|default:"-" }}</td>
                    <td>{{ row.post_count }}</td>
                    <td>
                        {% if row.post_count %}
                            <a class="button" href="{% url 'admin_export_user_posts' row.user.id %}">
                                Preuzmi postove
                            </a>
                        {% else %}
                            <span style="color: #777;">Nema postova</span>
                        {% endif %}
                    </td>
                </tr>
            {% empty %}
                <tr>
                    <td colspan="4">Nema korisnika za prikaz.</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
''', encoding="utf-8")

# 5) Dodaj link u Django admin početnu stranicu, ali NE u obični dropdown.
backup(ADMIN_PY, ".bak_before_admin_post_export_final")
admin_text = ADMIN_PY.read_text(encoding="utf-8")

admin_link_marker = "# === ADMIN POST EXPORT LINK ==="
if admin_link_marker not in admin_text:
    admin_text += r'''

# === ADMIN POST EXPORT LINK ===
_PREVIOUS_GET_APP_LIST_WITHOUT_POST_EXPORT = admin.site.get_app_list

def _post_export_admin_row():
    return {
        "name": "Izvoz postova korisnika",
        "object_name": "PostExport",
        "perms": {"add": False, "change": False, "delete": False, "view": True},
        "admin_url": "/admin/post-exports/",
        "add_url": None,
        "view_only": True,
    }

def _get_app_list_with_post_export(request, app_label=None):
    app_list = _PREVIOUS_GET_APP_LIST_WITHOUT_POST_EXPORT(request, app_label)

    if app_label:
        return app_list

    row = _post_export_admin_row()

    for app in app_list:
        if app.get("name") == "Postovi i sadržaj":
            models = app.setdefault("models", [])
            if not any(model.get("object_name") == "PostExport" for model in models):
                models.insert(0, row)
            return app_list

    app_list.append({
        "name": "Postovi i sadržaj",
        "app_label": "post_exports",
        "app_url": "",
        "has_module_perms": True,
        "models": [row],
    })
    return app_list

admin.site.get_app_list = _get_app_list_with_post_export
'''
    ADMIN_PY.write_text(admin_text, encoding="utf-8")

# 6) Ako je neka ranija skripta dodala link u obični dropdown, probaj ga maknuti oprezno.
if BASE_HTML.exists():
    backup(BASE_HTML, ".bak_before_admin_post_export_final")
    base_text = BASE_HTML.read_text(encoding="utf-8")
    if "admin_post_exports" in base_text and "Izvoz postova korisnika" in base_text:
        base_text_new = re.sub(
            r'\s*<li>\s*<a[^>]+href="\{% url \'admin_post_exports\' %\}"[^>]*>.*?Izvoz postova korisnika.*?</a>\s*</li>',
            "",
            base_text,
            flags=re.DOTALL,
        )
        if base_text_new != base_text:
            BASE_HTML.write_text(base_text_new, encoding="utf-8")

print("Gotovo.")
print("Dodano:")
print("- admin URL: /admin/post-exports/")
print("- link u Django adminu: Postovi i sadržaj > Izvoz postova korisnika")
print("- nije dodan link u obični korisnički dropdown")
print("")
print("Sada pokreni:")
print("python manage.py check")
print("python manage.py runserver")
