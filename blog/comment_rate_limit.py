import hashlib
import os
import time

from django.conf import settings
from django.core.cache import cache


def _env_int(name, default):
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _setting_int(name, default):
    return int(getattr(settings, name, _env_int(name, default)))


def _env_list_int(name, default):
    value = os.environ.get(name)
    if value is None or value == "":
        return default

    result = []
    for part in str(value).split(","):
        part = part.strip()
        if not part:
            continue
        try:
            result.append(int(part))
        except (TypeError, ValueError):
            return default

    return result or default


def _setting_list_int(name, default):
    value = getattr(settings, name, None)
    if value is None or value == "":
        return _env_list_int(name, default)

    if isinstance(value, (list, tuple)):
        try:
            parsed = [int(v) for v in value]
            return parsed or default
        except (TypeError, ValueError):
            return default

    if isinstance(value, str):
        result = []
        for part in value.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                result.append(int(part))
            except (TypeError, ValueError):
                return default
        return result or default

    return default


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def format_seconds_as_minutes(seconds):
    seconds = int(seconds)

    if seconds < 3600:
        minutes = max(1, int((seconds + 59) // 60))
        if minutes == 1:
            return "1 minutu"
        return f"{minutes} minuta"

    if seconds < 86400:
        hours = max(1, int((seconds + 3599) // 3600))
        if hours == 1:
            return "1 sat"
        if hours in (2, 3, 4):
            return f"{hours} sata"
        return f"{hours} sati"

    days = max(1, int((seconds + 86399) // 86400))
    if days == 1:
        return "1 dan"
    return f"{days} dana"


def _comment_actor_key(request):
    if request.user.is_authenticated:
        return f"user:{request.user.id}"
    return f"ip:{get_client_ip(request)}"


def _comment_rate_cache_keys(request):
    raw_key = _comment_actor_key(request)
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    return {
        "attempts": f"comment_attempts:{key_hash}",
        "lock": f"comment_lock:{key_hash}",
        "violations": f"comment_violations:{key_hash}",
    }


def _get_comment_lock_seconds_left(request):
    keys = _comment_rate_cache_keys(request)
    lock_until = cache.get(keys["lock"])

    if not lock_until:
        return 0

    now = int(time.time())

    try:
        lock_until = int(lock_until)
    except (TypeError, ValueError):
        cache.delete(keys["lock"])
        return 0

    seconds_left = lock_until - now

    if seconds_left <= 0:
        cache.delete(keys["lock"])
        cache.delete(keys["attempts"])
        return 0

    return seconds_left


def _get_escalated_lockout_seconds(request):
    keys = _comment_rate_cache_keys(request)

    default_levels = [
        300,       # 5 minuta
        1800,      # 30 minuta
        7200,      # 2 sata
        86400,     # 1 dan
        259200,    # 3 dana
        604800,    # 7 dana
    ]

    levels = _setting_list_int("COMMENT_LOCKOUT_LEVEL_SECONDS", default_levels)
    reset_seconds = _setting_int("COMMENT_VIOLATION_RESET_SECONDS", 604800)

    try:
        violations = int(cache.get(keys["violations"]) or 0)
    except (TypeError, ValueError):
        violations = 0

    violations += 1

    # Ako korisnik nema novi spam prekršaj kroz reset_seconds, brojač se sam briše.
    cache.set(keys["violations"], violations, timeout=reset_seconds)

    index = min(violations - 1, len(levels) - 1)
    return int(levels[index]), violations


def _register_comment_attempt(request):
    keys = _comment_rate_cache_keys(request)

    max_attempts = _setting_int("COMMENT_MAX_ATTEMPTS", 5)
    window_seconds = _setting_int("COMMENT_RATE_LIMIT_WINDOW_SECONDS", 60)

    try:
        attempts = int(cache.get(keys["attempts"]) or 0)
    except (TypeError, ValueError):
        attempts = 0

    attempts += 1
    cache.set(keys["attempts"], attempts, timeout=window_seconds)

    if attempts > max_attempts:
        lockout_seconds, violations = _get_escalated_lockout_seconds(request)
        lock_until = int(time.time()) + lockout_seconds

        cache.set(keys["lock"], lock_until, timeout=lockout_seconds)
        cache.delete(keys["attempts"])

        return (
            False,
            f"Previše komentara u kratkom vremenu. Ovo je {violations}. prekršaj. "
            f"Pokušaj ponovno za {format_seconds_as_minutes(lockout_seconds)}."
        )

    return True, ""


def _duplicate_comment_cache_key(request, post, content):
    normalized_content = " ".join((content or "").split()).strip().lower()
    actor = _comment_actor_key(request)
    raw_key = f"{actor}:post:{post.id}:content:{normalized_content}"
    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    return f"duplicate_comment:{key_hash}"


def check_comment_allowed(request, post, content):
    """
    Vraća tuple: (allowed, error_message).
    Pozovi prije spremanja komentara.
    """
    seconds_left = _get_comment_lock_seconds_left(request)
    if seconds_left > 0:
        return False, f"Previše komentara u kratkom vremenu. Pokušaj ponovno za {format_seconds_as_minutes(seconds_left)}."

    ok, error_message = _register_comment_attempt(request)
    if not ok:
        return False, error_message

    duplicate_key = _duplicate_comment_cache_key(request, post, content)
    if cache.get(duplicate_key):
        return False, "Isti komentar je već poslan. Pričekaj malo prije ponovnog slanja."

    return True, ""


def remember_comment_sent(request, post, content):
    duplicate_window_seconds = _setting_int("COMMENT_DUPLICATE_WINDOW_SECONDS", 120)
    duplicate_key = _duplicate_comment_cache_key(request, post, content)
    cache.set(duplicate_key, True, timeout=duplicate_window_seconds)
