from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path.cwd()
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / "scripts" / f"_banner_clean_backup_{STAMP}"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

FILES_TO_BACKUP = [
    "blog/models.py",
    "blog/view_handlers/settings_views.py",
    "blog/templates/blog/settings/_settings_tab.html",
    "blog/templates/blog/components/blog_header.html",
    "blog/static/css/style.css",
    "blog/static/blog/js/blog_settings_banner.js",
]

def backup(rel):
    path = ROOT / rel
    if path.exists():
        dest = BACKUP_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)

for rel in FILES_TO_BACKUP:
    backup(rel)

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

models_rel = "blog/models.py"
models = read(models_rel)

models = re.sub(
    r"\n\s*BLOG_BANNER_SIZE_CHOICES\s*=\s*\([\s\S]*?\n\s*\)\s*\n\s*blog_banner_size\s*=\s*models\.CharField\([\s\S]*?\)\s*",
    "\n",
    models,
)
models = re.sub(
    r"\n\s*blog_banner_size\s*=\s*models\.CharField\([^\n]*\)\s*",
    "\n",
    models,
)

size_block = """
    BLOG_BANNER_SIZE_CHOICES = (
        ("xsmall", "Vrlo malo"),
        ("small", "Malo"),
        ("medium", "Srednje"),
        ("large", "Veliko"),
    )
    blog_banner_size = models.CharField(
        max_length=10,
        choices=BLOG_BANNER_SIZE_CHOICES,
        default="medium",
    )

"""

if "blog_banner_size = models.CharField" not in models:
    models = re.sub(
        r"(\n\s*blog_banner\s*=\s*models\.ImageField\s*\()",
        size_block + r"\1",
        models,
        count=1,
    )

write(models_rel, models)

views_rel = "blog/view_handlers/settings_views.py"
views = read(views_rel)

views_lines = views.splitlines()
cleaned = []
for line in views_lines:
    if "selected_banner_size" in line or "blog_banner_size" in line or "BLOG_BANNER_SIZE_CHOICES" in line:
        continue
    cleaned.append(line)
views = "\n".join(cleaned) + "\n"

lines = views.splitlines()
out = []
inserted = False
i = 0
while i < len(lines):
    out.append(lines[i])
    if (not inserted) and "selected_position = request.POST.get('blog_banner_position')" in lines[i]:
        i += 1
        while i < len(lines):
            out.append(lines[i])
            if "settings_changed = True" in lines[i]:
                indent = re.match(r"^(\s*)", lines[i]).group(1)
                base_indent = indent[:-4] if len(indent) >= 4 else indent
                out.append(f"{base_indent}selected_banner_size = request.POST.get('blog_banner_size')")
                out.append(f"{base_indent}if selected_banner_size in {{'xsmall', 'small', 'medium', 'large'}} and getattr(profile, 'blog_banner_size', 'medium') != selected_banner_size:")
                out.append(f"{base_indent}    profile.blog_banner_size = selected_banner_size")
                out.append(f"{base_indent}    settings_changed = True")
                inserted = True
                break
            i += 1
    i += 1

views = "\n".join(out) + "\n"
write(views_rel, views)

header_rel = "blog/templates/blog/components/blog_header.html"
header = read(header_rel)

banner_block = """{% if blog.profile.blog_banner %}
{% with banner_position=blog.profile.blog_banner_position|default:'center' banner_size=blog.profile.blog_banner_size|default:'medium' %}
<div class="blog-banner-row blog-banner-pos-{{ banner_position }} blog-banner-size-{{ banner_size }}">
    <img class="blog-banner-image" src="{{ blog.profile.blog_banner.url }}" alt="Slika na vrhu bloga">
</div>
{% endwith %}
{% endif %}
"""

start = header.find("{% if blog.profile.blog_banner %}")
if start != -1:
    header = header[:start].rstrip() + "\n\n" + banner_block
else:
    header = header.rstrip() + "\n\n" + banner_block

write(header_rel, header)

tpl_rel = "blog/templates/blog/settings/_settings_tab.html"
tpl = read(tpl_rel)

repl = {
    "Ä‡": "ć", "Ä": "ć", "Ä": "č", "Ä�": "č", "ÄŒ": "Č", "Ä": "Č",
    "Å¡": "š", "Å ": "Š", "Å¾": "ž", "Å½": "Ž", "Ä‘": "đ", "Ä": "đ",
    "Ä": "Đ", "Ä†": "Ć", "Ä": "Ć",
}
for bad, good in repl.items():
    tpl = tpl.replace(bad, good)

settings_block = """<h5 class="mt-4">Slika na vrhu bloga</h5>

<div class="mb-3">
    <label class="form-label d-block">Odaberi sliku</label>

    <input
        type="file"
        name="blog_banner"
        id="blogBannerInput"
        accept="image/*"
        class="d-none"
    >

    <input type="hidden" name="cropped_blog_banner" id="croppedBlogBanner">

    <button type="button" class="btn btn-outline-primary" id="blogBannerChangeBtn">
        Odaberi i uredi banner
    </button>

    <div class="form-text mt-2">
        Slika će se prikazivati na vrhu tvog bloga. Maksimalna veličina je 2 MB, a maksimalne dimenzije 2200 x 900 px.
    </div>
</div>

<div class="mb-3">
    <label class="form-label d-block">Pozicija slike</label>

    <div class="d-flex flex-wrap gap-4 align-items-center">
        {% with banner_position=user.profile.blog_banner_position|default:"center" %}
        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_position" value="left" {% if banner_position == "left" %}checked{% endif %}>
            Lijevo
        </label>

        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_position" value="center" {% if banner_position == "center" %}checked{% endif %}>
            Sredina
        </label>

        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_position" value="right" {% if banner_position == "right" %}checked{% endif %}>
            Desno
        </label>
        {% endwith %}
    </div>
</div>

<div class="mb-3">
    <label class="form-label d-block">Veličina prikaza bannera</label>

    <div class="d-flex flex-wrap gap-4 align-items-center">
        {% with banner_size=user.profile.blog_banner_size|default:"medium" %}
        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_size" value="xsmall" {% if banner_size == "xsmall" %}checked{% endif %}>
            Vrlo malo
        </label>

        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_size" value="small" {% if banner_size == "small" %}checked{% endif %}>
            Malo
        </label>

        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_size" value="medium" {% if banner_size == "medium" %}checked{% endif %}>
            Srednje
        </label>

        <label class="form-check-label d-inline-flex align-items-center gap-2">
            <input class="form-check-input m-0" type="radio" name="blog_banner_size" value="large" {% if banner_size == "large" %}checked{% endif %}>
            Veliko
        </label>
        {% endwith %}
    </div>
</div>

{% if user.profile.blog_banner %}
<div class="mb-3">
    <label class="form-label d-block">Trenutna slika</label>
    <img src="{{ user.profile.blog_banner.url }}" alt="Trenutna banner slika" class="img-fluid rounded border" style="max-width: 640px; max-height: 260px; object-fit: contain;">

    <div class="form-check mt-3">
        <input class="form-check-input" type="checkbox" name="delete_blog_banner" value="1" id="deleteBlogBanner">
        <label class="form-check-label" for="deleteBlogBanner">Izbriši sliku</label>
    </div>
</div>
{% endif %}

"""

idx = tpl.find("Slika na vrhu bloga")
idx_modal = tpl.find("Uređivanje bannera")
if idx != -1 and idx_modal != -1 and idx_modal > idx:
    head_start = tpl.rfind("<h", 0, idx)
    if head_start == -1:
        head_start = idx
    modal_head_start = tpl.rfind("<h", 0, idx_modal)
    if modal_head_start == -1 or modal_head_start < idx:
        modal_head_start = idx_modal
    tpl = tpl[:head_start] + settings_block + tpl[modal_head_start:]
else:
    raise RuntimeError("Nisam našao banner blok u _settings_tab.html. Prekidam da ne pokvarim template.")

if "blog_settings_banner.js" not in tpl:
    tpl += "\n{% if settings_tab == 'opcenito' %}\n<script src=\"{% static 'blog/js/blog_settings_banner.js' %}\"></script>\n{% endif %}\n"

write(tpl_rel, tpl)

banner_js_rel = "blog/static/blog/js/blog_settings_banner.js"
banner_js = """(function () {
    "use strict";

    function ready(fn) {
        if (document.readyState !== "loading") {
            fn();
        } else {
            document.addEventListener("DOMContentLoaded", fn);
        }
    }

    ready(function () {
        const fileInput = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const changeBtn = document.getElementById("blogBannerChangeBtn");
        const modalEl = document.getElementById("blogBannerCropModal");
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");

        if (!fileInput || !changeBtn || !modalEl || !frame || !img || !zoomRange || !applyBtn) {
            return;
        }

        const form = fileInput.closest("form") || document.querySelector("form");
        let hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');

        if (!hiddenInput && form) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        let modal = null;

        if (window.bootstrap && window.bootstrap.Modal) {
            modal = new window.bootstrap.Modal(modalEl);
        }

        const state = {
            loaded: false,
            naturalWidth: 0,
            naturalHeight: 0,
            scale: 1,
            minScale: 1,
            maxScale: 4,
            x: 0,
            y: 0,
            dragging: false,
            dragStartX: 0,
            dragStartY: 0,
            startX: 0,
            startY: 0
        };

        function showModal() {
            if (modal) {
                modal.show();
            } else {
                modalEl.style.display = "block";
                modalEl.classList.add("show");
                document.body.classList.add("modal-open");
            }
        }

        function hideModal() {
            if (modal) {
                modal.hide();
            } else {
                modalEl.classList.remove("show");
                modalEl.style.display = "none";
                document.body.classList.remove("modal-open");
            }
        }

        function getFrameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, Math.round(rect.width)),
                height: Math.max(1, Math.round(rect.height))
            };
        }

        function calculateLimits() {
            const size = getFrameSize();

            state.minScale = Math.max(
                size.width / state.naturalWidth,
                size.height / state.naturalHeight
            );

            if (!Number.isFinite(state.minScale) || state.minScale <= 0) {
                state.minScale = 1;
            }

            state.maxScale = state.minScale * 4;
        }

        function clampPosition() {
            const size = getFrameSize();
            const scaledWidth = state.naturalWidth * state.scale;
            const scaledHeight = state.naturalHeight * state.scale;

            if (scaledWidth <= size.width) {
                state.x = (size.width - scaledWidth) / 2;
            } else {
                state.x = Math.min(0, Math.max(size.width - scaledWidth, state.x));
            }

            if (scaledHeight <= size.height) {
                state.y = (size.height - scaledHeight) / 2;
            } else {
                state.y = Math.min(0, Math.max(size.height - scaledHeight, state.y));
            }
        }

        function render() {
            if (!state.loaded) {
                return;
            }

            clampPosition();

            img.style.display = "block";
            img.style.position = "absolute";
            img.style.left = "0";
            img.style.top = "0";
            img.style.maxWidth = "none";
            img.style.maxHeight = "none";
            img.style.width = state.naturalWidth + "px";
            img.style.height = state.naturalHeight + "px";
            img.style.transformOrigin = "top left";
            img.style.transform = "translate(" + state.x + "px, " + state.y + "px) scale(" + state.scale + ")";
        }

        function resetEditor() {
            if (!state.loaded) {
                return;
            }

            calculateLimits();
            state.scale = state.minScale;

            const size = getFrameSize();

            state.x = (size.width - state.naturalWidth * state.scale) / 2;
            state.y = (size.height - state.naturalHeight * state.scale) / 2;

            zoomRange.value = "0";
            render();
        }

        function setZoomValue(value) {
            if (!state.loaded) {
                return;
            }

            const oldScale = state.scale;
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            const ratio = safeValue / 100;
            const nextScale = state.minScale + (state.maxScale - state.minScale) * ratio;

            const size = getFrameSize();
            const centerX = size.width / 2;
            const centerY = size.height / 2;

            const imagePointX = (centerX - state.x) / oldScale;
            const imagePointY = (centerY - state.y) / oldScale;

            state.scale = nextScale;
            state.x = centerX - imagePointX * state.scale;
            state.y = centerY - imagePointY * state.scale;

            zoomRange.value = String(safeValue);
            render();
        }

        function openFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) {
                return;
            }

            if (hiddenInput) {
                hiddenInput.value = "";
            }

            const reader = new FileReader();

            reader.onload = function (event) {
                state.loaded = false;

                img.onload = function () {
                    state.naturalWidth = img.naturalWidth;
                    state.naturalHeight = img.naturalHeight;
                    state.loaded = true;

                    showModal();
                    window.setTimeout(resetEditor, 120);
                };

                img.src = event.target.result;
            };

            reader.readAsDataURL(file);
        }

        changeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = fileInput.files && fileInput.files[0];
            openFile(file);
        });

        zoomRange.addEventListener("input", function () {
            setZoomValue(zoomRange.value);
        });

        frame.addEventListener("wheel", function (event) {
            if (!state.loaded) {
                return;
            }

            event.preventDefault();

            const current = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            const next = Math.max(0, Math.min(100, current + step));

            setZoomValue(next);
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!state.loaded) {
                return;
            }

            state.dragging = true;
            state.dragStartX = event.clientX;
            state.dragStartY = event.clientY;
            state.startX = state.x;
            state.startY = state.y;

            frame.setPointerCapture(event.pointerId);
            img.classList.add("is-dragging");
        });

        frame.addEventListener("pointermove", function (event) {
            if (!state.dragging || !state.loaded) {
                return;
            }

            state.x = state.startX + (event.clientX - state.dragStartX);
            state.y = state.startY + (event.clientY - state.dragStartY);

            render();
        });

        function stopDragging(event) {
            if (!state.dragging) {
                return;
            }

            state.dragging = false;
            img.classList.remove("is-dragging");

            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {
                // Nije bitno.
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                resetEditor();
            });
        }

        applyBtn.addEventListener("click", function () {
            if (!state.loaded) {
                return;
            }

            const size = getFrameSize();
            const outputWidth = 2200;
            const outputHeight = 900;

            const sourceX = Math.max(0, -state.x / state.scale);
            const sourceY = Math.max(0, -state.y / state.scale);
            const sourceWidth = Math.min(state.naturalWidth - sourceX, size.width / state.scale);
            const sourceHeight = Math.min(state.naturalHeight - sourceY, size.height / state.scale);

            const canvas = document.createElement("canvas");
            canvas.width = outputWidth;
            canvas.height = outputHeight;

            const ctx = canvas.getContext("2d");
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, outputWidth, outputHeight);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";

            ctx.drawImage(
                img,
                sourceX,
                sourceY,
                sourceWidth,
                sourceHeight,
                0,
                0,
                outputWidth,
                outputHeight
            );

            const dataUrl = canvas.toDataURL("image/jpeg", 0.95);

            if (hiddenInput) {
                hiddenInput.value = dataUrl;
            }

            hideModal();
        });

        if (form) {
            form.addEventListener("submit", function () {
                if (state.loaded && hiddenInput && !hiddenInput.value) {
                    applyBtn.click();
                }
            });
        }

        modalEl.addEventListener("shown.bs.modal", function () {
            if (state.loaded) {
                resetEditor();
            }
        });

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
"""
write(banner_js_rel, banner_js)

css_rel = "blog/static/css/style.css"
css = read(css_rel) if (ROOT / css_rel).exists() else ""

marker = "/* Banner editor and fixed banner sizes */"
if marker not in css:
    css += """

/* Banner editor and fixed banner sizes */
.blog-banner-row {
    display: flex;
    width: 100%;
    margin: 2rem 0;
}

.blog-banner-pos-left {
    justify-content: flex-start;
}

.blog-banner-pos-center {
    justify-content: center;
}

.blog-banner-pos-right {
    justify-content: flex-end;
}

.blog-banner-image {
    display: block;
    height: auto;
    max-width: 100%;
    object-fit: contain;
}

.blog-banner-size-xsmall .blog-banner-image {
    width: min(100%, 360px);
}

.blog-banner-size-small .blog-banner-image {
    width: min(100%, 560px);
}

.blog-banner-size-medium .blog-banner-image {
    width: min(100%, 820px);
}

.blog-banner-size-large .blog-banner-image {
    width: min(100%, 1080px);
}

.banner-crop-modal {
    background: rgba(8, 15, 30, 0.94);
}

.banner-crop-dialog {
    max-width: 1120px;
}

.banner-crop-content {
    background: #111827;
    color: #f8fafc;
    border: 0;
    border-radius: 24px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
}

.banner-crop-title {
    font-size: 28px;
    font-weight: 700;
}

.banner-crop-description {
    color: rgba(248, 250, 252, 0.65);
    margin-bottom: 18px;
}

.banner-crop-stage {
    background: #020617;
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 22px;
    padding: 16px;
}

.banner-crop-frame {
    position: relative;
    width: 100%;
    aspect-ratio: 22 / 9;
    overflow: hidden;
    background: #020617;
    border: 2px solid rgba(255, 255, 255, 0.92);
    border-radius: 14px;
    cursor: grab;
    user-select: none;
    touch-action: none;
}

.banner-crop-frame:active {
    cursor: grabbing;
}

.banner-crop-frame img {
    user-select: none;
    pointer-events: none;
}

.banner-crop-controls {
    margin-top: 18px;
}

.banner-crop-controls label {
    font-weight: 600;
}

.banner-crop-actions {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-top: 16px;
}

@media (max-width: 768px) {
    .blog-banner-row {
        justify-content: center !important;
    }

    .banner-crop-dialog {
        max-width: calc(100% - 20px);
        margin: 10px auto;
    }

    .banner-crop-title {
        font-size: 22px;
    }
}
"""
write(css_rel, css)

migrations_dir = ROOT / "blog" / "migrations"
migrations_dir.mkdir(parents=True, exist_ok=True)

existing_migration = False
for path in migrations_dir.glob("*.py"):
    if path.name == "__init__.py":
        continue
    try:
        if "blog_banner_size" in path.read_text(encoding="utf-8", errors="ignore"):
            existing_migration = True
            break
    except Exception:
        pass

if not existing_migration:
    migration_files = sorted(
        p for p in migrations_dir.glob("[0-9][0-9][0-9][0-9]_*.py")
        if p.is_file()
    )
    if migration_files:
        last = migration_files[-1]
        try:
            next_num = int(last.name[:4]) + 1
        except ValueError:
            next_num = 1
        dependency = last.stem
    else:
        next_num = 1
        dependency = "0001_initial"

    migration_name = f"{next_num:04d}_profile_blog_banner_size.py"
    migration_path = migrations_dir / migration_name

    migration_text = f"""# Generated by banner clean all-in-one fix

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '{dependency}'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='blog_banner_size',
            field=models.CharField(
                max_length=10,
                choices=[
                    ('xsmall', 'Vrlo malo'),
                    ('small', 'Malo'),
                    ('medium', 'Srednje'),
                    ('large', 'Veliko'),
                ],
                default='medium',
            ),
        ),
    ]
"""
    migration_path.write_text(migration_text, encoding="utf-8")

print("Gotovo: banner editor, fiksne pozicije i veličine su pripremljeni.")
print(f"Backup je spremljen u: {BACKUP_DIR}")
print("Sada pokreni: python manage.py check")
print("Ako check prođe: python manage.py migrate")
