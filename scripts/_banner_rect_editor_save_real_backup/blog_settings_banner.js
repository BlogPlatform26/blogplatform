(function () {
    "use strict";

    function ready(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    ready(function () {
        const bannerInput = document.querySelector('input[name="blog_banner"]');
        if (!bannerInput) return;

        const form = bannerInput.closest("form");
        if (!form) return;

        let hiddenInput = form.querySelector('input[name="cropped_blog_banner"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        injectBannerEditorStyles();
        const modal = ensureBannerEditorModal();

        const modalEl = modal.modalEl;
        const frame = modal.frame;
        const cropRect = modal.cropRect;
        const image = modal.image;
        const zoomRange = modal.zoomRange;
        const rotateBtn = modal.rotateBtn;
        const resetBtn = modal.resetBtn;
        const applyBtn = modal.applyBtn;
        const statusText = modal.statusText;

        let bootstrapModal = null;
        if (window.bootstrap && window.bootstrap.Modal) {
            bootstrapModal = new window.bootstrap.Modal(modalEl);
        }

        let imageLoaded = false;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let startX = 0;
        let startY = 0;
        let applied = false;
        let submittingAfterApply = false;

        const state = {
            x: 0,
            y: 0,
            scale: 1,
            minScale: 1,
            rotation: 0,
            naturalWidth: 0,
            naturalHeight: 0,
            cropWidth: 660,
            cropHeight: 270,
        };

        function setStatus(text) {
            if (statusText) statusText.textContent = text || "";
        }

        function showModal() {
            if (bootstrapModal) {
                bootstrapModal.show();
            } else {
                modalEl.classList.add("show");
                modalEl.style.display = "block";
                modalEl.removeAttribute("aria-hidden");
            }
        }

        function hideModal() {
            if (bootstrapModal) {
                bootstrapModal.hide();
            } else {
                modalEl.classList.remove("show");
                modalEl.style.display = "none";
                modalEl.setAttribute("aria-hidden", "true");
            }
        }

        function getFrameRect() {
            return frame.getBoundingClientRect();
        }

        function getRotatedBaseSize() {
            const normalized = ((state.rotation % 360) + 360) % 360;
            if (normalized === 90 || normalized === 270) {
                return { width: state.naturalHeight, height: state.naturalWidth };
            }
            return { width: state.naturalWidth, height: state.naturalHeight };
        }

        function updateCropRectSize() {
            const rect = getFrameRect();
            const aspect = 22 / 9;
            const paddingX = 36;
            const paddingY = 34;
            let width = Math.max(260, rect.width - paddingX * 2);
            let height = width / aspect;

            if (height > rect.height - paddingY * 2) {
                height = Math.max(120, rect.height - paddingY * 2);
                width = height * aspect;
            }

            state.cropWidth = Math.round(width);
            state.cropHeight = Math.round(height);

            cropRect.style.width = state.cropWidth + "px";
            cropRect.style.height = state.cropHeight + "px";
            cropRect.style.left = Math.round((rect.width - state.cropWidth) / 2) + "px";
            cropRect.style.top = Math.round((rect.height - state.cropHeight) / 2) + "px";
        }

        function getCropBounds() {
            const rect = getFrameRect();
            return {
                left: (rect.width - state.cropWidth) / 2,
                top: (rect.height - state.cropHeight) / 2,
                width: state.cropWidth,
                height: state.cropHeight,
            };
        }

        function clampPosition() {
            const bounds = getCropBounds();
            const base = getRotatedBaseSize();
            const renderedWidth = base.width * state.scale;
            const renderedHeight = base.height * state.scale;

            const minX = bounds.left + bounds.width - renderedWidth / 2;
            const maxX = bounds.left + renderedWidth / 2;
            const minY = bounds.top + bounds.height - renderedHeight / 2;
            const maxY = bounds.top + renderedHeight / 2;

            if (minX <= maxX) {
                state.x = Math.min(Math.max(state.x, minX), maxX);
            } else {
                state.x = bounds.left + bounds.width / 2;
            }

            if (minY <= maxY) {
                state.y = Math.min(Math.max(state.y, minY), maxY);
            } else {
                state.y = bounds.top + bounds.height / 2;
            }
        }

        function updateImageTransform() {
            image.style.width = state.naturalWidth + "px";
            image.style.height = state.naturalHeight + "px";
            image.style.left = "0px";
            image.style.top = "0px";
            image.style.transform =
                "translate(" + (state.x - state.naturalWidth / 2) + "px, " + (state.y - state.naturalHeight / 2) + "px) " +
                "rotate(" + state.rotation + "deg) " +
                "scale(" + state.scale + ")";
        }

        function calculateInitialState() {
            updateCropRectSize();
            const bounds = getCropBounds();
            const base = getRotatedBaseSize();
            state.minScale = Math.max(bounds.width / base.width, bounds.height / base.height);
            state.scale = state.minScale;
            state.x = bounds.left + bounds.width / 2;
            state.y = bounds.top + bounds.height / 2;

            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";

            clampPosition();
            updateImageTransform();
        }

        function getScaleForZoomValue(value) {
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            return state.minScale * (1 + (safeValue / 100) * 3);
        }

        function setZoomValue(value) {
            if (!imageLoaded) return;
            const currentScale = state.scale || state.minScale;
            const nextScale = getScaleForZoomValue(value);
            const bounds = getCropBounds();
            const centerX = bounds.left + bounds.width / 2;
            const centerY = bounds.top + bounds.height / 2;
            const ratio = nextScale / currentScale;

            state.x = centerX + (state.x - centerX) * ratio;
            state.y = centerY + (state.y - centerY) * ratio;
            state.scale = nextScale;
            zoomRange.value = String(Math.max(0, Math.min(100, Number(value || 0))));
            clampPosition();
            updateImageTransform();
        }

        function drawStageToCanvas() {
            const rect = getFrameRect();
            const canvas = document.createElement("canvas");
            canvas.width = Math.max(1, Math.round(rect.width));
            canvas.height = Math.max(1, Math.round(rect.height));
            const ctx = canvas.getContext("2d");
            ctx.fillStyle = "#111827";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.save();
            ctx.translate(state.x, state.y);
            ctx.rotate((state.rotation * Math.PI) / 180);
            ctx.scale(state.scale, state.scale);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(image, -state.naturalWidth / 2, -state.naturalHeight / 2, state.naturalWidth, state.naturalHeight);
            ctx.restore();
            return canvas;
        }

        function getCroppedCanvas() {
            if (!imageLoaded) return null;
            const stageCanvas = drawStageToCanvas();
            const bounds = getCropBounds();
            const outputCanvas = document.createElement("canvas");
            outputCanvas.width = 2200;
            outputCanvas.height = 900;
            const ctx = outputCanvas.getContext("2d");
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(stageCanvas, Math.round(bounds.left), Math.round(bounds.top), Math.round(bounds.width), Math.round(bounds.height), 0, 0, outputCanvas.width, outputCanvas.height);
            return outputCanvas;
        }

        function putBlobIntoFileInput(blob) {
            try {
                const file = new File([blob], "blog_banner_cropped.jpg", { type: "image/jpeg" });
                const transfer = new DataTransfer();
                transfer.items.add(file);
                bannerInput.files = transfer.files;
                hiddenInput.value = "";
                return true;
            } catch (error) {
                return false;
            }
        }

        function applyCrop(callback) {
            const canvas = getCroppedCanvas();
            if (!canvas) {
                if (callback) callback(false);
                return;
            }
            canvas.toBlob(function (blob) {
                if (!blob) {
                    if (callback) callback(false);
                    return;
                }
                const replacedFileInput = putBlobIntoFileInput(blob);
                if (!replacedFileInput) {
                    hiddenInput.value = canvas.toDataURL("image/jpeg", 0.9);
                }
                applied = true;
                setStatus("Banner je pripremljen. Kliknite Spremi promjene.");
                if (callback) callback(true);
            }, "image/jpeg", 0.9);
        }

        function setupImageAfterLoad() {
            if (!image.naturalWidth || !image.naturalHeight) return;
            imageLoaded = true;
            applied = false;
            hiddenInput.value = "";
            state.naturalWidth = image.naturalWidth;
            state.naturalHeight = image.naturalHeight;
            state.rotation = 0;
            requestAnimationFrame(function () {
                calculateInitialState();
                setStatus("");
            });
        }

        function openEditorFromFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) return;
            const reader = new FileReader();
            reader.onload = function (event) {
                imageLoaded = false;
                applied = false;
                hiddenInput.value = "";
                image.src = event.target.result;
                showModal();
            };
            reader.readAsDataURL(file);
        }

        function addChooseButton() {
            if (document.getElementById("blogBannerEditorChooseBtn")) return;
            const btn = document.createElement("button");
            btn.type = "button";
            btn.id = "blogBannerEditorChooseBtn";
            btn.className = "btn btn-outline-primary btn-sm mt-2";
            btn.textContent = "Odaberi i uredi banner";
            btn.addEventListener("click", function () { bannerInput.click(); });
            bannerInput.insertAdjacentElement("afterend", btn);
        }

        addChooseButton();

        bannerInput.addEventListener("change", function () {
            const file = bannerInput.files && bannerInput.files[0];
            if (!file) return;
            openEditorFromFile(file);
        });

        image.addEventListener("load", function () {
            if (!bootstrapModal || modalEl.classList.contains("show")) setupImageAfterLoad();
        });

        modalEl.addEventListener("shown.bs.modal", function () {
            if (image.complete && image.naturalWidth > 0 && image.naturalHeight > 0) setupImageAfterLoad();
        });

        zoomRange.addEventListener("input", function () { setZoomValue(zoomRange.value); });

        frame.addEventListener("wheel", function (event) {
            if (!imageLoaded) return;
            event.preventDefault();
            const currentValue = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 4 : -4;
            const nextValue = Math.max(0, Math.min(100, currentValue + step));
            if (nextValue !== currentValue) setZoomValue(nextValue);
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!imageLoaded) return;
            isDragging = true;
            frame.setPointerCapture(event.pointerId);
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            startX = state.x;
            startY = state.y;
            image.classList.add("is-dragging");
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
            image.classList.remove("is-dragging");
            if (event && frame.hasPointerCapture(event.pointerId)) frame.releasePointerCapture(event.pointerId);
        }
        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        rotateBtn.addEventListener("click", function () {
            if (!imageLoaded) return;
            state.rotation = (state.rotation + 90) % 360;
            calculateInitialState();
        });

        resetBtn.addEventListener("click", function () {
            if (!imageLoaded) return;
            state.rotation = 0;
            calculateInitialState();
        });

        applyBtn.addEventListener("click", function () {
            applyCrop(function (ok) { if (ok) hideModal(); });
        });

        form.addEventListener("submit", function (event) {
            if (submittingAfterApply) return;
            const submitter = event.submitter;
            if (submitter && submitter.name === "delete_blog_banner") {
                hiddenInput.value = "";
                return;
            }
            if (imageLoaded && !applied && bannerInput.files && bannerInput.files.length) {
                event.preventDefault();
                applyCrop(function (ok) {
                    if (!ok) return;
                    submittingAfterApply = true;
                    if (form.requestSubmit) form.requestSubmit(submitter || undefined);
                    else form.submit();
                });
            }
        });

        window.addEventListener("resize", function () {
            if (!imageLoaded || !modalEl.classList.contains("show")) return;
            calculateInitialState();
        });
    });

    function ensureBannerEditorModal() {
        let modalEl = document.getElementById("blogBannerEditorModal");
        if (!modalEl) {
            modalEl = document.createElement("div");
            modalEl.id = "blogBannerEditorModal";
            modalEl.className = "modal fade blog-banner-editor-modal";
            modalEl.tabIndex = -1;
            modalEl.setAttribute("aria-hidden", "true");
            modalEl.innerHTML = '' +
                '<div class="modal-dialog modal-dialog-centered blog-banner-editor-dialog">' +
                    '<div class="modal-content">' +
                        '<div class="modal-header py-2">' +
                            '<div><h5 class="modal-title mb-0">Uređivanje bannera</h5><div class="small text-muted">Namjestite sliku unutar pravokutnika.</div></div>' +
                            '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Zatvori"></button>' +
                        '</div>' +
                        '<div class="modal-body">' +
                            '<div class="blog-banner-editor-frame"><img id="blogBannerEditorImage" alt="Banner za uređivanje"><div class="blog-banner-crop-rect"></div></div>' +
                            '<label for="blogBannerZoomRange" class="form-label small fw-semibold mt-3 mb-1">Uvećanje</label>' +
                            '<input type="range" id="blogBannerZoomRange" class="form-range" min="0" max="100" value="0">' +
                            '<div class="d-flex gap-2 mt-2 flex-wrap"><button type="button" id="blogBannerRotateBtn" class="btn btn-outline-secondary btn-sm">Zakreni</button><button type="button" id="blogBannerResetBtn" class="btn btn-outline-secondary btn-sm">Vrati</button><button type="button" id="blogBannerApplyBtn" class="btn btn-primary btn-sm ms-auto">Primijeni banner</button></div>' +
                            '<div id="blogBannerEditorStatus" class="small text-success mt-2"></div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
            document.body.appendChild(modalEl);
        }
        return {
            modalEl: modalEl,
            frame: modalEl.querySelector(".blog-banner-editor-frame"),
            cropRect: modalEl.querySelector(".blog-banner-crop-rect"),
            image: modalEl.querySelector("#blogBannerEditorImage"),
            zoomRange: modalEl.querySelector("#blogBannerZoomRange"),
            rotateBtn: modalEl.querySelector("#blogBannerRotateBtn"),
            resetBtn: modalEl.querySelector("#blogBannerResetBtn"),
            applyBtn: modalEl.querySelector("#blogBannerApplyBtn"),
            statusText: modalEl.querySelector("#blogBannerEditorStatus"),
        };
    }

    function injectBannerEditorStyles() {
        if (document.getElementById("blogBannerEditorStyles")) return;
        const style = document.createElement("style");
        style.id = "blogBannerEditorStyles";
        style.textContent = `
            .blog-banner-editor-dialog { max-width: 900px; }
            .blog-banner-editor-modal .modal-content { border-radius: 18px; overflow: hidden; }
            .blog-banner-editor-frame { position: relative; width: 100%; height: min(360px, 56vh); min-height: 250px; overflow: hidden; background: #111827; border-radius: 14px; user-select: none; touch-action: none; }
            .blog-banner-editor-frame img { position: absolute; max-width: none !important; transform-origin: center center; will-change: transform; cursor: grab; user-select: none; pointer-events: none; }
            .blog-banner-editor-frame img.is-dragging { cursor: grabbing; }
            .blog-banner-crop-rect { position: absolute; border: 2px solid #ffffff; box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.38); border-radius: 8px; pointer-events: none; z-index: 3; }
            #blogBannerApplyBtn { min-width: 140px; }
        `;
        document.head.appendChild(style);
    }
})();
