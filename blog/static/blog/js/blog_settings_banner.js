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
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");

        if (!fileInput || !changeBtn || !modalEl || !frame || !img || !zoomRange || !applyBtn) {
            return;
        }

        let form = fileInput.closest("form") || document.querySelector("form");
        let hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');

        if (!hiddenInput && form) {
            hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "cropped_blog_banner";
            hiddenInput.id = "croppedBlogBanner";
            form.appendChild(hiddenInput);
        }

        let modal = null;
        if (window.bootstrap && window.bootstrap.Modal) {
            modal = new window.bootstrap.Modal(modalEl);
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
            startY: 0
        };

        let sourceDataUrl = "";

        function showModal() {
            if (modal) {
                modal.show();
            } else {
                modalEl.style.display = "block";
                modalEl.classList.add("show");
                document.body.classList.add("modal-open");
            }
        }

        function hideModal() {
            if (modal) {
                modal.hide();
            } else {
                modalEl.classList.remove("show");
                modalEl.style.display = "none";
                document.body.classList.remove("modal-open");
            }
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

            img.style.setProperty("display", "block", "important");
            img.style.setProperty("position", "absolute", "important");
            img.style.setProperty("left", "0px", "important");
            img.style.setProperty("top", "0px", "important");
            img.style.setProperty("max-width", "none", "important");
            img.style.setProperty("max-height", "none", "important");
            img.style.setProperty("width", state.naturalWidth + "px", "important");
            img.style.setProperty("height", state.naturalHeight + "px", "important");
            img.style.setProperty("transform-origin", "top left", "important");
            img.style.setProperty("transform", "translate(" + state.x + "px, " + state.y + "px) scale(" + state.scale + ")", "important");
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
            if (!file || !file.type || !file.type.startsWith("image/")) return;

            if (hiddenInput) {
                hiddenInput.value = "";
            }

            const reader = new FileReader();

            reader.onload = function (event) {
                sourceDataUrl = event.target.result;
                state.loaded = false;

                img.onload = function () {
                    state.naturalWidth = img.naturalWidth;
                    state.naturalHeight = img.naturalHeight;
                    state.loaded = true;

                    showModal();

                    // Bootstrap modal ima mali delay. Zato reset ide nakon prikaza.
                    window.setTimeout(resetEditor, 120);
                };

                img.src = sourceDataUrl;
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
            img.classList.add("is-dragging");
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
            img.classList.remove("is-dragging");

            try {
                if (event && frame.hasPointerCapture && frame.hasPointerCapture(event.pointerId)) {
                    frame.releasePointerCapture(event.pointerId);
                }
            } catch (error) {
                // nije važno
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                resetEditor();
            });
        }

        function setFileInputFromBlob(blob) {
            try {
                const file = new File([blob], "blog_banner.jpg", { type: "image/jpeg" });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;
            } catch (error) {
                // Ako browser ne dopušta postavljanje file inputa, hidden input i dalje šalje banner.
            }
        }

        applyBtn.addEventListener("click", function () {
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

            const dataUrl = canvas.toDataURL("image/jpeg", 0.9);

            if (hiddenInput) {
                hiddenInput.value = dataUrl;
            }

            canvas.toBlob(function (blob) {
                if (blob) {
                    setFileInputFromBlob(blob);
                }
                hideModal();
            }, "image/jpeg", 0.9);
        });

        if (form) {
            form.addEventListener("submit", function () {
                // Ako korisnik odabere sliku, ali zaboravi kliknuti Primijeni banner,
                // spremi trenutni izrez automatski.
                if (state.loaded && hiddenInput && !hiddenInput.value) {
                    applyBtn.click();
                }
            });
        }

        modalEl.addEventListener("shown.bs.modal", function () {
            if (state.loaded) {
                resetEditor();
            }
        });

        window.addEventListener("resize", function () {
            if (state.loaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
