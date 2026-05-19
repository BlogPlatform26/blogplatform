from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
css_path = ROOT / "blog" / "static" / "css" / "style.css"
backup_dir = ROOT / "scripts" / "_banner_modal_hard_reset_backup"
backup_dir.mkdir(parents=True, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path: Path):
    if path.exists():
        target = backup_dir / f"{path.name}.{stamp}.bak"
        target.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

backup(js_path)
backup(css_path)

js_path.parent.mkdir(parents=True, exist_ok=True)
css_path.parent.mkdir(parents=True, exist_ok=True)

js_code = r'''(function () {
    "use strict";

    function ready(fn) {
        if (document.readyState !== "loading") {
            fn();
        } else {
            document.addEventListener("DOMContentLoaded", fn);
        }
    }

    function findButtonByText(text) {
        const wanted = text.trim().toLowerCase();
        const items = Array.from(document.querySelectorAll("button, a, label"));
        return items.find(function (el) {
            return (el.textContent || "").trim().toLowerCase().includes(wanted);
        }) || null;
    }

    ready(function () {
        const fileInput = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const changeBtn = document.getElementById("blogBannerChangeBtn") || findButtonByText("Odaberi i uredi banner");
        const modalEl = document.getElementById("blogBannerCropModal");
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const form = fileInput ? (fileInput.closest("form") || document.querySelector("form")) : document.querySelector("form");

        if (!fileInput || !changeBtn || !modalEl || !frame || !img || !zoomRange || !applyBtn || !form) {
            console.warn("Banner editor nije pokrenut jer nedostaje HTML element.", {
                fileInput: !!fileInput,
                changeBtn: !!changeBtn,
                modalEl: !!modalEl,
                frame: !!frame,
                img: !!img,
                zoomRange: !!zoomRange,
                applyBtn: !!applyBtn,
                form: !!form
            });
            return;
        }

        let hiddenInput = document.getElementById("croppedBlogBanner") || form.querySelector('input[name="cropped_blog_banner"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        document.body.appendChild(modalEl);
        modalEl.classList.add("bp-banner-crop-modal");
        modalEl.classList.remove("show", "d-block", "bp-banner-open");
        modalEl.setAttribute("aria-hidden", "true");
        modalEl.style.display = "none";

        const closeBtn = modalEl.querySelector('[data-bs-dismiss="modal"], .btn-close, .blog-banner-close, .banner-modal-close, [aria-label="Close"], [aria-label="Zatvori"]');

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
            modalEl.classList.add("bp-banner-open");
            modalEl.setAttribute("aria-hidden", "false");
            modalEl.style.display = "flex";
            document.body.classList.add("bp-banner-modal-open");
        }

        function hideModal() {
            modalEl.classList.remove("bp-banner-open");
            modalEl.setAttribute("aria-hidden", "true");
            modalEl.style.display = "none";
            document.body.classList.remove("bp-banner-modal-open");
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
            state.minScale = Math.max(size.width / state.naturalWidth, size.height / state.naturalHeight);
            if (!Number.isFinite(state.minScale) || state.minScale <= 0) state.minScale = 1;
            state.maxScale = state.minScale * 4;
        }

        function clampPosition() {
            const size = getFrameSize();
            const scaledWidth = state.naturalWidth * state.scale;
            const scaledHeight = state.naturalHeight * state.scale;
            state.x = scaledWidth <= size.width ? (size.width - scaledWidth) / 2 : Math.min(0, Math.max(size.width - scaledWidth, state.x));
            state.y = scaledHeight <= size.height ? (size.height - scaledHeight) / 2 : Math.min(0, Math.max(size.height - scaledHeight, state.y));
        }

        function render() {
            if (!state.loaded) return;
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
            if (!state.loaded) return;
            calculateLimits();
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
            hiddenInput.value = "";
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

        function setFileInputFromBlob(blob) {
            try {
                const file = new File([blob], "blog_banner.jpg", { type: "image/jpeg" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
            } catch (error) {}
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

        zoomRange.addEventListener("input", function () { setZoomValue(zoomRange.value); });

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
            frame.classList.add("is-dragging");
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
            frame.classList.remove("is-dragging");
            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) frame.releasePointerCapture(event.pointerId);
            } catch (error) {}
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (resetBtn) resetBtn.addEventListener("click", function (event) { event.preventDefault(); resetEditor(); });
        if (closeBtn) closeBtn.addEventListener("click", function (event) { event.preventDefault(); hideModal(); });

        modalEl.addEventListener("click", function (event) { if (event.target === modalEl) hideModal(); });
        document.addEventListener("keydown", function (event) { if (event.key === "Escape" && modalEl.classList.contains("bp-banner-open")) hideModal(); });

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
            ctx.drawImage(img, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, outputWidth, outputHeight);
            const dataUrl = canvas.toDataURL("image/jpeg", 0.94);
            hiddenInput.value = dataUrl;
            canvas.toBlob(function (blob) {
                if (blob) setFileInputFromBlob(blob);
                hideModal();
            }, "image/jpeg", 0.94);
        });

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("bp-banner-open")) resetEditor();
        });
    });
})();
'''

js_path.write_text(js_code, encoding="utf-8")

css_marker_start = "/* Banner modal hard reset - start */"
css_marker_end = "/* Banner modal hard reset - end */"
css = css_path.read_text(encoding="utf-8", errors="replace") if css_path.exists() else ""
start = css.find(css_marker_start)
end = css.find(css_marker_end)
if start != -1 and end != -1:
    css = css[:start] + css[end + len(css_marker_end):]

css_block = r'''
/* Banner modal hard reset - start */
body.bp-banner-modal-open { overflow: hidden !important; }

#blogBannerCropModal {
    display: none !important;
    position: fixed !important;
    inset: 0 !important;
    z-index: 99999 !important;
    width: 100vw !important;
    height: 100vh !important;
    max-width: none !important;
    max-height: none !important;
    margin: 0 !important;
    padding: 18px !important;
    overflow: auto !important;
    background: rgba(0, 0, 0, 0.58) !important;
    box-sizing: border-box !important;
}

#blogBannerCropModal.bp-banner-open {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

#blogBannerCropModal .modal-dialog,
#blogBannerCropModal .modal-content,
#blogBannerCropModal .banner-crop-content,
#blogBannerCropModal .blog-banner-crop-content {
    max-width: min(1180px, calc(100vw - 48px)) !important;
    width: 100% !important;
    max-height: calc(100vh - 48px) !important;
    overflow: auto !important;
    margin: 0 auto !important;
    border-radius: 22px !important;
    background: #0f172a !important;
    color: #f8fafc !important;
    box-sizing: border-box !important;
}

#blogBannerCropFrame {
    position: relative !important;
    width: min(1060px, calc(100vw - 120px)) !important;
    aspect-ratio: 22 / 9 !important;
    height: auto !important;
    max-height: 58vh !important;
    overflow: hidden !important;
    margin-left: auto !important;
    margin-right: auto !important;
    background: #020617 !important;
    border: 2px solid rgba(255,255,255,.9) !important;
    border-radius: 16px !important;
    cursor: grab !important;
    box-sizing: border-box !important;
}

#blogBannerCropFrame.is-dragging { cursor: grabbing !important; }

#blogBannerCropImage {
    user-select: none !important;
    -webkit-user-drag: none !important;
    pointer-events: none !important;
}

#blogBannerZoomRange { width: min(860px, 100%) !important; }

#blogBannerApplyBtn,
#blogBannerResetBtn {
    font-size: 15px !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
}
/* Banner modal hard reset - end */
'''
css = css.rstrip() + "\n\n" + css_block + "\n"
css_path.write_text(css, encoding="utf-8")

print("Banner modal hard reset primijenjen.")
