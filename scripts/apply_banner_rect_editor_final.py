from pathlib import Path
import re
import shutil

ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
BACKUP_DIR = ROOT / "scripts" / "_banner_rect_editor_final_backup"

BANNER_JS = r'''
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
        const hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');
        const changeBtn = document.getElementById("blogBannerChangeBtn");
        const selectedName = document.getElementById("blogBannerSelectedName");

        const modalEl = document.getElementById("blogBannerCropModal");
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");

        if (!fileInput || !hiddenInput || !changeBtn || !modalEl || !frame || !img || !zoomRange || !applyBtn) {
            return;
        }

        let modal = null;
        if (window.bootstrap && window.bootstrap.Modal) {
            modal = new window.bootstrap.Modal(modalEl);
        }

        let imageLoaded = false;
        let naturalWidth = 0;
        let naturalHeight = 0;
        let minScale = 1;
        let maxScale = 4;
        let scale = 1;
        let x = 0;
        let y = 0;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let startX = 0;
        let startY = 0;
        let objectUrl = null;

        function showModal() {
            if (modal) {
                modal.show();
                return;
            }
            modalEl.style.display = "block";
            modalEl.classList.add("show");
            document.body.classList.add("modal-open");
        }

        function hideModal() {
            if (modal) {
                modal.hide();
                return;
            }
            modalEl.classList.remove("show");
            modalEl.style.display = "none";
            document.body.classList.remove("modal-open");
        }

        function frameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, rect.width),
                height: Math.max(1, rect.height)
            };
        }

        function calculateLimits() {
            const size = frameSize();
            minScale = Math.max(size.width / naturalWidth, size.height / naturalHeight);
            maxScale = minScale * 4;

            if (!Number.isFinite(minScale) || minScale <= 0) {
                minScale = 1;
            }
            if (!Number.isFinite(maxScale) || maxScale <= minScale) {
                maxScale = minScale + 1;
            }
        }

        function clampPosition() {
            const size = frameSize();
            const scaledWidth = naturalWidth * scale;
            const scaledHeight = naturalHeight * scale;

            if (scaledWidth <= size.width) {
                x = (size.width - scaledWidth) / 2;
            } else {
                x = Math.min(0, Math.max(size.width - scaledWidth, x));
            }

            if (scaledHeight <= size.height) {
                y = (size.height - scaledHeight) / 2;
            } else {
                y = Math.min(0, Math.max(size.height - scaledHeight, y));
            }
        }

        function render() {
            clampPosition();
            img.style.width = naturalWidth + "px";
            img.style.height = naturalHeight + "px";
            img.style.transform = "translate(" + x + "px, " + y + "px) scale(" + scale + ")";
        }

        function setZoomFromRange(value) {
            if (!imageLoaded) {
                return;
            }

            const oldScale = scale;
            const size = frameSize();
            const centerX = size.width / 2;
            const centerY = size.height / 2;
            const ratio = Math.max(0, Math.min(100, Number(value))) / 100;

            scale = minScale + (maxScale - minScale) * ratio;

            const imagePointX = (centerX - x) / oldScale;
            const imagePointY = (centerY - y) / oldScale;
            x = centerX - imagePointX * scale;
            y = centerY - imagePointY * scale;

            render();
        }

        function resetEditor() {
            if (!imageLoaded) {
                return;
            }

            calculateLimits();
            scale = minScale;
            const size = frameSize();
            x = (size.width - naturalWidth * scale) / 2;
            y = (size.height - naturalHeight * scale) / 2;
            zoomRange.value = "0";
            render();
        }

        function openSelectedFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) {
                return;
            }

            hiddenInput.value = "";

            if (objectUrl) {
                URL.revokeObjectURL(objectUrl);
                objectUrl = null;
            }

            objectUrl = URL.createObjectURL(file);
            imageLoaded = false;
            img.onload = function () {
                naturalWidth = img.naturalWidth;
                naturalHeight = img.naturalHeight;
                imageLoaded = true;
                showModal();
                window.setTimeout(resetEditor, 80);
            };
            img.src = objectUrl;

            if (selectedName) {
                selectedName.textContent = file.name || "Odabrana slika";
            }
        }

        changeBtn.addEventListener("click", function () {
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = fileInput.files && fileInput.files[0];
            openSelectedFile(file);
        });

        zoomRange.addEventListener("input", function () {
            setZoomFromRange(zoomRange.value);
        });

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                resetEditor();
            });
        }

        frame.addEventListener("wheel", function (event) {
            if (!imageLoaded) {
                return;
            }
            event.preventDefault();
            const current = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            const next = Math.max(0, Math.min(100, current + step));
            zoomRange.value = String(next);
            setZoomFromRange(next);
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!imageLoaded) {
                return;
            }
            isDragging = true;
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            startX = x;
            startY = y;
            frame.setPointerCapture(event.pointerId);
            img.classList.add("is-dragging");
        });

        frame.addEventListener("pointermove", function (event) {
            if (!isDragging || !imageLoaded) {
                return;
            }
            x = startX + (event.clientX - dragStartX);
            y = startY + (event.clientY - dragStartY);
            render();
        });

        function stopDragging(event) {
            if (!isDragging) {
                return;
            }
            isDragging = false;
            img.classList.remove("is-dragging");
            if (event && frame.releasePointerCapture) {
                try {
                    frame.releasePointerCapture(event.pointerId);
                } catch (error) {
                    // nije važno ako pointer više nije aktivan
                }
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        applyBtn.addEventListener("click", function () {
            if (!imageLoaded) {
                return;
            }

            const size = frameSize();
            const outputWidth = 2200;
            const outputHeight = 900;
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");

            canvas.width = outputWidth;
            canvas.height = outputHeight;

            const sourceX = Math.max(0, -x / scale);
            const sourceY = Math.max(0, -y / scale);
            const sourceWidth = Math.min(naturalWidth - sourceX, size.width / scale);
            const sourceHeight = Math.min(naturalHeight - sourceY, size.height / scale);

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, outputWidth, outputHeight);
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

            hiddenInput.value = canvas.toDataURL("image/jpeg", 0.96);

            if (selectedName) {
                selectedName.textContent = "Banner je pripremljen. Klikni Spremi promjene.";
            }

            hideModal();
        });

        window.addEventListener("resize", function () {
            if (imageLoaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
'''

BANNER_MODAL = r'''
<div class="modal fade banner-crop-modal" id="blogBannerCropModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content">
            <div class="modal-header border-0">
                <div>
                    <h5 class="modal-title mb-1">Uređivanje bannera</h5>
                    <div class="small text-muted">Namjestite pravokutni izrez prije spremanja.</div>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Zatvori"></button>
            </div>
            <div class="modal-body pt-0">
                <div class="banner-crop-stage">
                    <div class="banner-crop-frame" id="blogBannerCropFrame">
                        <img id="blogBannerCropImage" alt="Banner preview">
                    </div>
                </div>
                <div class="banner-crop-controls mt-3">
                    <div class="banner-crop-control-row">
                        <label for="blogBannerZoomRange" class="form-label mb-1">Uvećanje</label>
                        <input type="range" id="blogBannerZoomRange" min="0" max="100" value="0" class="form-range">
                    </div>
                    <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center mt-3">
                        <button type="button" class="btn btn-outline-secondary btn-sm" id="blogBannerResetBtn">Vrati</button>
                        <button type="button" class="btn btn-primary btn-sm" id="blogBannerApplyBtn">Primijeni banner</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''

BANNER_STYLE = r'''
<style id="banner-rect-editor-style">
#blogBannerCropModal .modal-dialog {
    max-width: 900px !important;
    margin: 1.25rem auto !important;
}
#blogBannerCropModal .modal-content {
    border-radius: 20px !important;
    padding: 18px 24px !important;
}
#blogBannerCropModal .modal-header {
    padding: 0 0 10px 0 !important;
    border-bottom: 0 !important;
}
#blogBannerCropModal .modal-title {
    font-size: 24px !important;
    line-height: 1.2 !important;
    margin: 0 0 4px 0 !important;
}
#blogBannerCropModal .text-muted {
    font-size: 13px !important;
}
#blogBannerCropModal .btn-close {
    width: 22px !important;
    height: 22px !important;
    padding: 0 !important;
    transform: scale(0.8) !important;
    opacity: 0.85 !important;
}
#blogBannerCropModal .modal-body {
    padding: 0 !important;
}
#blogBannerCropModal .banner-crop-stage {
    max-width: 820px !important;
    margin: 12px auto 10px auto !important;
    padding: 10px !important;
    border-radius: 18px !important;
    background: #05080d !important;
}
#blogBannerCropModal .banner-crop-frame {
    width: 100% !important;
    aspect-ratio: 22 / 9;
    position: relative !important;
    overflow: hidden !important;
    border-radius: 14px !important;
    background: #05080d !important;
    cursor: grab;
}
#blogBannerCropModal .banner-crop-frame::after {
    content: "";
    position: absolute;
    inset: 0;
    border: 3px solid rgba(255, 255, 255, 0.95);
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.25), 0 0 0 9999px rgba(0, 0, 0, 0.12);
    pointer-events: none;
    z-index: 3;
}
#blogBannerCropModal #blogBannerCropImage {
    position: absolute !important;
    left: 0;
    top: 0;
    max-width: none !important;
    max-height: none !important;
    width: auto !important;
    height: auto !important;
    user-select: none !important;
    -webkit-user-drag: none !important;
    transform-origin: top left !important;
    cursor: grab;
}
#blogBannerCropModal #blogBannerCropImage.is-dragging,
#blogBannerCropModal .banner-crop-frame:active {
    cursor: grabbing;
}
#blogBannerCropModal .banner-crop-controls {
    max-width: 820px !important;
    margin: 0 auto !important;
}
#blogBannerCropModal label,
#blogBannerCropModal .form-label {
    font-size: 15px !important;
    font-weight: 600 !important;
}
#blogBannerCropModal .btn,
#blogBannerCropModal button {
    font-size: 14px !important;
    line-height: 1.2 !important;
    padding: 7px 14px !important;
    border-radius: 8px !important;
}
@media (max-width: 768px) {
    #blogBannerCropModal .modal-dialog {
        max-width: calc(100vw - 18px) !important;
        margin: 0.75rem auto !important;
    }
    #blogBannerCropModal .modal-content {
        padding: 14px !important;
    }
}
</style>
'''

SCRIPT_INCLUDE = r'''
{% if settings_tab == 'opcenito' %}
<script src="{% static 'blog/js/blog_settings_banner.js' %}?v=banner-rect-final"></script>
{% endif %}
'''

REPLACEMENT_INPUT = r'''
<div class="d-flex flex-wrap gap-2 align-items-center">
    <input type="file" name="blog_banner" id="blogBannerInput" class="d-none" accept="image/*">
    <button type="button" class="btn btn-outline-primary btn-sm" id="blogBannerChangeBtn">Odaberi i uredi banner</button>
    <span class="small text-muted" id="blogBannerSelectedName"></span>
</div>
<input type="hidden" name="cropped_blog_banner" id="croppedBlogBanner">
'''


def backup_once(path: Path):
    if not path.exists():
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / path.name
    if not backup_path.exists():
        shutil.copy2(path, backup_path)


def main():
    if not HTML_PATH.exists():
        raise SystemExit(f"Ne postoji file: {HTML_PATH}")

    backup_once(HTML_PATH)
    backup_once(JS_PATH)

    html = HTML_PATH.read_text(encoding="utf-8")

    # Makni stari phase4B banner preview blok jer samo smeta i ne radi uređivanje.
    html = re.sub(
        r"\n?\{# === Banner preview phase 4B === #\}.*?(?=\n<style id=\"avatar-editor-normal-style\">|\Z)",
        "\n",
        html,
        flags=re.DOTALL,
    )

    # Makni eventualne stare duple hidden inpute za banner crop.
    html = re.sub(
        r"\s*<input[^>]+name=[\"']cropped_blog_banner[\"'][^>]*>\s*",
        "\n",
        html,
        flags=re.IGNORECASE,
    )

    # Ako već postoji stari banner modal, makni ga da ne ostanu dupli ID-jevi.
    html = re.sub(
        r"\n?<div class=\"modal fade banner-crop-modal\" id=\"blogBannerCropModal\".*?</div>\s*</div>\s*</div>\s*</div>",
        "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )

    if 'id="blogBannerChangeBtn"' not in html:
        pattern = r"<input\s+[^>]*name=[\"']blog_banner[\"'][^>]*>"
        html, count = re.subn(pattern, REPLACEMENT_INPUT, html, count=1, flags=re.IGNORECASE)
        if count == 0:
            raise SystemExit("Nisam našao input name='blog_banner' u _settings_tab.html")

    if 'id="blogBannerCropModal"' not in html:
        marker = '<div class="modal fade avatar-crop-modal" id="avatarCropModal"'
        if marker in html:
            html = html.replace(marker, BANNER_MODAL + "\n" + marker, 1)
        else:
            fallback = "{% elif settings_tab == 'postovi' %}"
            if fallback in html:
                html = html.replace(fallback, BANNER_MODAL + "\n" + fallback, 1)
            else:
                raise SystemExit("Nisam našao mjesto za banner modal.")

    if 'id="banner-rect-editor-style"' not in html:
        if '<style id="avatar-editor-normal-style">' in html:
            html = html.replace('<style id="avatar-editor-normal-style">', BANNER_STYLE + "\n<style id=\"avatar-editor-normal-style\">", 1)
        else:
            html += "\n" + BANNER_STYLE

    if "blog_settings_banner.js" not in html:
        html += "\n" + SCRIPT_INCLUDE + "\n"

    HTML_PATH.write_text(html, encoding="utf-8")

    JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    JS_PATH.write_text(BANNER_JS, encoding="utf-8")

    print("Banner editor je dodan/popravljen.")
    print("Dodan je poseban JS file: blog/static/blog/js/blog_settings_banner.js")
    print("Avatar nije diran.")


if __name__ == "__main__":
    main()
