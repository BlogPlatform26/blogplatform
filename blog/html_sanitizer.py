"""
HTML sanitizer za CKEditor sadržaj.

Cilj:
- dopustiti normalno formatiranje teksta
- maknuti opasne tagove: script, iframe, object, embed...
- maknuti opasne atribute: onclick, onerror, onload...
- dopustiti samo sigurne HTML elemente i atribute

Ako bleach nije instaliran, fallback čuva običan tekst bez HTML-a.
Za puni rad instaliraj:
    python -m pip install bleach
"""

from __future__ import annotations

import re
from typing import Iterable

from django.utils.html import strip_tags


try:
    import bleach
    from bleach.css_sanitizer import CSSSanitizer
except Exception:  # pragma: no cover
    bleach = None
    CSSSanitizer = None


DANGEROUS_BLOCK_TAGS = (
    "script",
    "style",
    "iframe",
    "object",
    "embed",
    "link",
    "meta",
    "form",
    "input",
    "button",
    "textarea",
    "select",
    "option",
    "svg",
    "math",
)


ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "s",
    "blockquote",
    "pre",
    "code",
    "ul",
    "ol",
    "li",
    "h2",
    "h3",
    "h4",
    "hr",
    "a",
    "img",
    "span",
    "div",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
]


ALLOWED_ATTRIBUTES = {
    "*": ["class", "title"],
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan"],
    "p": ["style", "class", "title"],
    "span": ["style", "class", "title"],
    "div": ["style", "class", "title"],
    "table": ["style", "class", "title"],
    "td": ["style", "class", "title", "colspan", "rowspan"],
    "th": ["style", "class", "title", "colspan", "rowspan"],
}


ALLOWED_PROTOCOLS = [
    "http",
    "https",
    "mailto",
]


ALLOWED_CSS_PROPERTIES = [
    "text-align",
    "color",
    "background-color",
    "font-weight",
    "font-style",
    "text-decoration",
    "margin-left",
    "margin-right",
    "width",
    "height",
    "max-width",
]


def _remove_dangerous_blocks(html: str) -> str:
    cleaned = html or ""

    for tag in DANGEROUS_BLOCK_TAGS:
        cleaned = re.sub(
            rf"<\s*{tag}\b[^>]*>.*?<\s*/\s*{tag}\s*>",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
        cleaned = re.sub(
            rf"<\s*{tag}\b[^>]*\/?\s*>",
            "",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )

    return cleaned


def _normalize_links(html: str) -> str:
    if bleach is None:
        return html

    # target="_blank" bez rel može biti sigurnosni problem.
    def add_rel(attrs, new=False):
        href = attrs.get((None, "href"))

        if href:
            target = attrs.get((None, "target"))
            if target == "_blank":
                attrs[(None, "rel")] = "noopener noreferrer"

        return attrs

    return bleach.linkifier.Linker(callbacks=[add_rel]).linkify(html)


def sanitize_post_html(html: str) -> str:
    """
    Sanitizira HTML iz CKEditora prije spremanja u bazu.
    """
    raw_html = _remove_dangerous_blocks(html or "")

    if bleach is None:
        # Siguran fallback: spremi samo običan tekst.
        return strip_tags(raw_html)

    css_sanitizer = None
    if CSSSanitizer is not None:
        css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_CSS_PROPERTIES)

    cleaned = bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
        strip_comments=True,
        css_sanitizer=css_sanitizer,
    )

    cleaned = _normalize_links(cleaned)

    return cleaned.strip()
