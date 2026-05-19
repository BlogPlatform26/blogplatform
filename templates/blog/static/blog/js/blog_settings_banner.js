(function () {
    "use strict";

    function onReady(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    function injectBannerEditorStyle() {
        if (document.getElementById("bannerEditorRectStyle")) {
            return;
        }

        const style = document.createElement("style");
        style.id = "bannerEditorRectStyle";
        style.textContent = `
            #blogBannerCropModal .modal-dialog {
                max-width: 980px;
                margin: 1.25rem auto;
            }

            #blogBannerCropModal .modal-content {
                background: #111827;
                color: #f8fafc;
                border: 0;
                border-radius: 22px;
                padding: 18px 24px;
                box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
            }

            #blogBannerCropModal .modal-header {
                border-bottom: 0;
                padding: 0 0 12px 0;
            }

            #blogBannerCropModal .modal-title {
                font-size: 24px;
                line-height: 1.2;
                margin: 0 0 4px 0;
            }

            #blogBannerCropModal .text-muted {
                color: rgba(248, 250, 252, 0.62) !important;
                font-size: 13px;
            }

            #blogBannerCropModal .btn-close {
                filter: invert(1) grayscale(100%);
                opacity: 0.85;
                transform: scale(0.82);
            }

            #blogBannerCropModal .modal-body {
                padding: 0;
            }

            #blogBannerCropModal .banner-crop-stage {
                max-width: 860px;
                margin: 14px auto 12px auto;
                padding: 10px;
                border: 1px solid rgba(148, 163, 184, 0.26);
                border-radius: 18px;
                background: rgba(15, 23, 42, 0.92);
            }

            #blogBannerCropModal .banner-crop-frame {
                width: 100%;
                aspect-ratio: 22 / 9;
                min-height: 220px;
                max-height: 340px;
                position: relative;
                overflow: hidden;
                border-radius: 14px;
                background: #05080d;
                border: 2px solid rgba(255, 255, 255, 0.88);
                touch-action: none;
            }

            #blogBannerCropModal .banner-crop-frame::after {
                content: "";
                position: absolute;
                inset: 0;
                border: 1px solid rgba(255, 255, 255, 0.42);
                box-shadow: inset 0 0 0 9999px rgba(0, 0, 0, 0.04);
                pointer-events: none;
                z-index: 3;
            }

            #blogBannerCropModal #blogBannerCropImage {
                position: absolute;
                left: 0;
                top: 0;
                max-width: none !important;
                max-height: none !important;
                width: auto !important;
                height: auto !important;
                user-select: none;
                -webkit-user-drag: none;
                cursor: grab;
                transform-origin: center center;
                will-change: transform;
            }

            #blogBannerCropModal #blogBannerCropImage.is-dragging {
                cursor: grabbing;
            }

            #blogBannerCropModal .banner-crop-controls {
                max-width: 860px;
                margin: 0 auto;
            }

            #blogBannerCropModal .banner-crop-control-row {
                display: grid;
                grid-template-columns: 120px 1fr;
                gap: 14px;
                align-items: center;
            }

            #blogBannerCropModal .form-label {
                color: #e5e7eb;
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 0;
            }

            #blogBannerCropModal #blogBannerZoomRange {
                height: 5px;
            }

            #blogBannerCropModal .btn {
                font-size: 14px;
                line-height: 1.2;
                padding: 7px 12px;
                border-radius: 8px;
            }

            #blogBannerCropModal #blogBannerApplyBtn {
                font-size: 15px;
                padding: 8px 18px;
                min-width: 160px;
            }

            @media (max-width: 768px) {
                #blogBannerCropModal .modal-dialog {
                    max-width: calc(100vw - 18px);
                    margin: 0.75rem auto;
                }

                #blogBannerCropModal .modal-content {
                    padding: 14px;
                }

                #blogBannerCropModal .banner-crop-control-row {
                    grid-template-columns: 1fr;
                    gap: 6px;
                }

                #blogBannerCropModal .banner-crop-frame {
                    min-height: 170px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    onReady(function () {
        injectBannerEditorStyle();

        const form = document.getElementById("avatarForm") || document.querySelector('form[enctype="multipart/form-data"]');
        const input = document.getElementById("blogBannerInput") || document.querySelector('input[type="file"][name="blog_banner"]');
        const triggerBtn = document.getElementById("blogBannerChangeBtn");
        const hiddenInput = document.getElementById("croppedBlogBanner") || document.querySelector('input[name="cropped_blog_banner"]');
        const modalEl = document.getElementById("blogBannerCropModal");
        const cropImage = document.getElementById("blogBannerCropImage");
        const zoomRange = document.getElementById("blogBannerZoomRange");
        const rotateBtn = document.getElementById("blogBannerRotateBtn");
        const resetBtn = document.getElementById("blogBannerResetBtn");
        const applyBtn = document.getElementById("blogBannerApplyBtn");

        if (!form || !input || !hiddenInput || !modalEl || !cropImage || !zoomRange) {
            return;
        }

        const frame = modalEl.querySelector(".banner-crop-frame") || cropImage.parentElement;
        let bannerModal = null;
        let imageLoaded = false;
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let startX = 0;
        let startY = 0;

        const state = {
            x: 0,
            y: 0,
            scale: 1,
            minScale: 1,
            rotation: 0,
            naturalWidth: 0,
            naturalHeight: 0,
        };

        if (window.bootstrap) {
            bannerModal = new bootstrap.Modal(modalEl);
        }

        function getFrameRect() {
            return frame.getBoundingClientRect();
        }

        function getRotatedBaseSize() {
            const normalized = ((state.rotation % 360) + 360) % 360;
            if (normalized === 90 || normalized === 270) {
                return {
                    width: state.naturalHeight,
                    height: state.naturalWidth,
                };
            }
            return {
                width: state.naturalWidth,
                height: state.naturalHeight,
            };
        }

        function clampPosition() {
            const rect = getFrameRect();
            const baseSize = getRotatedBaseSize();
            const renderedWidth = baseSize.width * state.scale;
            const renderedHeight = baseSize.height * state.scale;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const minX = rect.width - renderedWidth / 2;
            const maxX = renderedWidth / 2;
            const minY = rect.height - renderedHeight / 2;
            const maxY = renderedHeight / 2;

            if (minX <= maxX) {
                state.x = Math.min(Math.max(state.x, minX), maxX);
            } else {
                state.x = centerX;
            }

            if (minY <= maxY) {
                state.y = Math.min(Math.max(state.y, minY), maxY);
            } else {
                state.y = centerY;
            }
        }

        function updateImageTransform() {
            cropImage.style.width = state.naturalWidth + "px";
            cropImage.style.height = state.naturalHeight + "px";
            cropImage.style.left = "0px";
            cropImage.style.top = "0px";
            cropImage.style.transform =
                "translate(" + (state.x - state.naturalWidth / 2) + "px, " + (state.y - state.naturalHeight / 2) + "px) " +
                "rotate(" + state.rotation + "deg) " +
                "scale(" + state.scale + ")";
        }

        function calculateInitialState() {
            const rect = getFrameRect();
            const baseSize = getRotatedBaseSize();
            state.minScale = Math.max(rect.width / baseSize.width, rect.height / baseSize.height);
            state.scale = state.minScale;
            state.x = rect.width / 2;
            state.y = rect.height / 2;
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";
            clampPosition();
            updateImageTransform();
        }

        function getScaleForZoomValue(value) {
            const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
            const zoomFactor = 1 + (safeValue / 100) * 3;
            return state.minScale * zoomFactor;
        }

        function setZoomValue(nextValue) {
            if (!imageLoaded) return;

            const currentScale = state.scale;
            const nextScale = getScaleForZoomValue(nextValue);
            const rect = getFrameRect();
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const ratio = nextScale / currentScale;

            state.x = centerX + (state.x - centerX) * ratio;
            state.y = centerY + (state.y - centerY) * ratio;
            state.scale = nextScale;
            zoomRange.value = String(Math.max(0, Math.min(100, Number(nextValue || 0))));
            clampPosition();
            updateImageTransform();
        }

        function handleZoomChange() {
            if (!imageLoaded) return;
            setZoomValue(zoomRange.value);
        }

        function drawStageToCanvas() {
            const rect = getFrameRect();
            const stageCanvas = document.createElement("canvas");
            stageCanvas.width = Math.max(1, Math.round(rect.width));
            stageCanvas.height = Math.max(1, Math.round(rect.height));
            const ctx = stageCanvas.getContext("2d");
            ctx.fillStyle = "#05080d";
            ctx.fillRect(0, 0, stageCanvas.width, stageCanvas.height);
            ctx.save();
            ctx.translate(state.x, state.y);
            ctx.rotate((state.rotation * Math.PI) / 180);
            ctx.scale(state.scale, state.scale);
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(cropImage, -state.naturalWidth / 2, -state.naturalHeight / 2, state.naturalWidth, state.naturalHeight);
            ctx.restore();
            return stageCanvas;
        }

        function getCroppedCanvas() {
            if (!imageLoaded) return null;
            const stageCanvas = drawStageToCanvas();
            const outputCanvas = document.createElement("canvas");
            outputCanvas.width = 2200;
            outputCanvas.height = 900;
            const ctx = outputCanvas.getContext("2d");
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = "high";
            ctx.drawImage(stageCanvas, 0, 0, stageCanvas.width, stageCanvas.height, 0, 0, outputCanvas.width, outputCanvas.height);
            return outputCanvas;
        }

        function applyCropToHiddenInput() {
            const canvas = getCroppedCanvas();
            if (!canvas) return false;
            hiddenInput.value = canvas.toDataURL("image/jpeg", 0.94);
            return true;
        }

        function setupImageAfterLoad() {
            imageLoaded = true;
            state.naturalWidth = cropImage.naturalWidth;
            state.naturalHeight = cropImage.naturalHeight;
            state.rotation = 0;
            hiddenInput.value = "";
            requestAnimationFrame(calculateInitialState);
        }

        function openEditorFromFile(file) {
            if (!file || !file.type || !file.type.startsWith("image/")) return;
            const reader = new FileReader();
            reader.onload = function (event) {
                imageLoaded = false;
                cropImage.src = event.target.result;
                if (bannerModal) {
                    bannerModal.show();
                }
            };
            reader.readAsDataURL(file);
        }

        if (triggerBtn) {
            triggerBtn.addEventListener("click", function () {
                input.click();
            });
        }

        input.addEventListener("change", function (event) {
            const file = event.target.files && event.target.files[0];
            if (!file) return;
            openEditorFromFile(file);
        });

        cropImage.addEventListener("load", function () {
            if (cropImage.naturalWidth > 0 && cropImage.naturalHeight > 0) {
                if (!bannerModal || modalEl.classList.contains("show")) {
                    setupImageAfterLoad();
                }
            }
        });

        modalEl.addEventListener("shown.bs.modal", function () {
            if (cropImage.complete && cropImage.naturalWidth > 0 && cropImage.naturalHeight > 0) {
                setupImageAfterLoad();
            }
        });

        zoomRange.addEventListener("input", handleZoomChange);

        frame.addEventListener("wheel", function (event) {
            if (!imageLoaded) return;
            event.preventDefault();
            const currentValue = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 4 : -4;
            const nextValue = Math.max(0, Math.min(100, currentValue + step));
            if (nextValue !== currentValue) {
                setZoomValue(nextValue);
            }
        }, { passive: false });

        frame.addEventListener("pointerdown", function (event) {
            if (!imageLoaded) return;
            isDragging = true;
            cropImage.classList.add("is-dragging");
            frame.setPointerCapture(event.pointerId);
            dragStartX = event.clientX;
            dragStartY = event.clientY;
            startX = state.x;
            startY = state.y;
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
            cropImage.classList.remove("is-dragging");
            if (event && frame.hasPointerCapture(event.pointerId)) {
                frame.releasePointerCapture(event.pointerId);
            }
        }

        frame.addEventListener("pointerup", stopDragging);
        frame.addEventListener("pointercancel", stopDragging);
        frame.addEventListener("pointerleave", stopDragging);

        if (rotateBtn) {
            rotateBtn.addEventListener("click", function () {
                if (!imageLoaded) return;
                state.rotation = (state.rotation + 90) % 360;
                calculateInitialState();
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener("click", function () {
                if (!imageLoaded) return;
                state.rotation = 0;
                calculateInitialState();
            });
        }

        if (applyBtn) {
            applyBtn.addEventListener("click", function () {
                const applied = applyCropToHiddenInput();
                if (applied && bannerModal) {
                    bannerModal.hide();
                }
            });
        }

        form.addEventListener("submit", function () {
            if (imageLoaded && !hiddenInput.value) {
                applyCropToHiddenInput();
            }
        });

        window.addEventListener("resize", function () {
            if (!imageLoaded || !modalEl.classList.contains("show")) return;
            calculateInitialState();
        });
    });
})();
