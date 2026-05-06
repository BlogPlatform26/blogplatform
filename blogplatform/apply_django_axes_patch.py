
"""
Sigurni patch za dodavanje django-axes u postojeći projekt.

Pokreni iz glavnog foldera projekta, tamo gdje je manage.py:

    python apply_django_axes_patch.py

Skripta NE mijenja tvoje tajne podatke i NE zamjenjuje cijeli settings.py.
Samo doda potrebne django-axes stavke ako ih već nema.
"""

from pathlib import Path
import re


PROJECT_ROOT = Path.cwd()
SETTINGS_PATH = PROJECT_ROOT / "blogplatform" / "settings.py"
ADMIN_PATH = PROJECT_ROOT / "blog" / "admin.py"


def read_text(path):
    return path.read_text(encoding="utf-8")


def write_text(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def make_backup(path):
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")


def add_datetime_import(settings_text):
    if "from datetime import timedelta" in settings_text:
        return settings_text

    if re.search(r"^import os\s*$", settings_text, flags=re.MULTILINE):
        return re.sub(
            r"^import os\s*$",
            "import os\nfrom datetime import timedelta",
            settings_text,
            count=1,
            flags=re.MULTILINE,
        )

    return "from datetime import timedelta\n" + settings_text


def add_to_list_setting(settings_text, setting_name, item, after_item=None, append_last=False):
    pattern = rf"({setting_name}\s*=\s*\[)(.*?)(\n\])"
    match = re.search(pattern, settings_text, flags=re.S)

    if not match:
        return settings_text

    list_body = match.group(2)

    if item in list_body:
        return settings_text

    item_line = f"\n    '{item}',"

    if append_last:
        new_body = list_body.rstrip() + item_line
    elif after_item and after_item in list_body:
        new_body = list_body.replace(
            f"'{after_item}',",
            f"'{after_item}',{item_line}",
            1,
        )
    else:
        new_body = item_line + list_body

    return settings_text[:match.start(2)] + new_body + settings_text[match.end(2):]


def add_authentication_backends(settings_text):
    axes_backend = "'axes.backends.AxesStandaloneBackend'"
    model_backend = "'django.contrib.auth.backends.ModelBackend'"

    if re.search(r"AUTHENTICATION_BACKENDS\s*=", settings_text):
        pattern = r"(AUTHENTICATION_BACKENDS\s*=\s*\[)(.*?)(\n\])"
        match = re.search(pattern, settings_text, flags=re.S)

        if not match:
            return settings_text

        body = match.group(2)
        lines_to_add = []

        if axes_backend not in body:
            lines_to_add.append(f"\n    {axes_backend},")
        if model_backend not in body:
            lines_to_add.append(f"\n    {model_backend},")

        if not lines_to_add:
            return settings_text

        new_body = "".join(lines_to_add) + body
        return settings_text[:match.start(2)] + new_body + settings_text[match.end(2):]

    block = """

# ==========================================================
# AUTHENTICATION BACKENDS
# ==========================================================

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]
"""
    return settings_text.rstrip() + block + "\n"


def add_axes_settings(settings_text):
    if "AXES_FAILURE_LIMIT" in settings_text or "# DJANGO-AXES" in settings_text:
        return settings_text

    block = """

# ==========================================================
# DJANGO-AXES
# ==========================================================
# Dodatna zaštita od brute-force login napada.
# Instalacija paketa:
#   python -m pip install "django-axes[ipware]"
#
# Nakon instalacije:
#   python manage.py migrate
#
# Ako ove vrijednosti ne staviš u .env, koriste se default vrijednosti ispod.

AXES_ENABLED = os.getenv("AXES_ENABLED", "True").lower() == "true"
AXES_FAILURE_LIMIT = int(os.getenv("AXES_FAILURE_LIMIT", "5"))
AXES_COOLOFF_TIME = timedelta(minutes=int(os.getenv("AXES_COOLOFF_MINUTES", "10")))
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ADMIN = True
AXES_VERBOSE = True

# Zaključavanje po kombinaciji korisničkog imena/emaila i IP adrese.
# To je opreznije nego blokirati cijeli IP za sve korisnike.
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]

# 429 = Too Many Requests
AXES_HTTP_RESPONSE_CODE = 429
"""
    return settings_text.rstrip() + block + "\n"


def patch_settings():
    if not SETTINGS_PATH.exists():
        raise FileNotFoundError(f"Ne mogu naći settings.py: {SETTINGS_PATH}")

    make_backup(SETTINGS_PATH)
    text = read_text(SETTINGS_PATH)

    text = add_datetime_import(text)
    text = add_to_list_setting(text, "INSTALLED_APPS", "axes", after_item="django.contrib.staticfiles")
    text = add_to_list_setting(text, "MIDDLEWARE", "axes.middleware.AxesMiddleware", append_last=True)
    text = add_authentication_backends(text)
    text = add_axes_settings(text)

    write_text(SETTINGS_PATH, text)


def patch_admin_grouping():
    if not ADMIN_PATH.exists():
        return

    text = read_text(ADMIN_PATH)

    if "ADMIN_MODEL_GROUPS" not in text:
        return

    if '"AccessAttempt"' in text and '"AccessLog"' in text:
        return

    make_backup(ADMIN_PATH)

    if '"SecurityEvent",' in text:
        text = text.replace(
            '"SecurityEvent",',
            '"SecurityEvent",\n            "AccessAttempt",\n            "AccessLog",',
            1,
        )
    else:
        text = text.replace(
            '"models": [',
            '"models": [\n            "AccessAttempt",\n            "AccessLog",',
            1,
        )

    write_text(ADMIN_PATH, text)


def patch_env_example():
    env_example = PROJECT_ROOT / ".env.example"
    if not env_example.exists():
        return

    text = read_text(env_example)

    if "AXES_FAILURE_LIMIT" in text:
        return

    make_backup(env_example)

    block = """

# ==========================================================
# DJANGO-AXES
# ==========================================================

AXES_ENABLED=True
AXES_FAILURE_LIMIT=5
AXES_COOLOFF_MINUTES=10
"""
    write_text(env_example, text.rstrip() + block + "\n")


def main():
    patch_settings()
    patch_admin_grouping()
    patch_env_example()

    print("django-axes patch je dodan.")
    print("")
    print("Sada pokreni:")
    print('python -m pip install "django-axes[ipware]"')
    print("python manage.py migrate")
    print("python manage.py check")
    print("python manage.py runserver")
    print("")
    print("Ako se želiš vratiti nazad, napravljeni su .bak backupi za promijenjene datoteke.")


if __name__ == "__main__":
    main()
