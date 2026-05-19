from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "scripts" / "_banner_modal_working_backup"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATE = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
STYLE = ROOT / "blog" / "static" / "css" / "style.css"
JS = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"

for path in [TEMPLATE, STYLE, JS]:
    if path.exists():
        backup_name = path.as_posix().replace('/', '__') + ".bak"
        shutil.copy2(path, BACKUP_DIR / backup_name)

JS.parent.mkdir(parents=True, exist_ok=True)

banner_js = """
(function () {
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
        const image = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const closeButtons = modalEl ? modalEl.querySelectorAll("[data-banner-close], .btn-close, .banner-crop-close") : [];

        if (!fileInput || !changeBtn || !modalEl || !frame || !image || !zoomRange || !applyBtn) {
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

        const state = {
            loaded: false,
            naturalWidth: 0,
            naturalHeight: 0,
            x: 0,
            y: 0,
            scale: 1,
            minScale: 1,
            maxScale: 4,
            dragging: false,
            dragStartX: 0,
            dragStartY: 0,
            startX: 0,
            startY: 0
        };

        function showModal() {
            modalEl.classList.add("show");
            modalEl.setAttribute("aria-modal", "true");
            modalEl.removeAttribute("aria-hidden");
            modalEl.style.display = "block";
            document.body.classList.add("modal-open");
            document.body.style.overflow = "hidden";
        }

        function hideModal() {
            modalEl.classList.remove("show");
            modalEl.setAttribute("aria-hidden", "true");
            modalEl.removeAttribute("aria-modal");
            modalEl.style.display = "none";
            document.body.classList.remove("modal-open");
            document.body.style.overflow = "";
        }

        function getFrameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, Math.round(rect.width)),
                height: Math.max(1, Math.round(rect.height))
            };
        }

        function calculateMinScale() {
            const size = getFrameSize();
            state.minScale = Math.max(size.width / state.naturalWidth, size.height / state.naturalHeight);
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
            if (!state.loaded) return;
            clampPosition();

            image.style.display = "block";
            image.style.position = "absolute";
            image.style.left = "0";
            image.style.top = "0";
            image.style.width = state.naturalWidth + "px";
            image.style.height = state.naturalHeight + "px";
            image.style.maxWidth = "none";
            image.style.maxHeight = "none";
            image.style.transformOrigin = "top left";
            image.style.transform = "translate(" + state.x + "px, " + state.y + "px) scale(" + state.scale + ")";
        }

        function resetEditor() {
            if (!state.loaded) return;
            calculateMinScale();
            state.scale = state.minScale;
            const size = getFrameSize();
            state.x = (size.width - state.naturalWidth * state.scale) / 2;
            state.y = (size.height - state.naturalHeight * state.scale) / 2;
            zoomRange.value = "0";
            render();
        }

        function setZoomValue(value) {
            if (!state.loaded) return;

            const oldScale = state.scale;
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            const nextScale = state.minScale + (state.maxScale - state.minScale) * (safeValue / 100);
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
            if (!file || !file.type || !file.type.startsWith("image/")) return;
            if (hiddenInput) hiddenInput.value = "";

            const reader = new FileReader();
            reader.onload = function (event) {
                image.onload = function () {
                    state.naturalWidth = image.naturalWidth;
                    state.naturalHeight = image.naturalHeight;
                    state.loaded = true;
                    showModal();
                    window.setTimeout(resetEditor, 80);
                };
                image.src = event.target.result;
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
            if (!state.loaded) return;
            event.preventDefault();
            const current = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            setZoomValue(Math.max(0, Math.min(100, current + step)));
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!state.loaded) return;
            state.dragging = true;
            state.dragStartX = event.clientX;
            state.dragStartY = event.clientY;
            state.startX = state.x;
            state.startY = state.y;
            frame.setPointerCapture(event.pointerId);
        });

        frame.addEventListener("pointermove", function (event) {
            if (!state.dragging || !state.loaded) return;
            state.x = state.startX + (event.clientX - state.dragStartX);
            state.y = state.startY + (event.clientY - state.dragStartY);
            render();
        });

        function stopDragging(event) {
            if (!state.dragging) return;
            state.dragging = false;
            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {}
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (resetBtn) {
            resetBtn.addEventListener("click", function (event) {
                event.preventDefault();
                resetEditor();
            });
        }

        closeButtons.forEach(function (button) {
            button.addEventListener("click", function (event) {
                event.preventDefault();
                hideModal();
            });
        });

        function copyBlobToFileInput(blob) {
            try {
                const file = new File([blob], "blog_banner.jpg", { type: "image/jpeg" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
            } catch (error) {}
        }

        applyBtn.addEventListener("click", function (event) {
            event.preventDefault();
            if (!state.loaded) return;

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
            ctx.drawImage(image, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, outputWidth, outputHeight);

            const dataUrl = canvas.toDataURL("image/jpeg", 0.95);
            if (hiddenInput) hiddenInput.value = dataUrl;

            canvas.toBlob(function (blob) {
                if (blob) copyBlobToFileInput(blob);
                hideModal();
            }, "image/jpeg", 0.95);
        });

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
"""
JS.write_text(banner_js.strip() + "\n", encoding="utf-8")

if STYLE.exists():
    css = STYLE.read_text(encoding="utf-8", errors="replace")
else:
    css = ""

marker = "/* Banner editor modal - working clean version */"
css_block = """
/* Banner editor modal - working clean version */
#blogBannerCropModal {
    display: none !important;
}

#blogBannerCropModal.show {
    position: fixed !important;
    inset: 0 !important;
    z-index: 2050 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 24px !important;
    background: rgba(0, 0, 0, 0.55) !important;
    overflow: auto !important;
}

#blogBannerCropModal .modal-dialog,
#blogBannerCropModal .banner-crop-dialog,
#blogBannerCropModal > .modal-content,
#blogBannerCropModal > .banner-crop-content {
    width: min(1180px, 96vw) !important;
    margin: auto !important;
}

#blogBannerCropModal .modal-content,
#blogBannerCropModal .banner-crop-content,
#blogBannerCropModal .avatar-crop-modal {
    background: #111827 !important;
    color: #f8fafc !important;
    border-radius: 22px !important;
    padding: 22px 28px !important;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.35) !important;
}

#blogBannerCropModal .modal-header,
#blogBannerCropModal .banner-crop-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 16px !important;
    padding: 0 0 14px 0 !important;
    border: 0 !important;
}

#blogBannerCropModal h1,
#blogBannerCropModal h2,
#blogBannerCropModal .modal-title {
    font-size: 28px !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    color: #f8fafc !important;
}

#blogBannerCropModal p,
#blogBannerCropModal .text-muted {
    color: rgba(248, 250, 252, 0.72) !important;
    margin: 4px 0 18px 0 !important;
}

#blogBannerCropModal .btn-close,
#blogBannerCropModal .banner-crop-close {
    width: 28px !important;
    height: 28px !important;
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    color: #f8fafc !important;
    opacity: 0.85 !important;
    font-size: 28px !important;
    line-height: 1 !important;
}

#blogBannerCropFrame {
    position: relative !important;
    width: 100% !important;
    aspect-ratio: 22 / 9 !important;
    max-height: 440px !important;
    overflow: hidden !important;
    background: #030712 !important;
    border: 2px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 16px !important;
    cursor: grab !important;
    user-select: none !important;
    touch-action: none !important;
}

#blogBannerCropFrame:active {
    cursor: grabbing !important;
}

#blogBannerCropImage {
    user-select: none !important;
    pointer-events: none !important;
}

#blogBannerCropModal .banner-editor-controls,
#blogBannerCropModal .avatar-editor-controls,
#blogBannerCropModal .modal-footer {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 14px !important;
    flex-wrap: wrap !important;
    padding-top: 16px !important;
    border: 0 !important;
}

#blogBannerZoomRange {
    flex: 1 1 420px !important;
}

#blogBannerCropModal .btn,
#blogBannerCropModal button {
    font-size: 16px !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
}
"""

if marker not in css:
    css += "\n\n" + css_block.strip() + "\n"
STYLE.parent.mkdir(parents=True, exist_ok=True)
STYLE.write_text(css, encoding="utf-8")

html = TEMPLATE.read_text(encoding="utf-8", errors="replace")

if 'name="cropped_blog_banner"' not in html and "name='cropped_blog_banner'" not in html:
    hidden = '\n<input type="hidden" name="cropped_blog_banner" id="croppedBlogBanner">\n'
    if 'id="blogBannerInput"' in html:
        html = re.sub(r'(<input[^>]*id="blogBannerInput"[^>]*>)', r'\1' + hidden, html, count=1, flags=re.S)
    elif 'name="blog_banner"' in html:
        html = re.sub(r'(<input[^>]*name="blog_banner"[^>]*>)', r'\1' + hidden, html, count=1, flags=re.S)
    else:
        html = html.replace('Uređivanje bannera', hidden + 'Uređivanje bannera', 1)

html = re.sub(r'(<button[^>]*(?:btn-close|banner-crop-close)[^>]*)(>)', lambda m: m.group(1) + (' data-banner-close' if 'data-banner-close' not in m.group(1) else '') + m.group(2), html, flags=re.S)
html = re.sub(r'(<[^>]+id="blogBannerCropModal"[^>]*)(>)', lambda m: m.group(1) + (' style="display:none;"' if 'style=' not in m.group(1) else '') + m.group(2), html, count=1, flags=re.S)

script_tag = "{% if settings_tab == 'opcenito' %}<script src=\"{% static 'blog/js/blog_settings_banner.js' %}?v=working-banner-modal\"></script>{% endif %}"
if 'blog_settings_banner.js' not in html:
    html = html.rstrip() + "\n" + script_tag + "\n"
else:
    html = re.sub(r"blog/js/blog_settings_banner\.js(?:\?v=[^'\"]+)?", "blog/js/blog_settings_banner.js?v=working-banner-modal", html)

TEMPLATE.write_text(html, encoding="utf-8")
print("Banner modal i JS su popravljeni. Pokreni: python manage.py check")
