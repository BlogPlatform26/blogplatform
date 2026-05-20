(function () {
    "use strict";

    const OUTPUT_WIDTH = 2200;
    const OUTPUT_HEIGHT = 900;
    const MAX_BYTES = 1900 * 1024;

    function ready(callback) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback);
        } else {
            callback();
        }
    }

    function findBannerButton() {
        const byId = document.getElementById("blogBannerChangeBtn");
        if (byId) return byId;

        return Array.from(document.querySelectorAll("button, a, label")).find(function (el) {
            return (el.textContent || "").trim().toLowerCase().includes("odaberi i uredi banner");
        });
    }

    function createModal() {
        document.querySelectorAll("#blogBannerCropModal").forEach(function (el) {
            el.remove();
        });

        const modal = document.createElement("div");
        modal.id = "blogBannerCropModal";
        modal.setAttribute("aria-hidden", "true");
        modal.innerHTML = `
            <div class="blog-banner-editor-dialog" role="dialog" aria-modal="true" aria-label="Uređivanje bannera">
                <div class="blog-banner-editor-header">
                    <div>
                        <h2 class="blog-banner-editor-title">Uređivanje bannera</h2>
                        <p class="blog-banner-editor-help">Namjesti pravokutni izrez prije spremanja.</p>
                    </div>
                    <button type="button" class="blog-banner-editor-close" id="blogBannerCloseBtn" aria-label="Zatvori">×</button>
                </div>

                <div id="blogBannerCropFrame">
                    <img id="blogBannerCropImage" alt="Banner preview">
                </div>

                <div class="blog-banner-editor-controls">
                    <label for="blogBannerZoomRange">Uvećanje</label>
                    <input type="range" id="blogBannerZoomRange" min="1" max="3" step="0.01" value="1">
                </div>

                <div class="blog-banner-editor-actions">
                    <button type="button" class="blog-banner-editor-btn" id="blogBannerResetBtn">Vrati</button>
                    <button type="button" class="blog-banner-editor-btn blog-banner-editor-btn-primary" id="blogBannerApplyBtn">Primijeni banner</button>
                </div>
            </div>
        `;

        const style = document.createElement("style");
        style.id = "blogBannerEditorStyle";
        style.textContent = `
            #blogBannerCropModal {
                position: fixed !important;
                inset: 0 !important;
                z-index: 30000 !important;
                display: none !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 18px !important;
                background: rgba(0, 0, 0, 0.62) !important;
            }
            #blogBannerCropModal.is-open {
                display: flex !important;
            }
            #blogBannerCropModal .blog-banner-editor-dialog {
                width: min(1040px, calc(100vw - 36px)) !important;
                max-height: calc(100vh - 36px) !important;
                overflow-y: auto !important;
                background: #111827 !important;
                color: #f8fafc !important;
                border-radius: 22px !important;
                box-shadow: 0 24px 70px rgba(0, 0, 0, 0.42) !important;
                padding: 24px !important;
                box-sizing: border-box !important;
            }
            #blogBannerCropModal .blog-banner-editor-header {
                display: flex !important;
                justify-content: space-between !important;
                gap: 16px !important;
                align-items: flex-start !important;
                margin-bottom: 16px !important;
            }
            #blogBannerCropModal .blog-banner-editor-title {
                margin: 0 0 4px 0 !important;
                font-size: 26px !important;
                line-height: 1.15 !important;
                font-weight: 700 !important;
            }
            #blogBannerCropModal .blog-banner-editor-help {
                margin: 0 !important;
                color: rgba(248, 250, 252, 0.72) !important;
                font-size: 14px !important;
            }
            #blogBannerCropModal .blog-banner-editor-close {
                border: 0 !important;
                background: transparent !important;
                color: #f8fafc !important;
                font-size: 30px !important;
                line-height: 1 !important;
                padding: 0 !important;
                width: 34px !important;
                height: 34px !important;
                cursor: pointer !important;
                opacity: 0.9 !important;
            }
            #blogBannerCropFrame {
                position: relative !important;
                width: 100% !important;
                aspect-ratio: 22 / 9 !important;
                overflow: hidden !important;
                background: #020617 !important;
                border: 2px solid rgba(248, 250, 252, 0.92) !important;
                border-radius: 18px !important;
                touch-action: none !important;
                user-select: none !important;
                cursor: grab !important;
            }
            #blogBannerCropFrame.is-dragging {
                cursor: grabbing !important;
            }
            #blogBannerCropImage {
                position: absolute !important;
                left: 0 !important;
                top: 0 !important;
                max-width: none !important;
                max-height: none !important;
                user-select: none !important;
                pointer-events: none !important;
                transform-origin: top left !important;
                display: block !important;
            }
            #blogBannerCropModal .blog-banner-editor-controls {
                margin-top: 14px !important;
                display: grid !important;
                grid-template-columns: 110px 1fr !important;
                gap: 12px !important;
                align-items: center !important;
            }
            #blogBannerCropModal .blog-banner-editor-controls label {
                margin: 0 !important;
                font-size: 15px !important;
                font-weight: 600 !important;
                color: #e5e7eb !important;
            }
            #blogBannerZoomRange {
                width: 100% !important;
            }
            #blogBannerCropModal .blog-banner-editor-actions {
                margin-top: 14px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                gap: 12px !important;
            }
            #blogBannerCropModal .blog-banner-editor-btn {
                font-size: 14px !important;
                padding: 7px 13px !important;
                border-radius: 8px !important;
                border: 1px solid rgba(248, 250, 252, 0.35) !important;
                background: transparent !important;
                color: #e5e7eb !important;
                cursor: pointer !important;
            }
            #blogBannerCropModal .blog-banner-editor-btn-primary {
                background: #0d6efd !important;
                border-color: #0d6efd !important;
                color: #fff !important;
                font-size: 15px !important;
                padding: 9px 18px !important;
            }
            @media (max-width: 700px) {
                #blogBannerCropModal {
                    padding: 10px !important;
                }
                #blogBannerCropModal .blog-banner-editor-dialog {
                    width: calc(100vw - 20px) !important;
                    padding: 18px !important;
                }
                #blogBannerCropModal .blog-banner-editor-title {
                    font-size: 22px !important;
                }
                #blogBannerCropModal .blog-banner-editor-controls {
                    grid-template-columns: 1fr !important;
                }
            }
        `;

        const oldStyle = document.getElementById("blogBannerEditorStyle");
        if (oldStyle) oldStyle.remove();

        document.head.appendChild(style);
        document.body.appendChild(modal);
        return modal;
    }

    function canvasToBlob(canvas, type, quality) {
        return new Promise(function (resolve) {
            canvas.toBlob(resolve, type, quality);
        });
    }

    async function makeSmallEnoughBlob(sourceCanvas) {
        let width = OUTPUT_WIDTH;
        let height = OUTPUT_HEIGHT;

        while (width >= 1400) {
            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext("2d");
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(sourceCanvas, 0, 0, width, height);

            for (let quality = 0.9; quality >= 0.55; quality -= 0.05) {
                const blob = await canvasToBlob(canvas, "image/jpeg", quality);
                if (blob && blob.size <= MAX_BYTES) {
                    return blob;
                }
            }

            width = Math.round(width * 0.9);
            height = Math.round(width * 9 / 22);
        }

        return canvasToBlob(sourceCanvas, "image/jpeg", 0.55);
    }

    ready(function () {
        const fileInput = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const changeBtn = findBannerButton();

        if (!fileInput || !changeBtn) {
            return;
        }

        if (!fileInput.id) {
            fileInput.id = "blogBannerInput";
        }

        const modal = createModal();
        const frame = modal.querySelector("#blogBannerCropFrame");
        const img = modal.querySelector("#blogBannerCropImage");
        const zoomRange = modal.querySelector("#blogBannerZoomRange");
        const closeBtn = modal.querySelector("#blogBannerCloseBtn");
        const resetBtn = modal.querySelector("#blogBannerResetBtn");
        const applyBtn = modal.querySelector("#blogBannerApplyBtn");

        let imageUrl = null;
        let naturalWidth = 0;
        let naturalHeight = 0;
        let minScale = 1;
        let scale = 1;
        let x = 0;
        let y = 0;
        let startX = 0;
        let startY = 0;
        let startPointerX = 0;
        let startPointerY = 0;
        let isDragging = false;
        let applied = false;

        function clampPosition() {
            const rect = frame.getBoundingClientRect();
            const renderedWidth = naturalWidth * scale;
            const renderedHeight = naturalHeight * scale;

            if (renderedWidth <= rect.width) {
                x = (rect.width - renderedWidth) / 2;
            } else {
                x = Math.min(0, Math.max(rect.width - renderedWidth, x));
            }

            if (renderedHeight <= rect.height) {
                y = (rect.height - renderedHeight) / 2;
            } else {
                y = Math.min(0, Math.max(rect.height - renderedHeight, y));
            }
        }

        function render() {
            clampPosition();
            img.style.width = `${naturalWidth * scale}px`;
            img.style.height = `${naturalHeight * scale}px`;
            img.style.transform = `translate(${x}px, ${y}px)`;
        }

        function resetImage() {
            const rect = frame.getBoundingClientRect();
            minScale = Math.max(rect.width / naturalWidth, rect.height / naturalHeight);
            zoomRange.value = "1";
            scale = minScale;
            x = (rect.width - naturalWidth * scale) / 2;
            y = (rect.height - naturalHeight * scale) / 2;
            render();
        }

        function openModal() {
            applied = false;
            modal.classList.add("is-open");
            modal.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
            setTimeout(resetImage, 30);
        }

        function closeModal(clearFile) {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
            document.body.style.overflow = "";
            frame.classList.remove("is-dragging");
            isDragging = false;

            if (clearFile && !applied) {
                fileInput.value = "";
            }
        }

        function setSelectedName(text) {
            let nameEl = document.getElementById("blogBannerSelectedName");
            if (!nameEl) {
                nameEl = document.createElement("div");
                nameEl.id = "blogBannerSelectedName";
                nameEl.className = "small text-muted mt-2";
                fileInput.insertAdjacentElement("afterend", nameEl);
            }
            nameEl.textContent = text;
        }

        changeBtn.addEventListener("click", function (event) {
            event.preventDefault();
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = fileInput.files && fileInput.files[0];
            if (!file) return;

            if (!file.type || !file.type.startsWith("image/")) {
                alert("Odaberi slikovnu datoteku.");
                fileInput.value = "";
                return;
            }

            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }

            imageUrl = URL.createObjectURL(file);
            img.onload = function () {
                naturalWidth = img.naturalWidth;
                naturalHeight = img.naturalHeight;
                openModal();
            };
            img.onerror = function () {
                alert("Slika se ne može učitati. Pokušaj drugu sliku.");
                fileInput.value = "";
            };
            img.src = imageUrl;
        });

        zoomRange.addEventListener("input", function () {
            const rect = frame.getBoundingClientRect();
            const oldScale = scale;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const zoom = Number(zoomRange.value);

            scale = minScale * zoom;
            x = centerX - ((centerX - x) / oldScale) * scale;
            y = centerY - ((centerY - y) / oldScale) * scale;
            render();
        });

        frame.addEventListener("pointerdown", function (event) {
            isDragging = true;
            frame.classList.add("is-dragging");
            frame.setPointerCapture(event.pointerId);
            startPointerX = event.clientX;
            startPointerY = event.clientY;
            startX = x;
            startY = y;
        });

        frame.addEventListener("pointermove", function (event) {
            if (!isDragging) return;
            x = startX + event.clientX - startPointerX;
            y = startY + event.clientY - startPointerY;
            render();
        });

        function stopDragging(event) {
            isDragging = false;
            frame.classList.remove("is-dragging");
            try {
                frame.releasePointerCapture(event.pointerId);
            } catch (error) {}
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", function () {
            isDragging = false;
            frame.classList.remove("is-dragging");
        });

        resetBtn.addEventListener("click", resetImage);
        closeBtn.addEventListener("click", function () {
            closeModal(true);
        });

        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                closeModal(true);
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && modal.classList.contains("is-open")) {
                closeModal(true);
            }
        });

        applyBtn.addEventListener("click", async function () {
            if (!naturalWidth || !naturalHeight) return;

            applyBtn.disabled = true;
            applyBtn.textContent = "Obrađujem...";

            try {
                const rect = frame.getBoundingClientRect();
                const canvas = document.createElement("canvas");
                canvas.width = OUTPUT_WIDTH;
                canvas.height = OUTPUT_HEIGHT;

                const ctx = canvas.getContext("2d");
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(0, 0, OUTPUT_WIDTH, OUTPUT_HEIGHT);
                ctx.imageSmoothingEnabled = true;
                ctx.imageSmoothingQuality = "high";

                const ratioX = OUTPUT_WIDTH / rect.width;
                const ratioY = OUTPUT_HEIGHT / rect.height;

                ctx.drawImage(
                    img,
                    x * ratioX,
                    y * ratioY,
                    naturalWidth * scale * ratioX,
                    naturalHeight * scale * ratioY
                );

                const blob = await makeSmallEnoughBlob(canvas);

                if (!blob) {
                    throw new Error("Canvas nije napravio sliku.");
                }

                const croppedFile = new File([blob], "blog_banner_cropped.jpg", {
                    type: "image/jpeg",
                    lastModified: Date.now()
                });

                const transfer = new DataTransfer();
                transfer.items.add(croppedFile);
                fileInput.files = transfer.files;

                applied = true;
                setSelectedName("Banner je uređen. Sada klikni Spremi promjene.");
                closeModal(false);
            } catch (error) {
                console.error(error);
                alert("Banner nije obrađen. Pokušaj ponovno s drugom slikom.");
            } finally {
                applyBtn.disabled = false;
                applyBtn.textContent = "Primijeni banner";
            }
        });

        window.addEventListener("resize", function () {
            if (modal.classList.contains("is-open") && naturalWidth && naturalHeight) {
                resetImage();
            }
        });
    });
})();
