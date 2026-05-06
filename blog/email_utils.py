from html import escape

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone


def _get_site_url(request=None):
    site_url = getattr(settings, "SITE_URL", "") or ""

    if site_url:
        return site_url.rstrip("/")

    if request is not None:
        return f"{request.scheme}://{request.get_host()}".rstrip("/")

    return ""


def _get_logo_url(request=None):
    """
    Gmail potpis iz Gmail postavki se ne dodaje automatski na Django SMTP emailove.
    Zato platforma ima vlastiti email footer/signature.

    Za logo u mailu možeš kasnije u .env dodati:
    EMAIL_LOGO_URL=https://tvoja-domena.hr/static/images/logo.png
    """
    logo_url = getattr(settings, "EMAIL_LOGO_URL", "") or ""

    if logo_url:
        return logo_url

    return ""


def send_platform_email(subject, text_message, recipient_list, html_message=None):
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)

    if not recipient_list:
        return 0

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=from_email,
        to=recipient_list,
    )

    if html_message:
        msg.attach_alternative(html_message, "text/html")

    return msg.send(fail_silently=False)


def send_security_notification_email(
    user,
    subject,
    title,
    message,
    request=None,
    recipient_email=None,
    event_label="Sigurnosna obavijest",
):
    email = recipient_email or getattr(user, "email", "")

    if not email:
        return 0

    username = getattr(user, "username", "") or "korisniče"
    site_url = _get_site_url(request)
    logo_url = _get_logo_url(request)

    ip_address = "nepoznato"
    if request is not None:
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            ip_address = forwarded_for.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR", "nepoznato")

    time_label = timezone.localtime(timezone.now()).strftime("%d.%m.%Y. %H:%M")

    text_message = (
        f"Pozdrav {username},\n\n"
        f"{message}\n\n"
        f"Događaj: {event_label}\n"
        f"Vrijeme: {time_label}\n"
        f"IP adresa: {ip_address}\n\n"
        "Ako ovo niste bili vi, promijenite lozinku i kontaktirajte podršku.\n\n"
        "BlogPlatform"
    )

    escaped_message = escape(message)
    escaped_username = escape(username)
    escaped_event = escape(event_label)
    escaped_ip = escape(ip_address)

    logo_html = ""
    if logo_url:
        logo_html = f"""
            <div style="margin-bottom:16px;">
                <img src="{escape(logo_url)}" alt="BlogPlatform" style="max-width:180px;height:auto;">
            </div>
        """

    button_html = ""
    if site_url:
        button_html = f"""
            <p style="margin:24px 0;">
                <a href="{escape(site_url)}"
                   style="background:#2f6f88;color:#ffffff;text-decoration:none;padding:10px 16px;border-radius:8px;display:inline-block;">
                    Otvori BlogPlatform
                </a>
            </p>
        """

    html_message = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;background:#f5f6fa;padding:24px;color:#1f2937;">
        <div style="max-width:640px;margin:0 auto;background:#ffffff;border-radius:14px;padding:28px;border:1px solid #e5e7eb;">
            {logo_html}
            <h2 style="margin-top:0;color:#1f2937;">{escape(title)}</h2>
            <p>Pozdrav <strong>{escaped_username}</strong>,</p>
            <p style="line-height:1.6;">{escaped_message}</p>

            <div style="margin:20px 0;padding:14px 16px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;">
                <div><strong>Događaj:</strong> {escaped_event}</div>
                <div><strong>Vrijeme:</strong> {escape(time_label)}</div>
                <div><strong>IP adresa:</strong> {escaped_ip}</div>
            </div>

            {button_html}

            <p style="line-height:1.6;">
                Ako ovo niste bili vi, odmah promijenite lozinku i kontaktirajte podršku.
            </p>

            <hr style="border:none;border-top:1px solid #e5e7eb;margin:24px 0;">
            <p style="font-size:13px;color:#6b7280;margin:0;">
                BlogPlatform sigurnosna obavijest
            </p>
        </div>
    </div>
    """

    return send_platform_email(
        subject=subject,
        text_message=text_message,
        html_message=html_message,
        recipient_list=[email],
    )
