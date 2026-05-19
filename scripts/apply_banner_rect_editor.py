from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
TEMPLATE_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_SOURCE = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
SCRIPT_SOURCE = ROOT / "scripts" / "apply_banner_rect_editor.py"
BACKUP_DIR = ROOT / "scripts" / "_banner_rect_editor_backup"

BANNER_JS_CONTENT = r'''(function () {
    "use strict";

    function onReady(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    function injectBannerEditorStyle() {
        if (document.getElementById("bannerEditorRectStyle")) {
            return;
        }

        const style = document.createElement("style");
        style.id = "bannerEditorRectStyle";
        style.textContent = `
            #blogBannerCropModal .modal-dialog {
                max-width: 980px;
                margin: 1.25rem auto;
            }

            #blogBannerCropModal .modal-content {
                background: #111827;
                color: #f8fafc;
                border: 0;
                border-radius: 22px;
                padding: 18px 24px;
                box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
            }

            #blogBannerCropModal .modal-header {
                border-bottom: 0;
                padding: 0 0 12px 0;
            }

            #blogBannerCropModal .modal-title {
                font-size: 24px;
                line-height: 1.2;
                margin: 0 0 4px 0;
            }

            #blogBannerCropModal .text-muted {
                color: rgba(248, 250, 252, 0.62) !important;
                font-size: 13px;
            }

            #blogBannerCropModal .btn-close {
                filter: invert(1) grayscale(100%);
                opacity: 0.85;
                transform: scale(0.82);
            }

            #blogBannerCropModal .modal-body {
                padding: 0;
            }

            #blogBannerCropModal .banner-crop-stage {
                max-width: 860px;
                margin: 14px auto 12px auto;
                padding: 10px;
                border: 1px solid rgba(148, 163, 184, 0.26);
                border-radius: 18px;
                background: rgba(15, 23, 42, 0.92);
            }

            #blogBannerCropModal .banner-crop-frame {
                width: 100%;
                aspect-ratio: 22 / 9;
                min-height: 220px;
                max-height: 340px;
                position: relative;
                overflow: hidden;
                border-radius: 14px;
                background: #05080d;
                border: 2px solid rgba(255, 255, 255, 0.88);
                touch-action: none;
            }

            #blogBannerCropModal .banner-crop-frame::after {
                content: "";
                position: absolute;
                inset: 0;
                border: 1px solid rgba(255, 255, 255, 0.42);
                box-shadow: inset 0 0 0 9999px rgba(0, 0, 0, 0.04);
                pointer-events: none;
                z-index: 3;
            }

            #blogBannerCropModal #blogBannerCropImage {
                position: absolute;
                left: 0;
                top: 0;
                max-width: none !important;
                max-height: none !important;
                width: auto !important;
                height: auto !important;
                user-select: none;
                -webkit-user-drag: none;
                cursor: grab;
                transform-origin: center center;
                will-change: transform;
            }

            #blogBannerCropModal #blogBannerCropImage.is-dragging {
                cursor: grabbing;
            }

            #blogBannerCropModal .banner-crop-controls {
                max-width: 860px;
                margin: 0 auto;
            }

            #blogBannerCropModal .banner-crop-control-row {
                display: grid;
                grid-template-columns: 120px 1fr;
                gap: 14px;
                align-items: center;
            }

            #blogBannerCropModal .form-label {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 0;
            }

            #blogBannerCropModal #blogBannerZoomRange {
                height: 5px;
            }

            #blogBannerCropModal .btn {
                font-size: 14px;
                line-height: 1.2;
                padding: 7px 12px;
                border-radius: 8px;
            }

            #blogBannerCropModal #blogBannerApplyBtn {
                font-size: 15px;
                padding: 8px 18px;
                min-width: 160px;
            }

            @media (max-width: 768px) {
                #blogBannerCropModal .modal-dialog {
                    max-width: calc(100vw - 18px);
                    margin: 0.75rem auto;
                }

                #blogBannerCropModal .modal-content {
                    padding: 14px;
                }

                #blogBannerCropModal .banner-crop-control-row {
                    grid-template-columns: 1fr;
                    gap: 6px;
                }

                #blogBannerCropModal .banner-crop-frame {
                    min-height: 170px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    onReady(function () {
        injectBannerEditorStyle();

        const form = document.getElementById("avatarForm") || document.querySelector('form[enctype="multipart/form-data"]');
        const input = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const triggerBtn = document.getElementById("blogBannerChangeBtn");
        const hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');
        const modalEl = document.getElementById("blogBannerCropModal");
        const cropImage = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const rotateBtn = document.getElementById("blogBannerRotateBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const applyBtn = document.getElementById("blogBannerApplyBtn");

        if (!form || !input || !hiddenInput || !modalEl || !cropImage || !zoomRange) {
            return;
        }

        const frame = modalEl.querySelector(".banner-crop-frame") || cropImage.parentElement;
        let bannerModal = null;
        let imageLoaded = false;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let startX = 0;
        let startY = 0;

        const state = {
            x: 0,
            y: 0,
            scale: 1,
            minScale: 1,
            rotation: 0,
            naturalWidth: 0,
            naturalHeight: 0,
        };

        if (window.bootstrap) {
            bannerModal = new bootstrap.Modal(modalEl);
        }

        function getFrameRect() {
            return frame.getBoundingClientRect();
        }

        function getRotatedBaseSize() {
            const normalized = ((state.rotation % 360) + 360) % 360;
            if (normalized === 90 || normalized === 270) {
                return {
                    width: state.naturalHeight,
                    height: state.naturalWidth,
                };
            }
            return {
                width: state.naturalWidth,
                height: state.naturalHeight,
            };
        }

        function clampPosition() {
            const rect = getFrameRect();
            const baseSize = getRotatedBaseSize();
            const renderedWidth = baseSize.width * state.scale;
            const renderedHeight = baseSize.height * state.scale;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const minX = rect.width - renderedWidth / 2;
            const maxX = renderedWidth / 2;
            const minY = rect.height - renderedHeight / 2;
            const maxY = renderedHeight / 2;

            if (minX <= maxX) {
                state.x = Math.min(Math.max(state.x, minX), maxX);
            } else {
                state.x = centerX;
            }

            if (minY <= maxY) {
                state.y = Math.min(Math.max(state.y, minY), maxY);
            } else {
                state.y = centerY;
            }
        }

        function updateImageTransform() {
            cropImage.style.width = state.naturalWidth + "px";
            cropImage.style.height = state.naturalHeight + "px";
            cropImage.style.left = "0px";
            cropImage.style.top = "0px";
            cropImage.style.transform =
                "translate(" + (state.x - state.naturalWidth / 2) + "px, " + (state.y - state.naturalHeight / 2) + "px) " +
                "rotate(" + state.rotation + "deg) " +
                "scale(" + state.scale + ")";
        }

        function calculateInitialState() {
            const rect = getFrameRect();
            const baseSize = getRotatedBaseSize();
            state.minScale = Math.max(rect.width / baseSize.width, rect.height / baseSize.height);
            state.scale = state.minScale;
            state.x = rect.width / 2;
            state.y = rect.height / 2;
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";
            clampPosition();
            updateImageTransform();
        }

        function getScaleForZoomValue(value) {
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            const zoomFactor = 1 + (safeValue / 100) * 3;
            return state.minScale * zoomFactor;
        }

        function setZoomValue(nextValue) {
            if (!imageLoaded) return;

            const currentScale = state.scale;
            const nextScale = getScaleForZoomValue(nextValue);
            const rect = getFrameRect();
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const ratio = nextScale / currentScale;

            state.x = centerX + (state.x - centerX) * ratio;
            state.y = centerY + (state.y - centerY) * ratio;
            state.scale = nextScale;
            zoomRange.value = String(Math.max(0, Math.min(100, Number(nextValue || 0))));
            clampPosition();
            updateImageTransform();
        }

        function handleZoomChange() {
            if (!imageLoaded) return;
            setZoomValue(zoomRange.value);
        }

        function drawStageToCanvas() {
            const rect = getFrameRect();
            const stageCanvas = document.createElement("canvas");
            stageCanvas.width = Math.max(1, Math.round(rect.width));
            stageCanvas.height = Math.max(1, Math.round(rect.height));
            const ctx = stageCanvas.getContext("2d");
            ctx.fillStyle = "#05080d";
            ctx.fillRect(0, 0, stageCanvas.width, stageCanvas.height);
            ctx.save();
            ctx.translate(state.x, state.y);
            ctx.rotate((state.rotation * Math.PI) / 180);
            ctx.scale(state.scale, state.scale);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(cropImage, -state.naturalWidth / 2, -state.naturalHeight / 2, state.naturalWidth, state.naturalHeight);
            ctx.restore();
            return stageCanvas;
        }

        function getCroppedCanvas() {
            if (!imageLoaded) return null;
            const stageCanvas = drawStageToCanvas();
            const outputCanvas = document.createElement("canvas");
            outputCanvas.width = 2200;
            outputCanvas.height = 900;
            const ctx = outputCanvas.getContext("2d");
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(stageCanvas, 0, 0, stageCanvas.width, stageCanvas.height, 0, 0, outputCanvas.width, outputCanvas.height);
            return outputCanvas;
        }

        function applyCropToHiddenInput() {
            const canvas = getCroppedCanvas();
            if (!canvas) return false;
            hiddenInput.value = canvas.toDataURL("image/jpeg", 0.94);
            return true;
        }

        function setupImageAfterLoad() {
            imageLoaded = true;
            state.naturalWidth = cropImage.naturalWidth;
            state.naturalHeight = cropImage.naturalHeight;
            state.rotation = 0;
            hiddenInput.value = "";
            requestAnimationFrame(calculateInitialState);
        }

        function openEditorFromFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) return;
            const reader = new FileReader();
            reader.onload = function (event) {
                imageLoaded = false;
                cropImage.src = event.target.result;
                if (bannerModal) {
                    bannerModal.show();
                }
            };
            reader.readAsDataURL(file);
        }

        if (triggerBtn) {
            triggerBtn.addEventListener("click", function () {
                input.click();
            });
        }

        input.addEventListener("change", function (event) {
            const file = event.target.files && event.target.files[0];
            if (!file) return;
            openEditorFromFile(file);
        });

        cropImage.addEventListener("load", function () {
            if (cropImage.naturalWidth > 0 && cropImage.naturalHeight > 0) {
                if (!bannerModal || modalEl.classList.contains("show")) {
                    setupImageAfterLoad();
                }
            }
        });

        modalEl.addEventListener("shown.bs.modal", function () {
            if (cropImage.complete && cropImage.naturalWidth > 0 && cropImage.naturalHeight > 0) {
                setupImageAfterLoad();
            }
        });

        zoomRange.addEventListener("input", handleZoomChange);

        frame.addEventListener("wheel", function (event) {
            if (!imageLoaded) return;
            event.preventDefault();
            const currentValue = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 4 : -4;
            const nextValue = Math.max(0, Math.min(100, currentValue + step));
            if (nextValue !== currentValue) {
                setZoomValue(nextValue);
            }
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!imageLoaded) return;
            isDragging = true;
            cropImage.classList.add("is-dragging");
            frame.setPointerCapture(event.pointerId);
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            startX = state.x;
            startY = state.y;
        });

        frame.addEventListener("pointermove", function (event) {
            if (!isDragging || !imageLoaded) return;
            state.x = startX + (event.clientX - dragStartX);
            state.y = startY + (event.clientY - dragStartY);
            clampPosition();
            updateImageTransform();
        });

        function stopDragging(event) {
            if (!isDragging) return;
            isDragging = false;
            cropImage.classList.remove("is-dragging");
            if (event && frame.hasPointerCapture(event.pointerId)) {
                frame.releasePointerCapture(event.pointerId);
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (rotateBtn) {
            rotateBtn.addEventListener("click", function () {
                if (!imageLoaded) return;
                state.rotation = (state.rotation + 90) % 360;
                calculateInitialState();
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                if (!imageLoaded) return;
                state.rotation = 0;
                calculateInitialState();
            });
        }

        if (applyBtn) {
            applyBtn.addEventListener("click", function () {
                const applied = applyCropToHiddenInput();
                if (applied && bannerModal) {
                    bannerModal.hide();
                }
            });
        }

        form.addEventListener("submit", function () {
            if (imageLoaded && !hiddenInput.value) {
                applyCropToHiddenInput();
            }
        });

        window.addEventListener("resize", function () {
            if (!imageLoaded || !modalEl.classList.contains("show")) return;
            calculateInitialState();
        });
    });
})();
'''


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def backup_file(path: Path) -> None:
    if not path.exists():
        return
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / path.relative_to(ROOT)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def remove_old_banner_preview(html: str) -> str:
    marker = "{# === Banner preview phase 4B === #}"
    if marker not in html:
        return html

    start = html.find(marker)
    next_style = html.find('<style id="avatar-editor-normal-style">', start)
    if next_style != -1:
        return html[:start].rstrip() + "\n\n" + html[next_style:]

    # Fallback: ukloni od markera do kraja ako nema avatar style bloka.
    return html[:start].rstrip() + "\n"


def patch_banner_input(html: str) -> str:
    if 'id="blogBannerInput"' in html and 'name="cropped_blog_banner"' in html:
        return html

    pattern = re.compile(r'<input\s+type="file"\s+name="blog_banner"[^>]*>', re.IGNORECASE)
    replacement = '''<input type="file" name="blog_banner" id="blogBannerInput" accept="image/*" class="form-control d-none">
<input type="hidden" name="cropped_blog_banner" id="croppedBlogBanner">
<button type="button" class="btn btn-outline-primary btn-sm" id="blogBannerChangeBtn">
    Odaberi i uredi banner
</button>'''

    html, count = pattern.subn(replacement, html, count=1)
    if count == 0:
        raise RuntimeError('Nisam našao input za blog_banner u _settings_tab.html.')
    return html


def add_banner_modal(html: str) -> str:
    if 'id="blogBannerCropModal"' in html:
        return html

    modal = '''

<div class="modal fade banner-crop-modal" id="blogBannerCropModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header border-0">
                <div>
                    <h5 class="modal-title mb-1">Uređivanje bannera</h5>
                    <div class="small text-muted">Namjestite sliku unutar pravokutnika prije spremanja.</div>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Zatvori"></button>
            </div>

            <div class="modal-body pt-0">
                <div class="banner-crop-stage">
                    <div class="banner-crop-frame">
                        <img id="blogBannerCropImage" alt="Banner preview">
                    </div>
                </div>

                <div class="banner-crop-controls mt-3">
                    <div class="banner-crop-control-row">
                        <label for="blogBannerZoomRange" class="form-label mb-0">Uvećanje</label>
                        <input type="range" id="blogBannerZoomRange" min="0" max="100" value="0" class="form-range">
                    </div>

                    <div class="d-flex flex-wrap gap-2 justify-content-between align-items-center mt-3">
                        <div class="d-flex gap-2">
                            <button type="button" class="btn btn-outline-secondary btn-sm" id="blogBannerRotateBtn">Zakreni</button>
                            <button type="button" class="btn btn-outline-secondary btn-sm" id="blogBannerResetBtn">Vrati</button>
                        </div>
                        <button type="button" class="btn btn-primary" id="blogBannerApplyBtn">Primijeni banner</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''

    anchor = '<div class="modal fade avatar-crop-modal" id="avatarCropModal"'
    if anchor not in html:
        raise RuntimeError('Nisam našao avatar modal. Ne želim ubaciti banner modal na krivo mjesto.')
    return html.replace(anchor, modal + "\n" + anchor, 1)


def add_banner_script_include(html: str) -> str:
    script_tag = "<script src=\"{% static 'blog/js/blog_settings_banner.js' %}\"></script>"
    if "blog_settings_banner.js" in html:
        return html

    avatar_style = '<style id="avatar-editor-normal-style">'
    if avatar_style in html:
        return html.replace(avatar_style, script_tag + "\n\n" + avatar_style, 1)

    close_form = "</form>"
    if close_form in html:
        return html.replace(close_form, close_form + "\n" + script_tag, 1)

    return html + "\n" + script_tag + "\n"


def main() -> None:
    if not TEMPLATE_PATH.exists():
        raise RuntimeError(f"Ne postoji: {TEMPLATE_PATH}")

    backup_file(TEMPLATE_PATH)
    backup_file(JS_SOURCE)

    html = read_text(TEMPLATE_PATH)
    html = remove_old_banner_preview(html)
    html = patch_banner_input(html)
    html = add_banner_modal(html)
    html = add_banner_script_include(html)
    write_text(TEMPLATE_PATH, html)

    js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
    write_text(js_path, BANNER_JS_CONTENT)

    print("Gotovo: dodan je pravokutni banner editor.")
    print("Promijenjeno:")
    print("- blog/templates/blog/settings/_settings_tab.html")
    print("- blog/static/blog/js/blog_settings_banner.js")
    print("Backup je u: scripts/_banner_rect_editor_backup")


if __name__ == "__main__":
    main()
