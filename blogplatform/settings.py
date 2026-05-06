"""
Django settings for blogplatform project.

Ova verzija čita tajne podatke iz .env datoteke ili iz environment varijabli.
Prije online objave obavezno postavi DEBUG=False i popuni prave vrijednosti u .env.
"""

from pathlib import Path
import os
from datetime import timedelta
from django.utils.csp import CSP
# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# .env LOADER
# ==========================================================
# Ovo je jednostavan loader da ne moraš odmah instalirati dodatne pakete.
# U root projekta stavi .env datoteku:
# blogplatform/.env

def load_env_file(path):
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        # Ne pregazi vrijednost ako je već postavljena na serveru.
        os.environ.setdefault(key, value)


load_env_file(BASE_DIR / ".env")


def env_bool(name, default=False):
    value = os.environ.get(name)

    if value is None:
        return default

    return value.strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    value = os.environ.get(name, default)

    if not value:
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def env_int(name, default):
    value = os.environ.get(name)

    if value is None or value == "":
        return default

    try:
        return int(value)
    except ValueError:
        return default


# ==========================================================
# BASIC SECURITY
# ==========================================================

DEBUG = env_bool("DEBUG", default=True)

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        # Samo za lokalni razvoj ako još nisi napravio .env.
        # Za produkciju ovo se NE SMIJE koristiti.
        SECRET_KEY = "django-insecure-local-development-key-change-me"
    else:
        raise RuntimeError("SECRET_KEY nije postavljen. Dodaj SECRET_KEY u .env ili environment varijable.")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", default="127.0.0.1,localhost")

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")


# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",

    "blog",
    "ckeditor",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]


ROOT_URLCONF = "blogplatform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "blog.context_processors.notifications_data",
            ],
        },
    },
]

WSGI_APPLICATION = "blogplatform.wsgi.application"


# ==========================================================
# DATABASE
# ==========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.environ.get("SQLITE_DB_NAME", "db.sqlite3"),
    }
}


# ==========================================================
# PASSWORD HASHING / VALIDATION
# ==========================================================

# Argon2 je jači algoritam za spremanje lozinki.
# Potrebno je instalirati paket: pip install argon2-cffi
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

PASSWORD_MIN_LENGTH = env_int("PASSWORD_MIN_LENGTH", 10)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": PASSWORD_MIN_LENGTH,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==========================================================
# CKEDITOR
# ==========================================================

CKEDITOR_CONFIGS = {
    "minimal": {
        "toolbar": [
            ["Font", "FontSize"],
            ["Bold", "Italic", "Underline"],
            ["Link", "Unlink"],
            ["NumberedList", "BulletedList"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["RemoveFormat"],
        ],
        "height": 250,
        "width": "100%",
    }
}


# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "hr"

TIME_ZONE = "Europe/Zagreb"

USE_I18N = True

USE_TZ = True


# ==========================================================
# LOGIN / LOGOUT
# ==========================================================

LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"

PASSWORD_RESET_TIMEOUT = env_int("PASSWORD_RESET_TIMEOUT", 3600)

# Zaštita login forme od brute-force pokušaja.
# Zadano: 5 krivih pokušaja u 10 minuta, zatim blokada 10 minuta.
LOGIN_MAX_ATTEMPTS = env_int("LOGIN_MAX_ATTEMPTS", 5)
LOGIN_RATE_LIMIT_WINDOW_SECONDS = env_int("LOGIN_RATE_LIMIT_WINDOW_SECONDS", 600)
LOGIN_LOCKOUT_SECONDS = env_int("LOGIN_LOCKOUT_SECONDS", 600)

# Ograničenje registracije protiv spama/botova.
# Zadano: 5 pokušaja registracije u 1 sat, zatim blokada 1 sat.
REGISTRATION_MAX_ATTEMPTS = env_int("REGISTRATION_MAX_ATTEMPTS", 5)
REGISTRATION_RATE_LIMIT_WINDOW_SECONDS = env_int("REGISTRATION_RATE_LIMIT_WINDOW_SECONDS", 3600)
REGISTRATION_LOCKOUT_SECONDS = env_int("REGISTRATION_LOCKOUT_SECONDS", 3600)

# Ograničenje ponovnog slanja aktivacijskog/potvrdnog emaila.
# Zadano: 3 ponovna slanja u 15 minuta, zatim blokada 15 minuta.
RESEND_EMAIL_MAX_ATTEMPTS = env_int("RESEND_EMAIL_MAX_ATTEMPTS", 3)
RESEND_EMAIL_RATE_LIMIT_WINDOW_SECONDS = env_int("RESEND_EMAIL_RATE_LIMIT_WINDOW_SECONDS", 900)
RESEND_EMAIL_LOCKOUT_SECONDS = env_int("RESEND_EMAIL_LOCKOUT_SECONDS", 900)

# Ograničenje komentara protiv spama.
# Zadano: 5 komentara u 1 minutu, zatim blokada 5 minuta.
COMMENT_MAX_ATTEMPTS = env_int("COMMENT_MAX_ATTEMPTS", 5)
COMMENT_RATE_LIMIT_WINDOW_SECONDS = env_int("COMMENT_RATE_LIMIT_WINDOW_SECONDS", 60)
COMMENT_LOCKOUT_SECONDS = env_int("COMMENT_LOCKOUT_SECONDS", 300)
COMMENT_DUPLICATE_WINDOW_SECONDS = env_int("COMMENT_DUPLICATE_WINDOW_SECONDS", 120)
COMMENT_LOCKOUT_LEVEL_SECONDS = os.environ.get(
    "COMMENT_LOCKOUT_LEVEL_SECONDS",
    "300,1800,7200,86400,259200,604800",
)
COMMENT_VIOLATION_RESET_SECONDS = env_int("COMMENT_VIOLATION_RESET_SECONDS", 604800)

# Cloudflare Turnstile za zaštitu registracije od botova.
# Lokalno može ostati False. U produkciji stavi True i popuni ključeve.
TURNSTILE_ENABLED = env_bool("TURNSTILE_ENABLED", False)
TURNSTILE_SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY", "")
TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "")


# ==========================================================
# EMAIL
# ==========================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = env_int("EMAIL_PORT", 587)
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", default=True)

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

EMAIL_TIMEOUT = env_int("EMAIL_TIMEOUT", 30)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER or "webmaster@localhost",
)

SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

BUG_REPORT_EMAIL = os.environ.get(
    "BUG_REPORT_EMAIL",
    DEFAULT_FROM_EMAIL,
)


# ==========================================================
# STATIC / MEDIA
# ==========================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==========================================================
# UPLOAD LIMITS
# ==========================================================
# Ovo ne mijenja tvoj validator od 2 MB za slike, nego dodatno štiti zahtjeve.

DATA_UPLOAD_MAX_MEMORY_SIZE = env_int("DATA_UPLOAD_MAX_MEMORY_SIZE", 5 * 1024 * 1024)
FILE_UPLOAD_MAX_MEMORY_SIZE = env_int("FILE_UPLOAD_MAX_MEMORY_SIZE", 5 * 1024 * 1024)


# ==========================================================
# SECURITY SETTINGS
# ==========================================================

IS_PRODUCTION = not DEBUG

# Cookie zaštita
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
CSRF_COOKIE_SAMESITE = os.environ.get("CSRF_COOKIE_SAMESITE", "Lax")

# JavaScriptu obično ne treba čitati CSRF cookie jer koristiš Django forme.
# Ako kasnije radiš fetch/AJAX, ovo možda treba prilagoditi.
CSRF_COOKIE_HTTPONLY = env_bool("CSRF_COOKIE_HTTPONLY", default=False)

# Header zaštita
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = os.environ.get(
    "SECURE_REFERRER_POLICY",
    "strict-origin-when-cross-origin",
)

X_FRAME_OPTIONS = os.environ.get(
    "X_FRAME_OPTIONS",
    "DENY" if IS_PRODUCTION else "SAMEORIGIN",
)

# HTTPS produkcijske postavke
if IS_PRODUCTION:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", default=True)

    SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", default=True)

    # Uključi samo ako hosting/proxy šalje X-Forwarded-Proto header.
    if env_bool("USE_X_FORWARDED_PROTO", default=False):
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    SECURE_SSL_REDIRECT = False

    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False


# ==========================================================
# DEFAULTS
# ==========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================================
# AUTHENTICATION BACKENDS
# ==========================================================

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# ==========================================================
# CONTENT SECURITY POLICY / CSP
# ==========================================================
# CSP je zaštitni HTTP header koji ograničava odakle se smiju učitavati
# skripte, stilovi, slike, fontovi, frameovi i ostali resursi.
#
# Za sada je default REPORT-ONLY da ne razbije stranicu dok testiraš.
# Kad u browser konzoli više nema bitnih CSP upozorenja, u .env možeš staviti:
# CSP_REPORT_ONLY=False

CSP_REPORT_ONLY = env_bool("CSP_REPORT_ONLY", default=True)

BLOGPLATFORM_CSP = {
    "default-src": [CSP.SELF],

    # Projekt trenutno ima dosta inline JS/CSS u templateovima, zato je unsafe-inline
    # privremeno dopušten. Kasnije možemo ići na nonce i maknuti unsafe-inline.
    "script-src": [
        CSP.SELF,
        CSP.UNSAFE_INLINE,
        "https://cdn.jsdelivr.net",
        "https://unpkg.com",
        "https://cdnjs.cloudflare.com",
        "https://challenges.cloudflare.com",
        "https://www.youtube.com",
        "https://www.youtube-nocookie.com",
    ],
    "script-src-elem": [
        CSP.SELF,
        CSP.UNSAFE_INLINE,
        "https://cdn.jsdelivr.net",
        "https://unpkg.com",
        "https://cdnjs.cloudflare.com",
        "https://challenges.cloudflare.com",
        "https://www.youtube.com",
        "https://www.youtube-nocookie.com",
    ],
    "style-src": [
        CSP.SELF,
        CSP.UNSAFE_INLINE,
        "https://cdn.jsdelivr.net",
        "https://unpkg.com",
        "https://cdnjs.cloudflare.com",
        "https://fonts.googleapis.com",
        "https://cdn.cursors-4u.net",
    ],
    "style-src-elem": [
        CSP.SELF,
        CSP.UNSAFE_INLINE,
        "https://cdn.jsdelivr.net",
        "https://unpkg.com",
        "https://cdnjs.cloudflare.com",
        "https://fonts.googleapis.com",
        "https://cdn.cursors-4u.net",
    ],
    "style-src-attr": [
        CSP.SELF,
        CSP.UNSAFE_INLINE,
    ],
    "img-src": [
        CSP.SELF,
        "data:",
        "blob:",
        "https:",
        "https://cdn.cursors-4u.net",
        "https://server.arcgisonline.com",
    ],
    "font-src": [
        CSP.SELF,
        "data:",
        "https://cdn.jsdelivr.net",
        "https://cdnjs.cloudflare.com",
        "https://fonts.gstatic.com",
    ],
    "media-src": [
        CSP.SELF,
        "data:",
        "blob:",
        "https:",
    ],
    "connect-src": [
        CSP.SELF,
        "https://challenges.cloudflare.com",
        "https://server.arcgisonline.com",
    ],
    "frame-src": [
        CSP.SELF,
        "https://challenges.cloudflare.com",
        "https://www.youtube.com",
        "https://www.youtube-nocookie.com",
    ],
    "object-src": [CSP.NONE],
    "base-uri": [CSP.SELF],
    "form-action": [CSP.SELF],
    "frame-ancestors": [CSP.SELF],
}

if CSP_REPORT_ONLY:
    SECURE_CSP_REPORT_ONLY = BLOGPLATFORM_CSP
else:
    SECURE_CSP = BLOGPLATFORM_CSP


# ==========================================================
# DJANGO-AXES
# ==========================================================
# Dodatna zaštita od brute-force login napada.
# Paket:
#   python -m pip install "django-axes[ipware]"
#
# Nakon instalacije:
#   python manage.py migrate

AXES_ENABLED = env_bool("AXES_ENABLED", default=True)
AXES_FAILURE_LIMIT = env_int("AXES_FAILURE_LIMIT", 5)
AXES_COOLOFF_TIME = timedelta(minutes=env_int("AXES_COOLOFF_MINUTES", 10))
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ADMIN = True
AXES_VERBOSE = True

# Zaključavanje po kombinaciji korisničkog imena/emaila i IP adrese.
# To je opreznije nego blokirati cijeli IP za sve korisnike.
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]

# 429 = Too Many Requests
AXES_HTTP_RESPONSE_CODE = 429

