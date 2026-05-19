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
