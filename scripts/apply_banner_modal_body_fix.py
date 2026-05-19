from pathlib import Path
from datetime import datetime

BASE = Path.cwd()
JS_PATH = BASE / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
TPL_PATH = BASE / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
BACKUP_DIR = BASE / "scripts" / "_banner_modal_body_fix_backup"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path: Path):
    if path.exists():
        target = BACKUP_DIR / f"{path.name}.{stamp}.bak"
        target.write_bytes(path.read_bytes())
        return target
    return None

backup(JS_PATH)
backup(TPL_PATH)

JS_PATH.parent.mkdir(parents=True, exist_ok=True)

JS_CODE = r'''(function () {
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
        if (!fileInput) return;

        const form = fileInput.closest("form") || document.querySelector("form");
        let hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');

        if (!hiddenInput && form) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        // Sakrij stari banner editor koji je ostao u HTML-u i zbog toga se prikazivao na dnu stranice.
        const legacyModal = document.getElementById("blogBannerCropModal");
        if (legacyModal) {
            legacyModal.setAttribute("hidden", "hidden");
            legacyModal.style.setProperty("display", "none", "important");
            legacyModal.style.setProperty("visibility", "hidden", "important");
            legacyModal.style.setProperty("height", "0", "important");
            legacyModal.style.setProperty("overflow", "hidden", "important");
        }

        let changeBtn = document.getElementById("blogBannerChangeBtn");
        if (!changeBtn) {
            const possibleButtons = Array.from(document.querySelectorAll("button, a, label"));
            changeBtn = possibleButtons.find(function (el) {
                return (el.textContent || "").trim().toLowerCase().includes("odaberi i uredi banner");
            });
        }
        if (!changeBtn) return;

        const STYLE_ID = "bpBannerEditorStyles";
        if (!document.getElementById(STYLE_ID)) {
            const style = document.createElement("style");
            style.id = STYLE_ID;
            style.textContent = `
                .bp-banner-editor-overlay {
                    position: fixed;
                    inset: 0;
                    z-index: 10850;
                    display: none;
                    align-items: center;
                    justify-content: center;
                    padding: 24px;
                    background: rgba(0, 0, 0, 0.55);
                }
                .bp-banner-editor-overlay.is-open {
                    display: flex;
                }
                .bp-banner-editor-dialog {
                    width: min(1120px, calc(100vw - 48px));
                    max-height: calc(100vh - 48px);
                    overflow: auto;
                    background: #101827;
                    color: #f8fafc;
                    border-radius: 22px;
                    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45);
                    padding: 24px 28px 22px;
                }
                .bp-banner-editor-header {
                    display: flex;
                    align-items: flex-start;
                    justify-content: space-between;
                    gap: 16px;
                    margin-bottom: 18px;
                }
                .bp-banner-editor-title {
                    margin: 0;
                    font-size: 28px;
                    line-height: 1.15;
                    font-weight: 700;
                }
                .bp-banner-editor-help {
                    margin: 6px 0 0;
                    color: rgba(248, 250, 252, 0.72);
                    font-size: 15px;
                }
                .bp-banner-editor-close {
                    border: 0;
                    background: transparent;
                    color: #f8fafc;
                    font-size: 28px;
                    line-height: 1;
                    padding: 4px 8px;
                    cursor: pointer;
                    opacity: 0.85;
                }
                .bp-banner-editor-stage-wrap {
                    background: #020617;
                    border-radius: 20px;
                    padding: 16px;
                    border: 1px solid rgba(148, 163, 184, 0.22);
                }
                .bp-banner-editor-stage {
                    position: relative;
                    width: 100%;
                    aspect-ratio: 22 / 9;
                    max-height: 52vh;
                    overflow: hidden;
                    border: 2px solid rgba(255,255,255,0.95);
                    border-radius: 14px;
                    background: #020617;
                    touch-action: none;
                    cursor: grab;
                    user-select: none;
                }
                .bp-banner-editor-stage.is-dragging {
                    cursor: grabbing;
                }
                .bp-banner-editor-stage img {
                    position: absolute;
                    left: 0;
                    top: 0;
                    max-width: none !important;
                    max-height: none !important;
                    transform-origin: top left;
                    user-select: none;
                    pointer-events: none;
                    display: block;
                }
                .bp-banner-editor-controls {
                    margin-top: 18px;
                    display: grid;
                    grid-template-columns: 120px 1fr;
                    gap: 12px;
                    align-items: center;
                }
                .bp-banner-editor-controls label {
                    margin: 0;
                    font-weight: 600;
                    font-size: 15px;
                }
                .bp-banner-editor-controls input[type="range"] {
                    width: 100%;
                }
                .bp-banner-editor-actions {
                    margin-top: 18px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                }
                .bp-banner-editor-left-actions,
                .bp-banner-editor-right-actions {
                    display: flex;
                    gap: 10px;
                    align-items: center;
                }
                .bp-banner-editor-btn {
                    border: 1px solid rgba(148, 163, 184, 0.55);
                    background: transparent;
                    color: #f8fafc;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-size: 15px;
                    cursor: pointer;
                }
                .bp-banner-editor-btn-primary {
                    border-color: #0d6efd;
                    background: #0d6efd;
                    color: #fff;
                    padding-left: 20px;
                    padding-right: 20px;
                }
                body.bp-banner-editor-open {
                    overflow: hidden;
                }
                @media (max-width: 768px) {
                    .bp-banner-editor-dialog {
                        padding: 18px;
                    }
                    .bp-banner-editor-title {
                        font-size: 23px;
                    }
                    .bp-banner-editor-controls {
                        grid-template-columns: 1fr;
                    }
                    .bp-banner-editor-actions {
                        flex-direction: column;
                        align-items: stretch;
                    }
                    .bp-banner-editor-left-actions,
                    .bp-banner-editor-right-actions {
                        justify-content: stretch;
                    }
                    .bp-banner-editor-btn {
                        width: 100%;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        let overlay = document.getElementById("bpBannerEditorOverlay");
        if (!overlay) {
            overlay = document.createElement("div");
            overlay.id = "bpBannerEditorOverlay";
            overlay.className = "bp-banner-editor-overlay";
            overlay.innerHTML = `
                <div class="bp-banner-editor-dialog" role="dialog" aria-modal="true" aria-labelledby="bpBannerEditorTitle">
                    <div class="bp-banner-editor-header">
                        <div>
                            <h2 class="bp-banner-editor-title" id="bpBannerEditorTitle">Uređivanje bannera</h2>
                            <p class="bp-banner-editor-help">Namjestite pravokutni izrez prije spremanja.</p>
                        </div>
                        <button type="button" class="bp-banner-editor-close" id="bpBannerEditorClose" aria-label="Zatvori">×</button>
                    </div>
                    <div class="bp-banner-editor-stage-wrap">
                        <div class="bp-banner-editor-stage" id="bpBannerEditorStage">
                            <img id="bpBannerEditorImage" alt="Banner preview">
                        </div>
                    </div>
                    <div class="bp-banner-editor-controls">
                        <label for="bpBannerEditorZoom">Uvećanje</label>
                        <input type="range" id="bpBannerEditorZoom" min="0" max="100" value="0">
                    </div>
                    <div class="bp-banner-editor-actions">
                        <div class="bp-banner-editor-left-actions">
                            <button type="button" class="bp-banner-editor-btn" id="bpBannerEditorReset">Vrati</button>
                        </div>
                        <div class="bp-banner-editor-right-actions">
                            <button type="button" class="bp-banner-editor-btn bp-banner-editor-btn-primary" id="bpBannerEditorApply">Primijeni banner</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);
        }

        const closeBtn = document.getElementById("bpBannerEditorClose");
        const stage = document.getElementById("bpBannerEditorStage");
        const image = document.getElementById("bpBannerEditorImage");
        const zoomRange = document.getElementById("bpBannerEditorZoom");
        const resetBtn = document.getElementById("bpBannerEditorReset");
        const applyBtn = document.getElementById("bpBannerEditorApply");

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

        function openOverlay() {
            overlay.classList.add("is-open");
            document.body.classList.add("bp-banner-editor-open");
        }

        function closeOverlay() {
            overlay.classList.remove("is-open");
            document.body.classList.remove("bp-banner-editor-open");
        }

        function getStageSize() {
            const rect = stage.getBoundingClientRect();
            return {
                width: Math.max(1, Math.round(rect.width)),
                height: Math.max(1, Math.round(rect.height))
            };
        }

        function calculateLimits() {
            const size = getStageSize();
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
            const size = getStageSize();
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
            image.style.width = state.naturalWidth + "px";
            image.style.height = state.naturalHeight + "px";
            image.style.transform = "translate(" + state.x + "px, " + state.y + "px) scale(" + state.scale + ")";
        }

        function resetEditor() {
            if (!state.loaded) return;
            calculateLimits();
            state.scale = state.minScale;
            const size = getStageSize();
            state.x = (size.width - state.naturalWidth * state.scale) / 2;
            state.y = (size.height - state.naturalHeight * state.scale) / 2;
            zoomRange.value = "0";
            render();
        }

        function setZoomValue(value) {
            if (!state.loaded) return;
            const oldScale = state.scale;
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            const ratio = safeValue / 100;
            const nextScale = state.minScale + (state.maxScale - state.minScale) * ratio;
            const size = getStageSize();
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

        function loadFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) return;
            if (hiddenInput) hiddenInput.value = "";

            const reader = new FileReader();
            reader.onload = function (event) {
                image.onload = function () {
                    state.loaded = true;
                    state.naturalWidth = image.naturalWidth;
                    state.naturalHeight = image.naturalHeight;
                    openOverlay();
                    window.setTimeout(resetEditor, 50);
                };
                image.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }

        function setFileInputFromBlob(blob) {
            try {
                const file = new File([blob], "blog_banner.png", { type: "image/png" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
            } catch (error) {
                // Hidden input je dovoljan ako browser ne dopušta postavljanje file inputa.
            }
        }

        function applyBanner() {
            if (!state.loaded) return;

            const size = getStageSize();
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
            ctx.clearRect(0, 0, outputWidth, outputHeight);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(
                image,
                sourceX,
                sourceY,
                sourceWidth,
                sourceHeight,
                0,
                0,
                outputWidth,
                outputHeight
            );

            const dataUrl = canvas.toDataURL("image/png");
            if (hiddenInput) hiddenInput.value = dataUrl;

            canvas.toBlob(function (blob) {
                if (blob) setFileInputFromBlob(blob);
                closeOverlay();
            }, "image/png");
        }

        changeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();
            if (event.stopImmediatePropagation) event.stopImmediatePropagation();
            fileInput.click();
        }, true);

        fileInput.addEventListener("change", function () {
            const file = fileInput.files && fileInput.files[0];
            loadFile(file);
        });

        zoomRange.addEventListener("input", function () {
            setZoomValue(zoomRange.value);
        });

        stage.addEventListener("wheel", function (event) {
            if (!state.loaded) return;
            event.preventDefault();
            const current = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            const next = Math.max(0, Math.min(100, current + step));
            setZoomValue(next);
        }, { passive: false });

        stage.addEventListener("pointerdown", function (event) {
            if (!state.loaded) return;
            state.dragging = true;
            state.dragStartX = event.clientX;
            state.dragStartY = event.clientY;
            state.startX = state.x;
            state.startY = state.y;
            stage.classList.add("is-dragging");
            stage.setPointerCapture(event.pointerId);
        });

        stage.addEventListener("pointermove", function (event) {
            if (!state.dragging || !state.loaded) return;
            state.x = state.startX + (event.clientX - state.dragStartX);
            state.y = state.startY + (event.clientY - state.dragStartY);
            render();
        });

        function stopDragging(event) {
            if (!state.dragging) return;
            state.dragging = false;
            stage.classList.remove("is-dragging");
            try {
                if (event && stage.hasPointerCapture && stage.hasPointerCapture(event.pointerId)) {
                    stage.releasePointerCapture(event.pointerId);
                }
            } catch (error) {}
        }

        stage.addEventListener("pointerup", stopDragging);
        stage.addEventListener("pointercancel", stopDragging);
        stage.addEventListener("pointerleave", stopDragging);

        if (resetBtn) resetBtn.addEventListener("click", resetEditor);
        if (applyBtn) applyBtn.addEventListener("click", applyBanner);
        if (closeBtn) closeBtn.addEventListener("click", closeOverlay);

        overlay.addEventListener("click", function (event) {
            if (event.target === overlay) closeOverlay();
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && overlay.classList.contains("is-open")) {
                closeOverlay();
            }
        });
    });
})();
'''

JS_PATH.write_text(JS_CODE, encoding="utf-8")

if TPL_PATH.exists():
    html = TPL_PATH.read_text(encoding="utf-8", errors="replace")
    if "blog_settings_banner.js" not in html:
        html += '\n{% if settings_tab == \'opcenito\' %}<script src="{% static \'blog/js/blog_settings_banner.js\' %}"></script>{% endif %}\n'
        TPL_PATH.write_text(html, encoding="utf-8")

print("Banner modal je očišćen. Stari editor se skriva, novi editor se otvara kroz JS.")
print("Backup je u scripts/_banner_modal_body_fix_backup")
