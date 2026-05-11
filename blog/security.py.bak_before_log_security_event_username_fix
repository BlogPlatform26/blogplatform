from django.db import DatabaseError

from blog.models import SecurityEvent


def get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR") if request else None
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") if request else ""


def get_user_agent(request):
    if not request:
        return ""
    return (request.META.get("HTTP_USER_AGENT", "") or "")[:255]


def log_security_event(request=None, event_type="suspicious_access", user=None, severity="info", message="", metadata=None):
    """
    Spremi sigurnosni događaj.
    Funkcija namjerno ne ruši aplikaciju ako logiranje ne uspije.
    """
    try:
        request_user = getattr(request, "user", None) if request else None
        if user is None and getattr(request_user, "is_authenticated", False):
            user = request_user

        username = ""
        if user is not None:
            username = getattr(user, "username", "") or ""
        elif metadata and metadata.get("username"):
            username = str(metadata.get("username"))[:150]
        elif metadata and metadata.get("login_identifier"):
            username = str(metadata.get("login_identifier"))[:150]

        SecurityEvent.objects.create(
            user=user if getattr(user, "is_authenticated", True) else None,
            username=username,
            event_type=event_type,
            severity=severity,
            ip_address=get_client_ip(request) or None,
            user_agent=get_user_agent(request),
            path=(getattr(request, "path", "") or "")[:255] if request else "",
            method=(getattr(request, "method", "") or "")[:10] if request else "",
            message=message or "",
            metadata=metadata or {},
        )
    except (DatabaseError, Exception):
        # Sigurnosni log ne smije srušiti login, registraciju ili komentare.
        return None
