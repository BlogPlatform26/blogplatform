"""
HTML sanitizer za CKEditor sadržaj.

Cilj:
- dopustiti normalno formatiranje teksta iz CKEditora
- maknuti opasne tagove: script, iframe, object, embed...
- maknuti opasne atribute: onclick, onerror, onload...
- dopustiti samo sigurne HTML elemente i atribute

Napomena:
- Ako je instaliran samo bleach, čuvamo HTML tagove kao strong, em, ul, li, a...
- Ako je instaliran i tinycss2, čuvamo i sigurne style atribute kao text-align, color, font-size...
- Ako bleach nije instaliran, fallback sprema običan tekst bez HTML-a.

Preporučeno:
python -m pip install bleach tinycss2
"""

from __future__ import annotations

import re
from typing import Dict, List

from django.utils.html import strip_tags

try:
    import bleach
except Exception:  # pragma: no cover
    bleach = None

try:
    from bleach.css_sanitizer import CSSSanitizer
except Exception:  # pragma: no cover
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
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
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

BASE_ALLOWED_ATTRIBUTES = {
    "*": ["class", "title"],
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan"],
}

STYLE_ALLOWED_ATTRIBUTES = {
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
    "font-size",
    "font-family",
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


def _allowed_attributes() -> Dict[str, List[str]]:
    """
    Ako CSSSanitizer postoji, smijemo pustiti sigurne style atribute.
    Ako ne postoji, izbacujemo style atribute da bleach ne padne i da ne ode u fallback koji briše sav HTML.
    """
    attrs = {key: list(value) for key, value in BASE_ALLOWED_ATTRIBUTES.items()}

    if CSSSanitizer is not None:
        for key, value in STYLE_ALLOWED_ATTRIBUTES.items():
            existing = attrs.get(key, [])
            attrs[key] = list(dict.fromkeys(existing + value))

    return attrs


def _normalize_links(html: str) -> str:
    if bleach is None:
        return html

    def add_rel(attrs, new=False):
        href_key = (None, "href") if (None, "href") in attrs else "href"
        target_key = (None, "target") if (None, "target") in attrs else "target"
        rel_key = (None, "rel") if (None, "rel") in attrs else "rel"

        href = attrs.get(href_key)
        target = attrs.get(target_key)

        if href and target == "_blank":
            attrs[rel_key] = "noopener noreferrer"

        return attrs

    try:
        return bleach.linkifier.Linker(callbacks=[add_rel], skip_tags=["pre", "code"]).linkify(html)
    except Exception:
        return html


def sanitize_post_html(html: str) -> str:
    """
    Sanitizira HTML iz CKEditora prije spremanja u bazu.
    """
    raw_html = _remove_dangerous_blocks(html or "")

    if bleach is None:
        return strip_tags(raw_html).strip()

    css_sanitizer = None
    if CSSSanitizer is not None:
        css_sanitizer = CSSSanitizer(allowed_css_properties=ALLOWED_CSS_PROPERTIES)

    clean_kwargs = {
        "tags": ALLOWED_TAGS,
        "attributes": _allowed_attributes(),
        "protocols": ALLOWED_PROTOCOLS,
        "strip": True,
        "strip_comments": True,
    }

    if css_sanitizer is not None:
        clean_kwargs["css_sanitizer"] = css_sanitizer

    cleaned = bleach.clean(raw_html, **clean_kwargs)
    cleaned = _normalize_links(cleaned)

    return cleaned.strip()
