from pathlib import Path

BASE = Path.cwd()
js_path = BASE / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
tpl_path = BASE / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

if not js_path.parent.exists():
    js_path.parent.mkdir(parents=True, exist_ok=True)

backup_dir = BASE / "scripts" / "_banner_final_modal_backups"
backup_dir.mkdir(parents=True, exist_ok=True)

if js_path.exists():
    (backup_dir / "blog_settings_banner.js.bak").write_text(js_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
if tpl_path.exists():
    (backup_dir / "_settings_tab.html.bak").write_text(tpl_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

# Čisti, samostalan banner editor. Ne koristi stari HTML editor iz templatea.
js_code = r'''(function () {
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
        const changeBtn = document.getElementById("blogBannerChangeBtn") || Array.from(document.querySelectorAll("button, a, label")).find(function (el) {
            return (el.textContent || "").trim().toLowerCase().includes("odaberi i uredi banner");
        });

        if (!fileInput || !changeBtn) {
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

        function removeLegacyBannerEditors() {
            document.querySelectorAll("#blogBannerCropModal, #blogBannerEditorModal, .blog-banner-crop-modal, .blog-banner-editor-modal, .banner-crop-modal, .banner-editor-modal").forEach(function (el) {
                el.remove();
            });

            const headings = Array.from(document.querySelectorAll("h1, h2, h3, h4, h5, h6"));
            headings.forEach(function (heading) {
                const title = (heading.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
                if (title !== "uređivanje bannera") {
                    return;
                }

                let node = heading;
                while (node) {
                    const next = node.nextElementSibling;
                    const text = (node.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
                    node.remove();

                    if (!next) {
                        break;
                    }

                    const nextText = (next.textContent || "").replace(/\s+/g, " ").trim().toLowerCase();
                    if (next.matches("h1, h2, h3, h4, h5, h6") || nextText.includes("uređivanje avatara")) {
                        break;
                    }

                    node = next;
                }
            });
        }

        removeLegacyBannerEditors();

        const style = document.createElement("style");
        style.textContent = `
            #bpBannerModal {
                position: fixed !important;
                inset: 0 !important;
                z-index: 20000 !important;
                display: none !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 18px !important;
                background: rgba(0, 0, 0, 0.58) !important;
            }

            #bpBannerModal.bp-open {
                display: flex !important;
            }

            #bpBannerModal .bp-dialog {
                width: min(980px, calc(100vw - 36px)) !important;
                max-height: calc(100vh - 36px) !important;
                overflow-y: auto !important;
                background: #111827 !important;
                color: #f8fafc !important;
                border-radius: 22px !important;
                box-shadow: 0 24px 70px rgba(0,0,0,.42) !important;
                padding: 22px !important;
            }

            #bpBannerModal .bp-header {
                display: flex !important;
                align-items: flex-start !important;
                justify-content: space-between !important;
                gap: 16px !important;
                margin-bottom: 14px !important;
            }

            #bpBannerModal .bp-title {
                font-size: 26px !important;
                line-height: 1.15 !important;
                margin: 0 0 5px 0 !important;
                font-weight: 700 !important;
            }

            #bpBannerModal .bp-help {
                margin: 0 !important;
                color: rgba(248,250,252,.72) !important;
                font-size: 14px !important;
            }

            #bpBannerModal .bp-close {
                border: 0 !important;
                background: transparent !important;
                color: #f8fafc !important;
                font-size: 26px !important;
                line-height: 1 !important;
                padding: 0 !important;
                width: 30px !important;
                height: 30px !important;
                cursor: pointer !important;
                opacity: .85 !important;
            }

            #bpBannerFrame {
                position: relative !important;
                width: 100% !important;
                aspect-ratio: 22 / 9 !important;
                overflow: hidden !important;
                background: #020617 !important;
                border: 2px solid rgba(248,250,252,.92) !important;
                border-radius: 16px !important;
                touch-action: none !important;
                user-select: none !important;
                cursor: grab !important;
            }

            #bpBannerFrame.bp-dragging {
                cursor: grabbing !important;
            }

            #bpBannerImage {
                position: absolute !important;
                left: 0 !important;
                top: 0 !important;
                max-width: none !important;
                max-height: none !important;
                user-select: none !important;
                pointer-events: none !important;
                display: none !important;
                transform-origin: top left !important;
            }

            #bpBannerModal .bp-controls {
                margin-top: 14px !important;
                display: grid !important;
                grid-template-columns: 110px 1fr !important;
                align-items: center !important;
                gap: 12px !important;
            }

            #bpBannerModal .bp-controls label {
                margin: 0 !important;
                font-weight: 600 !important;
                color: #e5e7eb !important;
                font-size: 15px !important;
            }

            #bpBannerZoom {
                width: 100% !important;
            }

            #bpBannerModal .bp-actions {
                margin-top: 14px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                gap: 10px !important;
            }

            #bpBannerModal .bp-btn {
                font-size: 14px !important;
                padding: 7px 13px !important;
                border-radius: 8px !important;
                border: 1px solid rgba(248,250,252,.35) !important;
                background: transparent !important;
                color: #e5e7eb !important;
                cursor: pointer !important;
            }

            #bpBannerModal .bp-btn-primary {
                background: #0d6efd !important;
                border-color: #0d6efd !important;
                color: #fff !important;
                font-size: 15px !important;
                padding: 9px 20px !important;
            }

            @media (max-width: 700px) {
                #bpBannerModal { padding: 10px !important; }
                #bpBannerModal .bp-dialog { width: calc(100vw - 20px) !important; padding: 16px !important; }
                #bpBannerModal .bp-title { font-size: 22px !important; }
                #bpBannerModal .bp-controls { grid-template-columns: 1fr !important; }
                #bpBannerModal .bp-actions { flex-direction: column !important; align-items: stretch !important; }
            }
        `;
        document.head.appendChild(style);

        const modal = document.createElement("div");
        modal.id = "bpBannerModal";
        modal.setAttribute("aria-hidden", "true");
        modal.innerHTML = `
            <div class="bp-dialog" role="dialog" aria-modal="true" aria-label="Uređivanje bannera">
                <div class="bp-header">
                    <div>
                        <h3 class="bp-title">Uređivanje bannera</h3>
                        <p class="bp-help">Namjestite pravokutni izrez prije spremanja.</p>
                    </div>
                    <button type="button" class="bp-close" id="bpBannerClose" aria-label="Zatvori">×</button>
                </div>

                <div id="bpBannerFrame">
                    <img id="bpBannerImage" alt="Banner preview">
                </div>

                <div class="bp-controls">
                    <label for="bpBannerZoom">Uvećanje</label>
                    <input type="range" id="bpBannerZoom" min="0" max="100" value="0">
                </div>

                <div class="bp-actions">
                    <button type="button" class="bp-btn" id="bpBannerReset">Vrati</button>
                    <button type="button" class="bp-btn bp-btn-primary" id="bpBannerApply">Primijeni banner</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        const frame = document.getElementById("bpBannerFrame");
        const img = document.getElementById("bpBannerImage");
        const zoom = document.getElementById("bpBannerZoom");
        const closeBtn = document.getElementById("bpBannerClose");
        const resetBtn = document.getElementById("bpBannerReset");
        const applyBtn = document.getElementById("bpBannerApply");

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

        function openModal() {
            modal.classList.add("bp-open");
            modal.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        }

        function closeModal() {
            modal.classList.remove("bp-open");
            modal.setAttribute("aria-hidden", "true");
            document.body.style.overflow = "";
        }

        function frameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, Math.round(rect.width)),
                height: Math.max(1, Math.round(rect.height))
            };
        }

        function calculateScale() {
            const size = frameSize();

            // Banner kreće tako da se vidi cijela slika ako je moguće.
            // Ako korisnik želi više popuniti prostor, koristi zoom.
            state.minScale = Math.min(size.width / state.naturalWidth, size.height / state.naturalHeight);

            if (!Number.isFinite(state.minScale) || state.minScale <= 0) {
                state.minScale = 1;
            }

            state.maxScale = state.minScale * 5;
        }

        function clampPosition() {
            const size = frameSize();
            const scaledW = state.naturalWidth * state.scale;
            const scaledH = state.naturalHeight * state.scale;

            if (scaledW <= size.width) {
                state.x = (size.width - scaledW) / 2;
            } else {
                state.x = Math.min(0, Math.max(size.width - scaledW, state.x));
            }

            if (scaledH <= size.height) {
                state.y = (size.height - scaledH) / 2;
            } else {
                state.y = Math.min(0, Math.max(size.height - scaledH, state.y));
            }
        }

        function render() {
            if (!state.loaded) return;
            clampPosition();
            img.style.display = "block";
            img.style.width = state.naturalWidth + "px";
            img.style.height = state.naturalHeight + "px";
            img.style.transform = "translate(" + state.x + "px, " + state.y + "px) scale(" + state.scale + ")";
        }

        function resetEditor() {
            if (!state.loaded) return;
            calculateScale();
            state.scale = state.minScale;
            const size = frameSize();
            state.x = (size.width - state.naturalWidth * state.scale) / 2;
            state.y = (size.height - state.naturalHeight * state.scale) / 2;
            zoom.value = "0";
            render();
        }

        function setZoom(value) {
            if (!state.loaded) return;

            const safe = Math.max(0, Math.min(100, Number(value || 0)));
            const oldScale = state.scale;
            const ratio = safe / 100;
            const nextScale = state.minScale + (state.maxScale - state.minScale) * ratio;
            const size = frameSize();
            const centerX = size.width / 2;
            const centerY = size.height / 2;
            const imageX = (centerX - state.x) / oldScale;
            const imageY = (centerY - state.y) / oldScale;

            state.scale = nextScale;
            state.x = centerX - imageX * state.scale;
            state.y = centerY - imageY * state.scale;
            zoom.value = String(safe);
            render();
        }

        function openFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) return;

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
                    openModal();
                    window.requestAnimationFrame(function () {
                        window.requestAnimationFrame(resetEditor);
                    });
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }

        function cropToDataUrl() {
            const size = frameSize();
            const outputW = 2200;
            const outputH = 900;
            const scaleX = outputW / size.width;
            const scaleY = outputH / size.height;
            const canvas = document.createElement("canvas");
            canvas.width = outputW;
            canvas.height = outputH;
            const ctx = canvas.getContext("2d");

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, outputW, outputH);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";

            ctx.drawImage(
                img,
                state.x * scaleX,
                state.y * scaleY,
                state.naturalWidth * state.scale * scaleX,
                state.naturalHeight * state.scale * scaleY
            );

            return canvas.toDataURL("image/jpeg", 0.96);
        }

        function applyBanner() {
            if (!state.loaded) return;

            const dataUrl = cropToDataUrl();
            if (hiddenInput) {
                hiddenInput.value = dataUrl;
            }

            closeModal();
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

        closeBtn.addEventListener("click", closeModal);
        resetBtn.addEventListener("click", resetEditor);
        applyBtn.addEventListener("click", applyBanner);
        zoom.addEventListener("input", function () {
            setZoom(zoom.value);
        });

        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                closeModal();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && modal.classList.contains("bp-open")) {
                closeModal();
            }
        });

        frame.addEventListener("wheel", function (event) {
            if (!state.loaded) return;
            event.preventDefault();
            const current = Number(zoom.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            setZoom(Math.max(0, Math.min(100, current + step)));
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!state.loaded) return;
            state.dragging = true;
            state.dragStartX = event.clientX;
            state.dragStartY = event.clientY;
            state.startX = state.x;
            state.startY = state.y;
            frame.classList.add("bp-dragging");
            frame.setPointerCapture(event.pointerId);
        });

        frame.addEventListener("pointermove", function (event) {
            if (!state.dragging || !state.loaded) return;
            state.x = state.startX + (event.clientX - state.dragStartX);
            state.y = state.startY + (event.clientY - state.dragStartY);
            render();
        });

        function stopDrag(event) {
            if (!state.dragging) return;
            state.dragging = false;
            frame.classList.remove("bp-dragging");
            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {}
        }

        frame.addEventListener("pointerup", stopDrag);
        frame.addEventListener("pointercancel", stopDrag);
        frame.addEventListener("pointerleave", stopDrag);

        if (form) {
            form.addEventListener("submit", function () {
                if (state.loaded && hiddenInput && !hiddenInput.value) {
                    hiddenInput.value = cropToDataUrl();
                }
            });
        }

        window.addEventListener("resize", function () {
            if (state.loaded && modal.classList.contains("bp-open")) {
                resetEditor();
            }
        });
    });
})();
'''

js_path.write_text(js_code, encoding="utf-8")

# Ako template ne učitava banner JS, dodaj ga. Ovo ne dira avatar.
if tpl_path.exists():
    tpl = tpl_path.read_text(encoding="utf-8", errors="replace")
    script_line = "<script src=\"{% static 'blog/js/blog_settings_banner.js' %}\"></script>"
    if "blog_settings_banner.js" not in tpl:
        marker = "{% if settings_tab == 'opcenito' %}"
        # Dodaj na kraj templatea unutar jednostavnog uvjeta.
        tpl = tpl.rstrip() + "\n{% if settings_tab == 'opcenito' %}\n" + script_line + "\n{% endif %}\n"
        tpl_path.write_text(tpl, encoding="utf-8")

print("Banner modal JS je zamijenjen čistom verzijom. Stari banner editor se uklanja iz prikaza preko JS-a.")
