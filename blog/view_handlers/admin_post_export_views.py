import base64
import html
import mimetypes
import posixpath
import re
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_GET

from blog.models import Post

try:
    from blog.security import log_security_event
except Exception:
    log_security_event = None


_MEDIA_SRC_RE = re.compile(r"(?P<prefix>\bsrc\s*=\s*[\"'])(?P<src>[^\"']+)(?P<suffix>[\"'])", re.IGNORECASE)


def _fmt_dt(value):
    if not value:
        return ""
    try:
        return timezone.localtime(value).strftime("%d.%m.%Y %H:%M")
    except Exception:
        return str(value)


def _safe_filename(value, fallback="post"):
    base = slugify(value or "", allow_unicode=False).strip("-_")
    return base or fallback


def _zip_path(*parts):
    return posixpath.join(*[str(part).replace("\\", "/").strip("/") for part in parts if str(part).strip("/")])


def _filefield_exists(file_field):
    try:
        return bool(file_field and file_field.name and Path(file_field.path).is_file())
    except Exception:
        return False


def _guess_mime(path):
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def _data_uri_from_path(path):
    path = Path(path)
    if not path.is_file():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{_guess_mime(path)};base64,{encoded}"


def _add_filefield_to_zip(zip_file, file_field, added_files):
    if not _filefield_exists(file_field):
        return ""
    src_path = Path(file_field.path)
    archive_path = _zip_path("media", file_field.name)
    if archive_path not in added_files:
        zip_file.write(src_path, archive_path)
        added_files.add(archive_path)
    return archive_path


def _local_media_path_from_src(src):
    if not src:
        return None
    src = src.strip()
    media_url = getattr(settings, "MEDIA_URL", "/media/") or "/media/"
    if src.startswith(media_url):
        rel = src[len(media_url):].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel
    if src.startswith("media/"):
        rel = src[len("media/"):].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel
    marker = media_url if media_url.startswith("/") else f"/{media_url.strip('/')}"
    if marker and marker in src:
        rel = src.split(marker, 1)[1].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel
    return None


def _embed_media_images_in_content(content):
    if not content:
        return ""
    def replace(match):
        src = match.group("src")
        local_path = _local_media_path_from_src(src)
        if local_path and local_path.is_file():
            data_uri = _data_uri_from_path(local_path)
            if data_uri:
                return f"{match.group('prefix')}{data_uri}{match.group('suffix')}"
        return match.group(0)
    return _MEDIA_SRC_RE.sub(replace, content)


def _status_label(post):
    try:
        return post.get_status_display()
    except Exception:
        return getattr(post, "status", "") or ""


def _post_type_label(post):
    try:
        return post.get_post_type_display()
    except Exception:
        return getattr(post, "post_type", "") or "Post"


def _base_css():
    return """
body { font-family: Arial, sans-serif; margin: 32px; line-height: 1.55; color: #182033; background: #fff; }
a { color: #5b21ff; }
.page { max-width: 920px; margin: 0 auto; }
.post-card, article { border: 1px solid #ddd; border-radius: 14px; padding: 18px; margin: 18px 0; }
.muted { color: #666; }
.meta { border-collapse: collapse; margin: 18px 0; width: 100%; max-width: 640px; }
.meta th, .meta td { border: 1px solid #ddd; padding: 8px 10px; text-align: left; vertical-align: top; }
.meta th { width: 150px; background: #f5f5f5; }
.content { margin-top: 24px; }
img { max-width: 100%; height: auto; border-radius: 10px; }
figure { margin: 18px 0; }
figcaption { color: #666; font-size: 14px; margin-top: 6px; }
.extra { background: #fafafa; border: 1px solid #e5e5e5; border-radius: 12px; padding: 14px; margin-top: 24px; }
"""


def _metadata_html(post):
    category = getattr(getattr(post, "category", None), "name", "") or ""
    try:
        tags = ", ".join(post.tags.values_list("name", flat=True))
    except Exception:
        tags = ""
    rows = [
        ("Status", _status_label(post)),
        ("Tip", _post_type_label(post)),
        ("Kategorija", category),
        ("Tagovi", tags),
        ("Datum", _fmt_dt(getattr(post, "publish_at", None) or getattr(post, "created_at", None))),
        ("Pregledi", str(getattr(post, "views", 0))),
    ]
    try:
        rows.append(("Lajkovi", str(post.likes.count())))
    except Exception:
        pass
    try:
        rows.append(("Komentari", str(post.comments.count())))
    except Exception:
        pass
    html_rows = "".join(f"<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>" for label, value in rows if value)
    return f'<table class="meta">{html_rows}</table>' if html_rows else ""


def _poll_or_quiz_html(post):
    post_type = getattr(post, "post_type", "")
    if post_type == "poll" and hasattr(post, "poll_options"):
        options = list(post.poll_options.all())
        try:
            total_votes = post.poll_votes.count()
        except Exception:
            total_votes = 0
        items = []
        for option in options:
            try:
                votes = post.poll_votes.filter(option=option).count()
            except Exception:
                votes = 0
            percent = round((votes / total_votes) * 100, 1) if total_votes else 0
            items.append(f"<li>{html.escape(option.text)} — {votes} glasova ({percent}%)</li>")
        return f'<div class="extra"><h2>Anketa</h2><p>Ukupno glasova: {total_votes}</p><ul>{"".join(items)}</ul></div>'
    if post_type == "quiz" and hasattr(post, "quiz_options"):
        options = list(post.quiz_options.all())
        try:
            total_answers = post.quiz_answers.count()
        except Exception:
            total_answers = 0
        items = []
        for option in options:
            try:
                answers = post.quiz_answers.filter(selected_option=option).count()
            except Exception:
                answers = 0
            percent = round((answers / total_answers) * 100, 1) if total_answers else 0
            correct = " ✅ točan odgovor" if getattr(option, "is_correct", False) else ""
            items.append(f"<li>{html.escape(option.text)} — {answers} odgovora ({percent}%){correct}</li>")
        return f'<div class="extra"><h2>Kviz</h2><p>Ukupno odgovora: {total_answers}</p><ul>{"".join(items)}</ul></div>'
    return ""


def _post_images_html(post):
    blocks = []
    if _filefield_exists(getattr(post, "image", None)):
        src = _data_uri_from_path(post.image.path)
        if src:
            blocks.append(f'<figure><img src="{src}" alt=""><figcaption>Glavna slika</figcaption></figure>')
    try:
        images = post.images.all()
    except Exception:
        images = []
    for index, image_obj in enumerate(images, start=1):
        if _filefield_exists(getattr(image_obj, "image", None)):
            src = _data_uri_from_path(image_obj.image.path)
            if src:
                blocks.append(f'<figure><img src="{src}" alt=""><figcaption>Slika {index}</figcaption></figure>')
    return "<h2>Slike</h2>" + "".join(blocks) if blocks else ""


def _post_html_document(post, filename):
    content = _embed_media_images_in_content(getattr(post, "content", "") or "")
    return f"""<!doctype html>
<html lang="hr">
<head>
    <meta charset="utf-8">
    <title>{html.escape(post.title)}</title>
    <style>{_base_css()}</style>
</head>
<body>
<div class="page">
    <a class="top-link" href="../index.html">← Povratak na popis postova</a>
    <article>
        <h1>{html.escape(post.title)}</h1>
        <p class="muted">Autor: {html.escape(post.author.username)} · Datoteka: {html.escape(filename)}</p>
        {_metadata_html(post)}
        <div class="content">{content}</div>
        {_post_images_html(post)}
        {_poll_or_quiz_html(post)}
    </article>
</div>
</body>
</html>"""


def _index_html_document(user, exported_posts):
    cards = []
    for post, filename in exported_posts:
        date_label = _fmt_dt(getattr(post, "publish_at", None) or getattr(post, "created_at", None))
        cards.append(f"""
        <div class="post-card">
            <h2>{html.escape(post.title)}</h2>
            <p class="muted">{html.escape(_post_type_label(post))} · {html.escape(_status_label(post))} · {html.escape(date_label)}</p>
            <p><a href="postovi_html/{html.escape(filename)}">Otvori post</a></p>
        </div>
        """)
    if not cards:
        cards.append('<p class="muted">Korisnik nema postova za izvoz.</p>')
    return f"""<!doctype html>
<html lang="hr">
<head>
    <meta charset="utf-8">
    <title>Izvoz postova - {html.escape(user.username)}</title>
    <style>{_base_css()}</style>
</head>
<body>
<div class="page">
    <h1>Izvoz postova</h1>
    <p>Korisnik: <strong>{html.escape(user.username)}</strong></p>
    <p>Datum izvoza: {_fmt_dt(timezone.now())}</p>
    <p class="muted">Ako linkovi ili slike ne rade dok gledaš ZIP direktno iz Windows pregleda, prvo raspakiraj cijeli ZIP u običan folder pa otvori index.html.</p>
    {''.join(cards)}
</div>
</body>
</html>"""


def _readme_text(user, post_count):
    return f"""Izvoz postova
================

Korisnik: {user.username}
Broj postova: {post_count}
Datum izvoza: {_fmt_dt(timezone.now())}

Sadržaj ZIP-a:
- index.html: početna stranica izvoza
- postovi_html/: svaki post kao posebna HTML datoteka
- media/: kopije slika koje pripadaju postovima, ako postoje

U izvoz nisu uključeni komentari drugih korisnika, notifikacije, IP adrese ni sigurnosni događaji.
"""


def _build_admin_user_posts_zip(user):
    buffer = BytesIO()
    added_files = set()
    posts = (
        Post.objects.filter(author=user)
        .select_related("author", "category")
        .prefetch_related("tags", "images")
        .order_by("-created_at")
    )
    exported_posts = []
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for post in posts:
            filename_base = _safe_filename(post.title, fallback=f"post-{post.id}")
            filename = f"{post.id}-{filename_base}.html"
            archive_path = _zip_path("postovi_html", filename)
            _add_filefield_to_zip(zip_file, getattr(post, "image", None), added_files)
            try:
                images = post.images.all()
            except Exception:
                images = []
            for image_obj in images:
                _add_filefield_to_zip(zip_file, getattr(image_obj, "image", None), added_files)
            zip_file.writestr(archive_path, _post_html_document(post, filename))
            exported_posts.append((post, filename))
        zip_file.writestr("index.html", _index_html_document(user, exported_posts))
        zip_file.writestr("README.txt", _readme_text(user, len(exported_posts)))
    buffer.seek(0)
    return buffer


def _export_filename_for_user(user):
    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M")
    username = _safe_filename(user.username, fallback="korisnik")
    return f"postovi_{username}_{timestamp}.zip"


@staff_member_required
@require_GET
def admin_post_exports(request):
    User = get_user_model()
    q = (request.GET.get("q") or "").strip()
    users = User.objects.all().order_by("username")
    if q:
        users = users.filter(username__icontains=q)
    users = users[:100]
    users_with_counts = []
    for user in users:
        users_with_counts.append({"user": user, "post_count": Post.objects.filter(author=user).count()})
    context = {
        **admin.site.each_context(request),
        "title": "Izvoz postova korisnika",
        "q": q,
        "users_with_counts": users_with_counts,
    }
    return render(request, "admin/post_exports.html", context)


@staff_member_required
@require_GET
def admin_export_user_posts(request, user_id):
    User = get_user_model()
    target_user = get_object_or_404(User, pk=user_id)
    archive = _build_admin_user_posts_zip(target_user)
    filename = _export_filename_for_user(target_user)
    if log_security_event:
        try:
            log_security_event(
                request=request,
                event_type="admin_post_export",
                user=request.user,
                severity="info",
                message=f"Admin je izvezao postove korisnika: {target_user.username}",
                metadata={"target_user_id": target_user.id, "target_username": target_user.username},
            )
        except Exception:
            pass
    response = HttpResponse(archive.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
