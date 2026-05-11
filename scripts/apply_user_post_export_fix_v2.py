from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

URLS_PATH = ROOT / "blogplatform" / "urls.py"
SETTINGS_TAB_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

IMPORT_LINE = "from blog.view_handlers.post_export_views import export_my_posts\n"
URL_LINE = '    path("blog/settings/export-posts/", export_my_posts, name="export_my_posts"),\n'

EXPORT_BLOCK = """

<div class="card border-0 shadow-sm mb-4">
    <div class="card-body">
        <h5 class="card-title mb-2">Izvoz mojih postova</h5>
        <p class="text-muted mb-3">
            Preuzmi ZIP datoteku sa svojim postovima. U izvoz ulaze tvoji postovi,
            HTML prikaz postova, JSON/CSV pregled i slike koje pripadaju postovima.
            Komentari drugih korisnika, lajkovi, notifikacije i sigurnosni zapisi nisu uključeni.
        </p>
        <a href="{% url 'export_my_posts' %}" class="btn btn-outline-primary">
            Preuzmi moje postove
        </a>
    </div>
</div>
"""


def backup(path: Path, suffix: str):
    backup_path = path.with_name(path.name + suffix)
    if not backup_path.exists():
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")


def update_urls():
    if not URLS_PATH.exists():
        raise FileNotFoundError(f"Ne postoji: {URLS_PATH}")

    text = URLS_PATH.read_text(encoding="utf-8")
    original = text

    if IMPORT_LINE.strip() not in text:
        # Dodaj import na početak. Ovo ne dira postojeće rute.
        text = IMPORT_LINE + text

    if 'name="export_my_posts"' not in text and "name='export_my_posts'" not in text:
        marker = "urlpatterns = ["
        if marker not in text:
            raise RuntimeError("Ne mogu pronaći 'urlpatterns = [' u blogplatform/urls.py")
        text = text.replace(marker, marker + "\n" + URL_LINE, 1)

    if text != original:
        backup(URLS_PATH, ".bak_before_user_post_export_v2")
        URLS_PATH.write_text(text, encoding="utf-8")
        print("Ažurirano: blogplatform/urls.py")
    else:
        print("blogplatform/urls.py već ima export rutu.")


def update_settings_tab():
    if not SETTINGS_TAB_PATH.exists():
        raise FileNotFoundError(f"Ne postoji: {SETTINGS_TAB_PATH}")

    text = SETTINGS_TAB_PATH.read_text(encoding="utf-8")
    original = text

    if "Izvoz mojih postova" in text:
        print("_settings_tab.html već ima blok za izvoz postova.")
        return

    markers = [
        "Ovdje upravljaš blokiranim i ograničenim korisnicima.",
        "<h5>Sigurnost i privatnost</h5>",
        "Sigurnost i privatnost",
    ]

    for marker in markers:
        if marker in text:
            text = text.replace(marker, marker + EXPORT_BLOCK, 1)
            break
    else:
        raise RuntimeError(
            "Ne mogu pronaći mjesto za ubacivanje u _settings_tab.html. "
            "Treba ručno ubaciti blok u karticu Sigurnost i privatnost."
        )

    if text != original:
        backup(SETTINGS_TAB_PATH, ".bak_before_user_post_export_v2")
        SETTINGS_TAB_PATH.write_text(text, encoding="utf-8")
        print("Ažurirano: blog/templates/blog/settings/_settings_tab.html")


if __name__ == "__main__":
    update_urls()
    update_settings_tab()
    print("Gotovo. Pokreni: python manage.py runserver")
