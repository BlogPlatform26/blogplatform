from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

VIEWS_PY = ROOT / "blog" / "views.py"
URLS_PY = ROOT / "blogplatform" / "urls.py"
ADMIN_PY = ROOT / "blog" / "admin.py"
BASE_HTML = ROOT / "blog" / "templates" / "blog" / "base.html"

def backup(path: Path, suffix: str):
    if path.exists():
        backup_path = path.with_name(path.name + suffix)
        if not backup_path.exists():
            backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def require_file(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Ne postoji: {path}")

for p in (VIEWS_PY, URLS_PY, ADMIN_PY):
    require_file(p)

backup(VIEWS_PY, ".bak_before_admin_post_export_v2")
views_text = VIEWS_PY.read_text(encoding="utf-8")
import_line = "from blog.view_handlers.admin_post_export_views import *"
if import_line not in views_text:
    if views_text and not views_text.endswith("\n"):
        views_text += "\n"
    views_text += import_line + "\n"
    VIEWS_PY.write_text(views_text, encoding="utf-8")

backup(URLS_PY, ".bak_before_admin_post_export_v2")
urls_text = URLS_PY.read_text(encoding="utf-8")

urls_text = re.sub(r'^\s*path\(["\']admin/post-exports/["\'].*?admin_post_exports.*?\),\s*\n', '', urls_text, flags=re.MULTILINE)
urls_text = re.sub(r'^\s*path\(["\']admin/post-exports/.*?download/["\'].*?admin_export_user_posts.*?\),\s*\n', '', urls_text, flags=re.MULTILINE)

if "from blog import views" not in urls_text:
    if "from django.urls import path, include" in urls_text:
        urls_text = urls_text.replace("from django.urls import path, include", "from django.urls import path, include\nfrom blog import views", 1)
    else:
        urls_text = "from blog import views\n" + urls_text

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
    raise RuntimeError("Nisam našao admin rutu u blogplatform/urls.py.")

URLS_PY.write_text(urls_text, encoding="utf-8")

backup(ADMIN_PY, ".bak_before_admin_post_export_v2")
admin_text = ADMIN_PY.read_text(encoding="utf-8")

admin_text = re.sub(
    r'\n# === ADMIN POST EXPORT LINK ===[\s\S]*?admin\.site\.get_app_list\s*=\s*_get_app_list_with_post_export\s*\n?',
    "\n",
    admin_text,
)
admin_text = re.sub(
    r'\n# === ADMIN POST EXPORT LINK V2 ===[\s\S]*?admin\.site\.get_app_list\s*=\s*_get_app_list_with_post_export_v2\s*\n?',
    "\n",
    admin_text,
)

admin_text += r'''

# === ADMIN POST EXPORT LINK V2 ===
_PREVIOUS_GET_APP_LIST_WITHOUT_POST_EXPORT_V2 = admin.site.get_app_list

def _post_export_admin_row_v2():
    return {
        "name": "Izvoz postova korisnika",
        "object_name": "PostExport",
        "perms": {"add": False, "change": False, "delete": False, "view": True},
        "admin_url": "/admin/post-exports/",
        "add_url": None,
        "view_only": True,
    }

def _get_app_list_with_post_export_v2(request, app_label=None):
    app_list = _PREVIOUS_GET_APP_LIST_WITHOUT_POST_EXPORT_V2(request, app_label)

    if app_label:
        return app_list

    row = _post_export_admin_row_v2()

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

admin.site.get_app_list = _get_app_list_with_post_export_v2
'''
ADMIN_PY.write_text(admin_text, encoding="utf-8")

if BASE_HTML.exists():
    backup(BASE_HTML, ".bak_before_admin_post_export_v2")
    base_text = BASE_HTML.read_text(encoding="utf-8")
    if "Izvoz postova korisnika" in base_text and "admin_post_exports" in base_text:
        base_text = re.sub(
            r'\s*<li>\s*<a[^>]+href=.*?admin_post_exports.*?>.*?Izvoz postova korisnika.*?</a>\s*</li>',
            "",
            base_text,
            flags=re.DOTALL,
        )
        BASE_HTML.write_text(base_text, encoding="utf-8")

print("Gotovo.")
print("Dodano u Django admin: Postovi i sadržaj > Izvoz postova korisnika")
print("Sada pokreni:")
print("python manage.py check")
print("python manage.py runserver")
