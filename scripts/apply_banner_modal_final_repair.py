from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.cwd()
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
BACKUP_DIR = ROOT / 'scripts' / 'banner_modal_final_repair_backups' / STAMP

JS_PATH = ROOT / 'blog' / 'static' / 'blog' / 'js' / 'blog_settings_banner.js'
CSS_PATH = ROOT / 'blog' / 'static' / 'css' / 'style.css'
TPL_PATH = ROOT / 'blog' / 'templates' / 'blog' / 'settings' / '_settings_tab.html'

for p in [JS_PATH, CSS_PATH, TPL_PATH]:
    if p.exists():
        dest = BACKUP_DIR / p.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)

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
        let form = fileInput ? fileInput.closest("form") : document.querySelector("form");

        if (!fileInput || !form) {
            return;
        }

        let changeBtn = document.getElementById("blogBannerChangeBtn");

        if (!changeBtn) {
            const possibleButtons = Array.from(document.querySelectorAll("button, a, label"));
            changeBtn = possibleButtons.find(function (el) {
                return (el.textContent || "").trim().toLowerCase().includes("odaberi i uredi banner");
            });
        }

        if (!changeBtn) {
            return;
        }

        let hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        function ensureModal() {
            let modalEl = document.getElementById("blogBannerCropModal");

            if (!modalEl) {
                modalEl = document.createElement("div");
                modalEl.id = "blogBannerCropModal";
                document.body.appendChild(modalEl);
            }

            modalEl.className = "blog-banner-editor-modal";
            modalEl.setAttribute("aria-hidden", "true");
            modalEl.innerHTML = `
                <div class="blog-banner-editor-dialog" role="dialog" aria-modal="true" aria-labelledby="blogBannerEditorTitle">
                    <div class="blog-banner-editor-header">
                        <div>
                            <h3 id="blogBannerEditorTitle">Uređivanje bannera</h3>
                            <p>Namjestite pravokutni izrez prije spremanja.</p>
                        </div>
                        <button type="button" class="blog-banner-editor-close" id="blogBannerCloseBtn" aria-label="Zatvori">×</button>
                    </div>

                    <div class="blog-banner-crop-stage" id="blogBannerCropStage">
                        <div class="blog-banner-crop-frame" id="blogBannerCropFrame">
                            <img id="blogBannerCropImage" alt="Banner preview" draggable="false">
                            <div class="blog-banner-crop-border" aria-hidden="true"></div>
                        </div>
                    </div>

                    <div class="blog-banner-editor-controls">
                        <label for="blogBannerZoomRange">Uvećanje</label>
                        <input type="range" id="blogBannerZoomRange" min="0" max="100" value="0">
                    </div>

                    <div class="blog-banner-editor-actions">
                        <button type="button" class="btn btn-outline-light btn-sm" id="blogBannerResetBtn">Vrati</button>
                        <button type="button" class="btn btn-primary btn-sm" id="blogBannerApplyBtn">Primijeni banner</button>
                    </div>
                </div>
            `;

            return modalEl;
        }

        const modalEl = ensureModal();
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const closeBtn = document.getElementById("blogBannerCloseBtn");

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
            modalEl.classList.add("show");
            modalEl.setAttribute("aria-hidden", "false");
            document.body.classList.add("blog-banner-modal-open");
        }

        function hideModal() {
            modalEl.classList.remove("show");
            modalEl.setAttribute("aria-hidden", "true");
            document.body.classList.remove("blog-banner-modal-open");
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

        function exportBannerToHiddenInput() {
            if (!state.loaded) return null;

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
            hiddenInput.value = dataUrl;

            return dataUrl;
        }

        function setFileInputFromDataUrl(dataUrl) {
            fetch(dataUrl)
                .then(function (response) { return response.blob(); })
                .then(function (blob) {
                    try {
                        const file = new File([blob], "blog_banner.jpg", { type: "image/jpeg" });
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(file);
                        fileInput.files = dataTransfer.files;
                    } catch (error) {
                        // Ako browser ne dopusti promjenu file inputa, hidden input i dalje šalje crop.
                    }
                })
                .catch(function () {});
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
            const next = Math.max(0, Math.min(100, current + step));
            setZoomValue(next);
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
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {}
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                resetEditor();
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener("click", hideModal);
        }

        modalEl.addEventListener("click", function (event) {
            if (event.target === modalEl) {
                hideModal();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && modalEl.classList.contains("show")) {
                hideModal();
            }
        });

        applyBtn.addEventListener("click", function () {
            const dataUrl = exportBannerToHiddenInput();
            if (dataUrl) {
                setFileInputFromDataUrl(dataUrl);
            }
            hideModal();
        });

        form.addEventListener("submit", function () {
            if (state.loaded && !hiddenInput.value) {
                exportBannerToHiddenInput();
            }
        });

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
'''

CSS_MARKER_START = "/* BANNER_EDITOR_FINAL_REPAIR_START */"
CSS_MARKER_END = "/* BANNER_EDITOR_FINAL_REPAIR_END */"
CSS_BLOCK = r'''
/* BANNER_EDITOR_FINAL_REPAIR_START */
#blogBannerCropModal:not(.show) {
    display: none !important;
}

#blogBannerCropModal.show {
    position: fixed !important;
    inset: 0 !important;
    z-index: 1080 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 24px !important;
    background: rgba(0, 0, 0, 0.58) !important;
}

body.blog-banner-modal-open {
    overflow: hidden !important;
}

.blog-banner-editor-dialog {
    width: min(1120px, 96vw) !important;
    max-height: 94vh !important;
    overflow: auto !important;
    background: #10192b !important;
    color: #f8fafc !important;
    border-radius: 22px !important;
    padding: 24px 28px !important;
    box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45) !important;
}

.blog-banner-editor-header {
    display: flex !important;
    align-items: flex-start !important;
    justify-content: space-between !important;
    gap: 16px !important;
    margin-bottom: 16px !important;
}

.blog-banner-editor-header h3 {
    margin: 0 0 4px 0 !important;
    font-size: 26px !important;
    line-height: 1.2 !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

.blog-banner-editor-header p {
    margin: 0 !important;
    font-size: 14px !important;
    color: rgba(255, 255, 255, 0.72) !important;
}

.blog-banner-editor-close {
    border: 0 !important;
    background: transparent !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-size: 32px !important;
    line-height: 1 !important;
    padding: 0 !important;
    cursor: pointer !important;
}

.blog-banner-crop-stage {
    width: 100% !important;
    background: #050914 !important;
    border-radius: 20px !important;
    padding: 18px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.blog-banner-crop-frame {
    position: relative !important;
    width: 100% !important;
    aspect-ratio: 22 / 9 !important;
    min-height: 220px !important;
    max-height: 470px !important;
    overflow: hidden !important;
    border-radius: 16px !important;
    background: #05080f !important;
    cursor: grab !important;
}

.blog-banner-crop-frame.is-dragging {
    cursor: grabbing !important;
}

.blog-banner-crop-frame img {
    user-select: none !important;
    -webkit-user-drag: none !important;
}

.blog-banner-crop-border {
    position: absolute !important;
    inset: 0 !important;
    border: 2px solid rgba(255, 255, 255, 0.92) !important;
    border-radius: 16px !important;
    pointer-events: none !important;
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.25) !important;
}

.blog-banner-editor-controls {
    margin-top: 16px !important;
    display: grid !important;
    grid-template-columns: 110px 1fr !important;
    align-items: center !important;
    gap: 14px !important;
}

.blog-banner-editor-controls label {
    margin: 0 !important;
    color: #e5e7eb !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

.blog-banner-editor-controls input[type="range"] {
    width: 100% !important;
}

.blog-banner-editor-actions {
    margin-top: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 12px !important;
}

.blog-banner-editor-actions .btn {
    font-size: 15px !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
}

@media (max-width: 768px) {
    #blogBannerCropModal.show {
        padding: 12px !important;
    }

    .blog-banner-editor-dialog {
        padding: 18px !important;
    }

    .blog-banner-crop-stage {
        padding: 10px !important;
    }

    .blog-banner-crop-frame {
        min-height: 160px !important;
    }

    .blog-banner-editor-controls {
        grid-template-columns: 1fr !important;
    }
}
/* BANNER_EDITOR_FINAL_REPAIR_END */
'''

JS_PATH.write_text(JS_CODE, encoding='utf-8')

if CSS_PATH.exists():
    css = CSS_PATH.read_text(encoding='utf-8', errors='replace')
else:
    CSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    css = ''

pattern = re.compile(re.escape(CSS_MARKER_START) + r'.*?' + re.escape(CSS_MARKER_END), re.S)
if pattern.search(css):
    css = pattern.sub(CSS_BLOCK.strip(), css)
else:
    css = css.rstrip() + '\n\n' + CSS_BLOCK.strip() + '\n'
CSS_PATH.write_text(css, encoding='utf-8')

# Ensure template loads the banner JS once. We do not modify the rest of the banner HTML.
if TPL_PATH.exists():
    html = TPL_PATH.read_text(encoding='utf-8', errors='replace')
    if 'blog/js/blog_settings_banner.js' not in html and 'blog_settings_banner.js' not in html:
        script = '\n{% if settings_tab == \'opcenito\' %}\n<script src="{% static \'blog/js/blog_settings_banner.js\' %}"></script>\n{% endif %}\n'
        html = html.rstrip() + script
        TPL_PATH.write_text(html, encoding='utf-8')

print('Popravljen je banner editor modal i JS.')
print('Backup je spremljen u:', BACKUP_DIR)
