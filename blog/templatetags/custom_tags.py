from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()

MONTHS_HR = {
    1: "siječanj",
    2: "veljača",
    3: "ožujak",
    4: "travanj",
    5: "svibanj",
    6: "lipanj",
    7: "srpanj",
    8: "kolovoz",
    9: "rujan",
    10: "listopad",
    11: "studeni",
    12: "prosinac",
}


def _is_premium_user(user):
    try:
        return bool(user.profile.has_active_premium)
    except Exception:
        return False


def _premium_crown_html():
    return (
        '<span class="premium-crown-icon" aria-label="Premium" title="Premium">'
        '<svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true" focusable="false">'
        '<path d="M3 18h18v2H3v-2Zm1.2-2.2L3 7l5.2 3.6L12 4l3.8 6.6L21 7l-1.2 8.8H4.2Z"/>'
        '</svg>'
        '</span>'
    )


@register.filter
def premium_name(user):
    username = getattr(user, "username", "")
    if _is_premium_user(user):
        return mark_safe(
            f'<span class="premium-name-wrap">'
            f'<span class="premium-username">{username}</span>'
            f'{_premium_crown_html()}'
            f'</span>'
        )
    return username


@register.filter
def user_link(user):
    url = reverse('user_blog', args=[user.username])
    if _is_premium_user(user):
        return mark_safe(
            f'<a href="{url}" class="premium-user-link">'
            f'<span class="premium-name-wrap">'
            f'<span class="premium-username">{user.username}</span>'
            f'{_premium_crown_html()}'
            f'</span>'
            f'</a>'
        )
    return mark_safe(f'<a href="{url}" style="text-decoration:none;">{user.username}</a>')


@register.filter
def blog_link(user):
    url = reverse('user_blog', args=[user.username])
    return mark_safe(
        f'<a href="{url}" class="blog-link">{user.profile.blog_name}</a>'
    )


@register.filter
def month_hr(value):
    """
    Prima date/datetime ili broj mjeseca (1-12) i vraća naziv na hrvatskom.
    """
    month_num = None

    # date/datetime
    if hasattr(value, "month"):
        month_num = value.month
    else:
        # int ili string
        try:
            month_num = int(value)
        except:
            month_num = None

    if not month_num:
        return ""

    return MONTHS_HR.get(month_num, "")


@register.filter
def get_item(d, key):
    """
    Omogućuje: {{ some_dict|get_item:some_key }}
    """
    if d is None:
        return None
    return d.get(key)


@register.filter
def comment_words(value):
    import re
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    if value is None:
        return ""

    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\xa0", " ")

    # Ako je u tekstu slučajno ostao HTML iz starih pokušaja, makni ga.
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)

    # Makni umjetne prijelome reda.
    # Cilj je da komentar bude običan tekst koji browser sam prelama.
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    words = text.split(" ")

    html_words = []
    for word in words:
        safe_word = escape(word)
        html_words.append(f'<span class="bp-comment-word">{safe_word}</span>')

    return mark_safe(" ".join(html_words))

# BLOGPLATFORM_LIKED_BY_FILTER_START
@register.filter
def liked_by(post, user):
    """
    Pouzdana provjera lajka za template.
    Ako view već ima post.user_liked, koristi to.
    Ako nema, provjeri bazu.
    """
    if not getattr(user, "is_authenticated", False):
        return False

    cached_value = getattr(post, "user_liked", None)

    if isinstance(cached_value, bool):
        return cached_value

    try:
        return post.likes.filter(user=user).exists()
    except Exception:
        return False
# BLOGPLATFORM_LIKED_BY_FILTER_END

# BLOGPLATFORM_MENTION_LINKS_START
@register.filter
def link_mentions(value):
    import re
    from django.contrib.auth.models import User
    from django.urls import reverse
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    if value is None:
        return ""

    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\xa0", " ")
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    html_parts = []

    for token in text.split(" "):
        match = re.match(r"^@([A-Za-z0-9_.+-]{2,150})([.,!?;:]*)$", token)

        if match:
            typed_username = match.group(1)
            punctuation = match.group(2) or ""

            user = User.objects.filter(username__iexact=typed_username, is_active=True).first()

            if user:
                url = reverse("user_blog", args=[user.username])
                html_parts.append(
                    f'<a class="bp-mention-link bp-comment-word" href="{escape(url)}">'
                    f'@{escape(user.username)}'
                    f'</a>{escape(punctuation)}'
                )
                continue

        html_parts.append(f'<span class="bp-comment-word">{escape(token)}</span>')

    return mark_safe(" ".join(html_parts))


@register.filter
def notification_url(notification):
    from django.urls import reverse

    if getattr(notification, "notification_type", "") == "follow" and getattr(notification, "sender_id", None):
        return reverse("user_blog", args=[notification.sender.username])

    if getattr(notification, "post_id", None):
        url = reverse("post_detail", args=[notification.post.id])

        if getattr(notification, "comment_id", None):
            url += f"#comment-{notification.comment.id}"

        return url

    return reverse("notifications")


@register.filter
def notification_message(notification):
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    sender = getattr(notification, "sender", None)
    sender_name = escape(getattr(sender, "username", "Korisnik"))

    post = getattr(notification, "post", None)
    post_title = escape(getattr(post, "title", "")) if post else ""

    notification_type = getattr(notification, "notification_type", "")

    if notification_type == "follow":
        return mark_safe(f'<strong>{sender_name}</strong> vas je zapratio.')

    if notification_type == "like":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> je lajkao vaš post <strong>"{post_title}"</strong>.')
        return mark_safe(f'<strong>{sender_name}</strong> je lajkao vaš post.')

    if notification_type == "comment":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> je komentirao vaš post <strong>"{post_title}"</strong>.')
        return mark_safe(f'<strong>{sender_name}</strong> je komentirao vaš post.')

    if notification_type == "mention":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> vas je označio/la u komentaru na postu <strong>"{post_title}"</strong>.')
        return mark_safe(f'<strong>{sender_name}</strong> vas je označio/la u komentaru.')

    return mark_safe("Nova obavijest.")
# BLOGPLATFORM_MENTION_LINKS_END

# BLOGPLATFORM_NOTIFICATION_DROPDOWN_START
@register.filter
def bp_notification_icon(notification):
    notification_type = getattr(notification, "notification_type", "")

    if notification_type == "like":
        return "bi bi-heart"
    if notification_type == "comment":
        return "bi bi-chat-left-text"
    if notification_type == "follow":
        return "bi bi-person-plus"
    if notification_type == "mention":
        return "bi bi-at"

    return "bi bi-bell"


@register.filter
def bp_notification_message(notification):
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    sender = getattr(notification, "sender", None)
    sender_name = escape(getattr(sender, "username", "Korisnik"))

    post = getattr(notification, "post", None)
    post_title = escape(getattr(post, "title", "")) if post else ""

    notification_type = getattr(notification, "notification_type", "")

    if notification_type == "like":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> je lajkao vaš post <strong>"{post_title}"</strong>')
        return mark_safe(f'<strong>{sender_name}</strong> je lajkao vaš post')

    if notification_type == "comment":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> je komentirao vaš post <strong>"{post_title}"</strong>')
        return mark_safe(f'<strong>{sender_name}</strong> je komentirao vaš post')

    if notification_type == "follow":
        return mark_safe(f'<strong>{sender_name}</strong> vas je zapratio.')

    if notification_type == "mention":
        if post_title:
            return mark_safe(f'<strong>{sender_name}</strong> vas je označio/la u komentaru na postu <strong>"{post_title}"</strong>')
        return mark_safe(f'<strong>{sender_name}</strong> vas je označio/la u komentaru')

    return mark_safe("Nova obavijest")
# BLOGPLATFORM_NOTIFICATION_DROPDOWN_END
