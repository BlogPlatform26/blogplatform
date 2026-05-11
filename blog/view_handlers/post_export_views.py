import base64
import html
import mimetypes
import posixpath
import re
import zipfile
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_GET

from blog.models import Post


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
    mime = _guess_mime(path)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _add_filefield_to_zip(zip_file, file_field, added_files):
    if not _filefield_exists(file_field):
        return ""

    src_path = Path(file_field.path)
    # U ZIP-u čuvamo istu relativnu putanju kao u media folderu.
    archive_path = _zip_path("media", file_field.name)

    if archive_path not in added_files:
        zip_file.write(src_path, archive_path)
        added_files.add(archive_path)

    return archive_path


def _filefield_img_src(file_field, current_folder=""):
    """
    Vraća data URI kad god može, da slike rade i ako korisnik otvori HTML direktno.
    Ako iz nekog razloga ne može, vraća relativnu putanju prema media/ folderu.
    """
    if not _filefield_exists(file_field):
        return ""

    data_uri = _data_uri_from_path(file_field.path)
    if data_uri:
        return data_uri

    archive_path = _zip_path("media", file_field.name)
    if current_folder:
        return posixpath.relpath(archive_path, start=current_folder)
    return archive_path


def _local_media_path_from_src(src):
    if not src:
        return None

    src = src.strip()
    media_url = getattr(settings, "MEDIA_URL", "/media/") or "/media/"

    # /media/post_images/a.jpg
    if src.startswith(media_url):
        rel = src[len(media_url):].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel

    # media/post_images/a.jpg
    if src.startswith("media/"):
        rel = src[len("media/"):].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel

    # http://127.0.0.1:8000/media/post_images/a.jpg ili https://domena/media/...
    marker = media_url if media_url.startswith("/") else f"/{media_url.strip('/')}"
    if marker and marker in src:
        rel = src.split(marker, 1)[1].lstrip("/")
        return Path(settings.MEDIA_ROOT) / rel

    return None


def _embed_media_images_in_content(content):
    """
    Ako sadržaj posta ima <img src='/media/...'>, zamijeni src s data URI.
    Tako HTML izvoz ostaje čitljiv i kad se otvori izvan Django projekta.
    Vanjske slike ne diramo.
    """
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


def _post_type_label(post):
    try:
        return post.get_post_type_display()
    except Exception:
        return post.post_type or "Post"


def _status_label(post):
    try:
        return post.get_status_display()
    except Exception:
        return post.status or ""


def _post_metadata_html(post):
    category = post.category.name if post.category else ""
    tags = ", ".join(post.tags.values_list("name", flat=True))
    published_at = _fmt_dt(post.publish_at or post.created_at)

    rows = [
        ("Status", _status_label(post)),
        ("Tip", _post_type_label(post)),
        ("Kategorija", category),
        ("Tagovi", tags),
        ("Datum", published_at),
        ("Pregledi", str(getattr(post, "views", 0))),
        ("Lajkovi", str(post.likes.count() if hasattr(post, "likes") else 0)),
        ("Komentari", str(post.comments.count() if hasattr(post, "comments") else 0)),
    ]
    html_rows = "".join(
        f"<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>"
        for label, value in rows
        if value
    )
    return f"<table class='meta'>{html_rows}</table>" if html_rows else ""


def _poll_or_quiz_html(post):
    if post.post_type == "poll":
        options = list(post.poll_options.all())
        total_votes = post.poll_votes.count()
        if not options:
            return ""
        items = []
        for option in options:
            votes = post.poll_votes.filter(option=option).count()
            percent = round((votes / total_votes) * 100, 1) if total_votes else 0
            items.append(
                f"<li>{html.escape(option.text)} — {votes} glasova ({percent}%)</li>"
            )
        return (
            "<section class='extra'><h2>Anketa</h2>"
            f"<p>Ukupno glasova: {total_votes}</p><ul>{''.join(items)}</ul></section>"
        )

    if post.post_type == "quiz":
        options = list(post.quiz_options.all())
        total_answers = post.quiz_answers.count()
        if not options:
            return ""
        items = []
        for option in options:
            answers = post.quiz_answers.filter(selected_option=option).count()
            percent = round((answers / total_answers) * 100, 1) if total_answers else 0
            correct = " ✅ točan odgovor" if option.is_correct else ""
            items.append(
                f"<li>{html.escape(option.text)} — {answers} odgovora ({percent}%){correct}</li>"
            )
        return (
            "<section class='extra'><h2>Kviz</h2>"
            f"<p>Ukupno odgovora: {total_answers}</p><ul>{''.join(items)}</ul></section>"
        )

    return ""


def _post_images_html(post, current_folder="postovi_html"):
    blocks = []

    if _filefield_exists(post.image):
        src = _filefield_img_src(post.image, current_folder=current_folder)
        if src:
            blocks.append(
                f"<figure><img src=\"{src}\" alt=\"Slika posta\"><figcaption>Glavna slika</figcaption></figure>"
            )

    for index, image_obj in enumerate(post.images.all(), start=1):
        if _filefield_exists(image_obj.image):
            src = _filefield_img_src(image_obj.image, current_folder=current_folder)
            if src:
                blocks.append(
                    f"<figure><img src=\"{src}\" alt=\"Slika {index}\"><figcaption>Slika {index}</figcaption></figure>"
                )

    if not blocks:
        return ""

    return "<section class='images'><h2>Slike</h2>" + "".join(blocks) + "</section>"


def _base_css():
    return """
    body { font-family: Arial, sans-serif; margin: 32px; line-height: 1.55; color: #182033; background: #ffffff; }
    a { color: #5b21ff; }
    .page { max-width: 920px; margin: 0 auto; }
    .top-link { margin-bottom: 24px; display: inline-block; }
    h1 { margin-bottom: 6px; }
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
    .note { background: #fff8d8; border: 1px solid #f0d46a; border-radius: 12px; padding: 12px 14px; }
    """


def _post_html_document(post, filename):
    content = _embed_media_images_in_content(post.content or "")
    images_html = _post_images_html(post, current_folder="postovi_html")
    extra_html = _poll_or_quiz_html(post)
    return f"""<!doctype html>
<html lang="hr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(post.title)}</title>
  <style>{_base_css()}</style>
</head>
<body>
  <main class="page">
    <a class="top-link" href="../index.html">← Povratak na popis postova</a>
    <article>
      <h1>{html.escape(post.title)}</h1>
      <p class="muted">Autor: {html.escape(post.author.username)} · Izvoz datoteka: {html.escape(filename)}</p>
      {_post_metadata_html(post)}
      <section class="content">
        {content}
      </section>
      {images_html}
      {extra_html}
    </article>
  </main>
</body>
</html>
"""


def _index_html_document(user, exported_posts):
    cards = []
    for post, filename in exported_posts:
        date_label = _fmt_dt(post.publish_at or post.created_at)
        status = _status_label(post)
        post_type = _post_type_label(post)
        cards.append(f"""
        <section class="post-card">
          <h2>{html.escape(post.title)}</h2>
          <p class="muted">{html.escape(post_type)} · {html.escape(status)} · {html.escape(date_label)}</p>
          <p><a href="postovi_html/{html.escape(filename)}">Otvori post</a></p>
        </section>
        """)

    if not cards:
        cards.append("<p>Nema postova za izvoz.</p>")

    return f"""<!doctype html>
<html lang="hr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Izvoz postova - {html.escape(user.username)}</title>
  <style>{_base_css()}</style>
</head>
<body>
  <main class="page">
    <h1>Izvoz postova</h1>
    <p class="muted">Korisnik: {html.escape(user.username)} · Datum izvoza: {_fmt_dt(timezone.now())}</p>
    <div class="note">
      Ako linkovi ili slike ne rade dok gledaš ZIP direktno iz Windows pregleda, prvo raspakiraj cijeli ZIP u običan folder pa otvori <strong>index.html</strong>.
    </div>
    {''.join(cards)}
  </main>
</body>
</html>
"""


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

Važno:
Ako linkovi ili slike ne rade dok otvaraš datoteke direktno iz ZIP-a,
raspakiraj cijeli ZIP u običan folder i onda otvori index.html.

U izvoz nisu uključeni komentari drugih korisnika, notifikacije, IP adrese ni sigurnosni događaji.
"""


def _build_user_posts_zip(user):
    buffer = BytesIO()
    added_files = set()

    posts = (
        Post.objects.filter(author=user)
        .select_related("author", "category")
        .prefetch_related("tags", "images", "likes", "comments", "poll_options", "poll_votes", "quiz_options", "quiz_answers")
        .order_by("-created_at")
    )

    exported_posts = []

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for post in posts:
            filename_base = _safe_filename(post.title, fallback=f"post-{post.id}")
            filename = f"{post.id}-{filename_base}.html"
            archive_path = _zip_path("postovi_html", filename)

            # Kopiraj slike u media/ folder ZIP-a, čak i ako ih HTML može prikazati kao data URI.
            _add_filefield_to_zip(zip_file, post.image, added_files)
            for image_obj in post.images.all():
                _add_filefield_to_zip(zip_file, image_obj.image, added_files)

            zip_file.writestr(archive_path, _post_html_document(post, filename))
            exported_posts.append((post, filename))

        zip_file.writestr("index.html", _index_html_document(user, exported_posts))
        zip_file.writestr("README.txt", _readme_text(user, len(exported_posts)))

    buffer.seek(0)
    return buffer


@login_required
@require_GET
def export_my_posts(request):
    archive = _build_user_posts_zip(request.user)
    timestamp = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M")
    username = _safe_filename(request.user.username, fallback="korisnik")
    filename = f"postovi_{username}_{timestamp}.zip"

    response = HttpResponse(archive.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
