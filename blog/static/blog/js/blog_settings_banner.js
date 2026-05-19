
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
        const hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');
        const changeBtn = document.getElementById("blogBannerChangeBtn");
        const selectedName = document.getElementById("blogBannerSelectedName");

        const modalEl = document.getElementById("blogBannerCropModal");
        const frame = document.getElementById("blogBannerCropFrame");
        const img = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const applyBtn = document.getElementById("blogBannerApplyBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");

        if (!fileInput || !hiddenInput || !changeBtn || !modalEl || !frame || !img || !zoomRange || !applyBtn) {
            return;
        }

        let modal = null;
        if (window.bootstrap && window.bootstrap.Modal) {
            modal = new window.bootstrap.Modal(modalEl);
        }

        let imageLoaded = false;
        let naturalWidth = 0;
        let naturalHeight = 0;
        let minScale = 1;
        let maxScale = 4;
        let scale = 1;
        let x = 0;
        let y = 0;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let startX = 0;
        let startY = 0;
        let objectUrl = null;

        function showModal() {
            if (modal) {
                modal.show();
                return;
            }
            modalEl.style.display = "block";
            modalEl.classList.add("show");
            document.body.classList.add("modal-open");
        }

        function hideModal() {
            if (modal) {
                modal.hide();
                return;
            }
            modalEl.classList.remove("show");
            modalEl.style.display = "none";
            document.body.classList.remove("modal-open");
        }

        function frameSize() {
            const rect = frame.getBoundingClientRect();
            return {
                width: Math.max(1, rect.width),
                height: Math.max(1, rect.height)
            };
        }

        function calculateLimits() {
            const size = frameSize();
            minScale = Math.max(size.width / naturalWidth, size.height / naturalHeight);
            maxScale = minScale * 4;

            if (!Number.isFinite(minScale) || minScale <= 0) {
                minScale = 1;
            }
            if (!Number.isFinite(maxScale) || maxScale <= minScale) {
                maxScale = minScale + 1;
            }
        }

        function clampPosition() {
            const size = frameSize();
            const scaledWidth = naturalWidth * scale;
            const scaledHeight = naturalHeight * scale;

            if (scaledWidth <= size.width) {
                x = (size.width - scaledWidth) / 2;
            } else {
                x = Math.min(0, Math.max(size.width - scaledWidth, x));
            }

            if (scaledHeight <= size.height) {
                y = (size.height - scaledHeight) / 2;
            } else {
                y = Math.min(0, Math.max(size.height - scaledHeight, y));
            }
        }

        function render() {
            clampPosition();
            img.style.width = naturalWidth + "px";
            img.style.height = naturalHeight + "px";
            img.style.transform = "translate(" + x + "px, " + y + "px) scale(" + scale + ")";
        }

        function setZoomFromRange(value) {
            if (!imageLoaded) {
                return;
            }

            const oldScale = scale;
            const size = frameSize();
            const centerX = size.width / 2;
            const centerY = size.height / 2;
            const ratio = Math.max(0, Math.min(100, Number(value))) / 100;

            scale = minScale + (maxScale - minScale) * ratio;

            const imagePointX = (centerX - x) / oldScale;
            const imagePointY = (centerY - y) / oldScale;
            x = centerX - imagePointX * scale;
            y = centerY - imagePointY * scale;

            render();
        }

        function resetEditor() {
            if (!imageLoaded) {
                return;
            }

            calculateLimits();
            scale = minScale;
            const size = frameSize();
            x = (size.width - naturalWidth * scale) / 2;
            y = (size.height - naturalHeight * scale) / 2;
            zoomRange.value = "0";
            render();
        }

        function openSelectedFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) {
                return;
            }

            hiddenInput.value = "";

            if (objectUrl) {
                URL.revokeObjectURL(objectUrl);
                objectUrl = null;
            }

            objectUrl = URL.createObjectURL(file);
            imageLoaded = false;
            img.onload = function () {
                naturalWidth = img.naturalWidth;
                naturalHeight = img.naturalHeight;
                imageLoaded = true;
                showModal();
                window.setTimeout(resetEditor, 80);
            };
            img.src = objectUrl;

            if (selectedName) {
                selectedName.textContent = file.name || "Odabrana slika";
            }
        }

        changeBtn.addEventListener("click", function () {
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = fileInput.files && fileInput.files[0];
            openSelectedFile(file);
        });

        zoomRange.addEventListener("input", function () {
            setZoomFromRange(zoomRange.value);
        });

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                resetEditor();
            });
        }

        frame.addEventListener("wheel", function (event) {
            if (!imageLoaded) {
                return;
            }
            event.preventDefault();
            const current = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            const next = Math.max(0, Math.min(100, current + step));
            zoomRange.value = String(next);
            setZoomFromRange(next);
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!imageLoaded) {
                return;
            }
            isDragging = true;
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            startX = x;
            startY = y;
            frame.setPointerCapture(event.pointerId);
            img.classList.add("is-dragging");
        });

        frame.addEventListener("pointermove", function (event) {
            if (!isDragging || !imageLoaded) {
                return;
            }
            x = startX + (event.clientX - dragStartX);
            y = startY + (event.clientY - dragStartY);
            render();
        });

        function stopDragging(event) {
            if (!isDragging) {
                return;
            }
            isDragging = false;
            img.classList.remove("is-dragging");
            if (event && frame.releasePointerCapture) {
                try {
                    frame.releasePointerCapture(event.pointerId);
                } catch (error) {
                    // nije važno ako pointer više nije aktivan
                }
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        applyBtn.addEventListener("click", function () {
            if (!imageLoaded) {
                return;
            }

            const size = frameSize();
            const outputWidth = 2200;
            const outputHeight = 900;
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");

            canvas.width = outputWidth;
            canvas.height = outputHeight;

            const sourceX = Math.max(0, -x / scale);
            const sourceY = Math.max(0, -y / scale);
            const sourceWidth = Math.min(naturalWidth - sourceX, size.width / scale);
            const sourceHeight = Math.min(naturalHeight - sourceY, size.height / scale);

            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, outputWidth, outputHeight);
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

            hiddenInput.value = canvas.toDataURL("image/jpeg", 0.96);

            if (selectedName) {
                selectedName.textContent = "Banner je pripremljen. Klikni Spremi promjene.";
            }

            hideModal();
        });

        window.addEventListener("resize", function () {
            if (imageLoaded && modalEl.classList.contains("show")) {
                resetEditor();
            }
        });
    });
})();
