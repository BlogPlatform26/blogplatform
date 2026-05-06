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
