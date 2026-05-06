from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from blog.models import SecurityEvent


SUSPICIOUS_EVENT_TYPES = {
    "login_failed",
    "login_lockout",
    "registration_blocked",
    "turnstile_failed",
    "activation_failed",
    "resend_email_blocked",
    "password_change_failed",
    "comment_rate_limited",
    "duplicate_comment_blocked",
    "suspicious_access",
}


def _safe_int(value, default, minimum=None, maximum=None):
    try:
        result = int(value)
    except (TypeError, ValueError):
        result = default

    if minimum is not None:
        result = max(minimum, result)
    if maximum is not None:
        result = min(maximum, result)
    return result


@staff_member_required
def security_events_dashboard(request):
    """
    Admin pregled sumnjivih aktivnosti.
    Ovo je pregled za vlasnika/admina, odvojen od standardne Django admin liste.
    """
    days = _safe_int(request.GET.get("days"), 7, minimum=1, maximum=90)
    now = timezone.now()
    since = now - timedelta(days=days)

    base_qs = SecurityEvent.objects.select_related("user").filter(created_at__gte=since)

    selected_event_type = (request.GET.get("event_type") or "").strip()
    selected_severity = (request.GET.get("severity") or "").strip()
    search_query = (request.GET.get("q") or "").strip()
    selected_ip = (request.GET.get("ip") or "").strip()

    filtered_qs = base_qs

    if selected_event_type:
        filtered_qs = filtered_qs.filter(event_type=selected_event_type)

    if selected_severity:
        filtered_qs = filtered_qs.filter(severity=selected_severity)

    if selected_ip:
        filtered_qs = filtered_qs.filter(ip_address=selected_ip)

    if search_query:
        filtered_qs = filtered_qs.filter(
            Q(username__icontains=search_query)
            | Q(user__username__icontains=search_query)
            | Q(ip_address__icontains=search_query)
            | Q(message__icontains=search_query)
            | Q(path__icontains=search_query)
            | Q(user_agent__icontains=search_query)
        )

    filtered_qs = filtered_qs.order_by("-created_at")

    total_events = base_qs.count()
    warning_events = base_qs.filter(severity="warning").count()
    critical_events = base_qs.filter(severity="critical").count()
    suspicious_events = base_qs.filter(event_type__in=SUSPICIOUS_EVENT_TYPES).count()

    login_failed_count = base_qs.filter(event_type="login_failed").count()
    login_lockout_count = base_qs.filter(event_type="login_lockout").count()
    registration_blocked_count = base_qs.filter(event_type="registration_blocked").count()
    comment_limited_count = base_qs.filter(event_type="comment_rate_limited").count()

    top_ips = (
        base_qs.exclude(ip_address__isnull=True)
        .exclude(ip_address="")
        .values("ip_address")
        .annotate(
            total=Count("id"),
            warnings=Count("id", filter=Q(severity="warning")),
            critical=Count("id", filter=Q(severity="critical")),
            failed_logins=Count("id", filter=Q(event_type="login_failed")),
            lockouts=Count("id", filter=Q(event_type="login_lockout")),
        )
        .order_by("-critical", "-warnings", "-total")[:10]
    )

    top_usernames = (
        base_qs.exclude(username="")
        .values("username")
        .annotate(
            total=Count("id"),
            warnings=Count("id", filter=Q(severity="warning")),
            critical=Count("id", filter=Q(severity="critical")),
            failed_logins=Count("id", filter=Q(event_type="login_failed")),
        )
        .order_by("-critical", "-warnings", "-total")[:10]
    )

    event_type_counts = (
        base_qs.values("event_type")
        .annotate(total=Count("id"))
        .order_by("-total")[:12]
    )

    severity_counts = {
        row["severity"]: row["total"]
        for row in base_qs.values("severity").annotate(total=Count("id"))
    }

    paginator = Paginator(filtered_qs, 50)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "title": "Sigurnosni pregled",
        "days": days,
        "since": since,
        "total_events": total_events,
        "warning_events": warning_events,
        "critical_events": critical_events,
        "suspicious_events": suspicious_events,
        "login_failed_count": login_failed_count,
        "login_lockout_count": login_lockout_count,
        "registration_blocked_count": registration_blocked_count,
        "comment_limited_count": comment_limited_count,
        "top_ips": top_ips,
        "top_usernames": top_usernames,
        "event_type_counts": event_type_counts,
        "severity_counts": severity_counts,
        "page_obj": page_obj,
        "event_type_choices": SecurityEvent.EVENT_TYPE_CHOICES,
        "severity_choices": SecurityEvent.SEVERITY_CHOICES,
        "selected_event_type": selected_event_type,
        "selected_severity": selected_severity,
        "selected_ip": selected_ip,
        "search_query": search_query,
    }
    return render(request, "admin/security_events_dashboard.html", context)
