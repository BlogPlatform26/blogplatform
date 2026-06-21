import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()

INLINE_IMAGE_PATTERN = re.compile(r"\[slika\s*:\s*(\d+)\]", re.IGNORECASE)


def _get_post_images(post):
    try:
        return list(post.images.all())
    except Exception:
        return []


@register.filter
def has_inline_image_markers(content):
    return bool(INLINE_IMAGE_PATTERN.search(str(content or "")))


@register.filter
def remove_inline_image_markers(content):
    return mark_safe(INLINE_IMAGE_PATTERN.sub("", str(content or "")))


@register.filter
def render_inline_post_images(post):
    content = str(getattr(post, "content", "") or "")
    images = _get_post_images(post)
    title = str(getattr(post, "title", "") or "Slika")

    def replace_marker(match):
        try:
            image_number = int(match.group(1))
        except (TypeError, ValueError):
            return match.group(0)

        image_index = image_number - 1

        if image_index < 0 or image_index >= len(images):
            return match.group(0)

        post_image = images[image_index]

        try:
            image_url = post_image.image.url
        except Exception:
            return ""

        escaped_url = escape(image_url)
        escaped_alt = escape(f"{title} - slika {image_number}")

        return (
            f'<figure class="blog-inline-image">'
            f'<img src="{escaped_url}" alt="{escaped_alt}" loading="lazy">'
            f'<figcaption>Slika {image_number}</figcaption>'
            f'</figure>'
        )

    return mark_safe(INLINE_IMAGE_PATTERN.sub(replace_marker, content))