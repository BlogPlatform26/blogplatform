from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
css_path = ROOT / "blog" / "static" / "css" / "style.css"
backup_dir = ROOT / "scripts" / "_banner_modal_js_repair_backup"
backup_dir.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if js_path.exists():
    (backup_dir / f"blog_settings_banner.js.{stamp}.bak").write_text(js_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
else:
    js_path.parent.mkdir(parents=True, exist_ok=True)
    (backup_dir / f"blog_settings_banner.js.{stamp}.missing").write_text("missing", encoding="utf-8")

if css_path.exists():
    (backup_dir / f"style.css.{stamp}.bak").write_text(css_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
else:
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text("", encoding="utf-8")

banner_js = r'''(function () {
    "use strict";

    function ready(callback) {
        if (document.readyState !== "loading") {
            callback();
        } else {
            document.addEventListener("DOMContentLoaded", callback);
        }
    }

    ready(function () {
        const fileInput = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const changeBtn = document.getElementById("blogBannerChangeBtn") || document.querySelector("[data-banner-editor-open]");
        const modalEl = document.getElementById("blogBannerCropModal");
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const closeBtn = modalEl ? modalEl.querySelector(".btn-close, .banner-editor-close, [data-bs-dismiss='modal'], [data-bs-dismiss=\"modal\"]") : null;

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
            startY: 0,
        };

        function showModal() {
            modalEl.classList.add("banner-editor-open");
            modalEl.setAttribute("aria-hidden", "false");
            document.body.classList.add("modal-open");
        }

        function hideModal() {
            modalEl.classList.remove("banner-editor-open");
            modalEl.classList.remove("show");
            modalEl.setAttribute("aria-hidden", "true");
            document.body.classList.remove("modal-open");
        }

        function getFrameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, Math.round(rect.width)),
                height: Math.max(1, Math.round(rect.height)),
            };
        }

        function calculateLimits() {
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
                    window.setTimeout(resetEditor, 80);
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

            if (frame.setPointerCapture) {
                frame.setPointerCapture(event.pointerId);
            }
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

            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {
                // Nije bitno za rad editora.
            }
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

        if (closeBtn) {
            closeBtn.addEventListener("click", function (event) {
                event.preventDefault();
                hideModal();
            });
        }

        modalEl.addEventListener("click", function (event) {
            if (event.target === modalEl) {
                hideModal();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && modalEl.classList.contains("banner-editor-open")) {
                hideModal();
            }
        });

        function cropToDataUrl() {
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
            ctx.drawImage(img, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, outputWidth, outputHeight);

            return canvas.toDataURL("image/jpeg", 0.95);
        }

        applyBtn.addEventListener("click", function (event) {
            event.preventDefault();

            if (!state.loaded) {
                return;
            }

            const dataUrl = cropToDataUrl();

            if (hiddenInput) {
                hiddenInput.value = dataUrl;
            }

            hideModal();
        });

        if (form) {
            form.addEventListener("submit", function () {
                if (state.loaded && hiddenInput && !hiddenInput.value) {
                    hiddenInput.value = cropToDataUrl();
                }
            });
        }

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("banner-editor-open")) {
                resetEditor();
            }
        });

        hideModal();
    });
})();
'''

js_path.write_text(banner_js, encoding="utf-8")

css = css_path.read_text(encoding="utf-8", errors="replace")
start = "/* Banner editor repair start */"
end = "/* Banner editor repair end */"
if start in css and end in css:
    before = css.split(start)[0]
    after = css.split(end, 1)[1]
    css = before + after

repair_css = r'''
/* Banner editor repair start */
#blogBannerCropModal {
    display: none !important;
    position: fixed !important;
    inset: 0 !important;
    z-index: 1080 !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 24px !important;
    background: rgba(0, 0, 0, 0.55) !important;
    overflow: auto !important;
}

#blogBannerCropModal.banner-editor-open {
    display: flex !important;
}

#blogBannerCropModal .modal-dialog {
    width: min(1120px, 96vw) !important;
    max-width: 1120px !important;
    margin: 0 auto !important;
}

#blogBannerCropModal .modal-content {
    background: #111827 !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px !important;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35) !important;
}

#blogBannerCropModal .modal-header,
#blogBannerCropModal .modal-body,
#blogBannerCropModal .modal-footer {
    border: 0 !important;
}

#blogBannerCropFrame {
    position: relative !important;
    width: 100% !important;
    aspect-ratio: 22 / 9 !important;
    max-height: 55vh !important;
    overflow: hidden !important;
    background: #030712 !important;
    border: 2px solid rgba(255, 255, 255, 0.92) !important;
    border-radius: 16px !important;
    cursor: grab !important;
    touch-action: none !important;
}

#blogBannerCropFrame:active {
    cursor: grabbing !important;
}

#blogBannerCropImage {
    user-select: none !important;
    -webkit-user-drag: none !important;
}

#blogBannerZoomRange {
    width: 100% !important;
}
/* Banner editor repair end */
'''

css = css.rstrip() + "\n\n" + repair_css + "\n"
css_path.write_text(css, encoding="utf-8")

print("Popravljen banner JS i CSS. Backup je u scripts/_banner_modal_js_repair_backup.")
