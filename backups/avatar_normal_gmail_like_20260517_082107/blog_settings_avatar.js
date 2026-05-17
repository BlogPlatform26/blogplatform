document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let pendingImageSource = "";
    let minZoomRatio = 1;
    let isApplyingZoom = false;

    const form = document.getElementById("avatarForm");
    const input = document.getElementById("avatarInput");
    const triggerBtn = document.getElementById("avatarChangeBtn");
    const hiddenInput = document.getElementById("croppedImage");
    const currentAvatarImage = document.getElementById("currentAvatarImage");
    const previewCanvas = document.getElementById("avatarPreviewCanvas");
    const previewMiniCanvas = document.getElementById("avatarPreviewMiniCanvas");
    const modalEl = document.getElementById("avatarCropModal");
    const cropImage = document.getElementById("avatarCropImage");
    const zoomRange = document.getElementById("avatarZoomRange");
    const rotateBtn = document.getElementById("avatarRotateBtn");
    const resetBtn = document.getElementById("avatarResetBtn");
    const applyBtn = document.getElementById("avatarApplyBtn");

    if (!form || !input || !hiddenInput || !previewCanvas || !previewMiniCanvas) {
        return;
    }

    function addAvatarEditorStyles() {
        if (document.getElementById("avatar-normal-editor-style")) {
            return;
        }

        const style = document.createElement("style");
        style.id = "avatar-normal-editor-style";
        style.textContent = `
            #avatarCropModal .modal-dialog {
                max-width: 560px;
                width: calc(100% - 20px);
                margin: 0.5rem auto;
            }

            #avatarCropModal .modal-content {
                border-radius: 22px;
                overflow: hidden;
                max-height: calc(100vh - 24px);
            }

            #avatarCropModal .modal-body {
                padding: 12px;
            }

            #avatarCropModal .avatar-crop-stage {
                width: 100%;
                max-width: 430px;
                height: 300px;
                margin: 0 auto 10px auto;
                border-radius: 20px;
                overflow: hidden;
                background: #07101d;
                border: 1px solid rgba(255, 255, 255, 0.16);
            }

            #avatarCropModal .avatar-crop-stage img {
                display: block;
                max-width: 100%;
            }

            #avatarCropModal .cropper-container {
                width: 100% !important;
                height: 100% !important;
            }

            #avatarCropModal .cropper-view-box {
                border-radius: 50%;
                outline: 3px solid rgba(255, 255, 255, 0.95);
                outline-color: rgba(255, 255, 255, 0.95);
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.48);
            }

            #avatarCropModal .cropper-face {
                border-radius: 50%;
                background-color: transparent !important;
            }

            #avatarCropModal .cropper-dashed,
            #avatarCropModal .cropper-center,
            #avatarCropModal .cropper-line,
            #avatarCropModal .cropper-point {
                display: none !important;
            }

            #avatarCropModal .cropper-crop-box {
                outline: 2px solid rgba(255, 255, 255, 0.65);
                outline-offset: 0;
            }

            #avatarCropModal .avatar-actions-row,
            #avatarCropModal .avatar-zoom-row {
                max-width: 430px;
                margin-left: auto;
                margin-right: auto;
            }

            @media (max-width: 576px) {
                #avatarCropModal .avatar-crop-stage {
                    height: 260px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    function prepareStage() {
        if (!cropImage || !cropImage.parentElement) {
            return;
        }
        cropImage.parentElement.classList.add("avatar-crop-stage");

        if (zoomRange && zoomRange.parentElement) {
            zoomRange.parentElement.classList.add("avatar-zoom-row");
        }

        if (applyBtn && applyBtn.parentElement) {
            applyBtn.parentElement.classList.add("avatar-actions-row");
        }
    }

    addAvatarEditorStyles();
    prepareStage();

    if (modalEl && window.bootstrap) {
        avatarModal = new bootstrap.Modal(modalEl);
    }

    function clearCanvas(targetCanvas) {
        if (!targetCanvas) return;
        const ctx = targetCanvas.getContext("2d");
        ctx.clearRect(0, 0, targetCanvas.width, targetCanvas.height);
    }

    function drawCircularImage(source, targetCanvas) {
        if (!source || !targetCanvas) return;

        const ctx = targetCanvas.getContext("2d");
        const width = targetCanvas.width;
        const height = targetCanvas.height;

        ctx.clearRect(0, 0, width, height);
        ctx.save();
        ctx.beginPath();
        ctx.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, Math.PI * 2);
        ctx.closePath();
        ctx.clip();
        ctx.drawImage(source, 0, 0, width, height);
        ctx.restore();
    }

    function renderImagePreview(imageLike) {
        if (!imageLike) {
            clearCanvas(previewCanvas);
            clearCanvas(previewMiniCanvas);
            return;
        }

        drawCircularImage(imageLike, previewCanvas);
        drawCircularImage(imageLike, previewMiniCanvas);
    }

    function getCropDiameter() {
        if (!cropper) return 220;

        const containerData = cropper.getContainerData();
        const maxWidth = Math.max(160, containerData.width - 70);
        const maxHeight = Math.max(160, containerData.height - 70);

        return Math.round(Math.min(240, maxWidth, maxHeight));
    }

    function setFixedCenterCropBox() {
        if (!cropper) return;

        const containerData = cropper.getContainerData();
        const diameter = getCropDiameter();

        cropper.setCropBoxData({
            left: Math.round((containerData.width - diameter) / 2),
            top: Math.round((containerData.height - diameter) / 2),
            width: diameter,
            height: diameter,
        });
    }

    function calculateMinZoomRatio() {
        if (!cropper) return 1;

        const imageData = cropper.getImageData();
        const cropBoxData = cropper.getCropBoxData();

        if (!imageData.naturalWidth || !imageData.naturalHeight || !cropBoxData.width || !cropBoxData.height) {
            return 1;
        }

        return Math.max(
            cropBoxData.width / imageData.naturalWidth,
            cropBoxData.height / imageData.naturalHeight
        );
    }

    function centerImageBehindCircle() {
        if (!cropper) return;

        const cropBoxData = cropper.getCropBoxData();
        const canvasData = cropper.getCanvasData();

        cropper.setCanvasData({
            left: Math.round(cropBoxData.left + (cropBoxData.width - canvasData.width) / 2),
            top: Math.round(cropBoxData.top + (cropBoxData.height - canvasData.height) / 2),
        });
    }

    function zoomToSafeRatio(ratio) {
        if (!cropper) return;

        const safeRatio = Math.max(ratio, minZoomRatio);
        isApplyingZoom = true;
        cropper.zoomTo(safeRatio);
        isApplyingZoom = false;
    }

    function zoomRatioFromSliderValue(value) {
        const numericValue = Number(value || 0);
        const maxRatio = minZoomRatio * 4;
        return minZoomRatio + ((maxRatio - minZoomRatio) * numericValue / 100);
    }

    function updatePreviewFromCropper() {
        if (!cropper) return;

        const canvas = cropper.getCroppedCanvas({
            width: 320,
            height: 320,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: "high",
        });

        if (!canvas) return;
        renderImagePreview(canvas);
    }

    function applyCropToHiddenInput() {
        if (!cropper) return false;

        const canvas = cropper.getCroppedCanvas({
            width: 400,
            height: 400,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: "high",
        });

        if (!canvas) return false;

        hiddenInput.value = canvas.toDataURL("image/jpeg", 0.92);
        renderImagePreview(canvas);
        return true;
    }

    function destroyCropper() {
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    }

    function initCropper() {
        if (!cropImage || !cropImage.src) return;

        destroyCropper();
        hiddenInput.value = "";

        if (zoomRange) {
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";
        }

        cropper = new Cropper(cropImage, {
            aspectRatio: 1,
            viewMode: 1,
            dragMode: "move",
            autoCrop: true,
            autoCropArea: 1,
            background: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
            responsive: true,
            restore: false,
            checkOrientation: true,
            wheelZoomRatio: 0.05,

            ready() {
                setFixedCenterCropBox();
                minZoomRatio = calculateMinZoomRatio();
                zoomToSafeRatio(minZoomRatio);
                centerImageBehindCircle();
                updatePreviewFromCropper();
            },

            crop() {
                updatePreviewFromCropper();
            },

            zoom(event) {
                if (!isApplyingZoom && event.detail && event.detail.ratio < minZoomRatio) {
                    event.preventDefault();
                }
            },
        });
    }

    function openEditorFromFile(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (event) {
            pendingImageSource = event.target.result;
            cropImage.src = pendingImageSource;

            if (avatarModal) {
                avatarModal.show();
            } else {
                initCropper();
            }
        };
        reader.readAsDataURL(file);
    }

    if (currentAvatarImage) {
        if (currentAvatarImage.complete) {
            renderImagePreview(currentAvatarImage);
        } else {
            currentAvatarImage.addEventListener("load", function () {
                renderImagePreview(currentAvatarImage);
            }, { once: true });
        }
    }

    if (triggerBtn) {
        triggerBtn.addEventListener("click", function () {
            input.click();
        });
    }

    if (cropImage) {
        cropImage.addEventListener("load", function () {
            if (!pendingImageSource) return;
            if (!modalEl || modalEl.classList.contains("show")) {
                initCropper();
            }
        });
    }

    input.addEventListener("change", function (event) {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        openEditorFromFile(file);
    });

    if (modalEl) {
        modalEl.addEventListener("shown.bs.modal", function () {
            if (pendingImageSource && cropImage && cropImage.complete && cropImage.naturalWidth > 0) {
                initCropper();
            }
        });

        modalEl.addEventListener("hidden.bs.modal", function () {
            destroyCropper();
        });
    }

    if (zoomRange) {
        zoomRange.addEventListener("input", function () {
            if (!cropper) return;
            zoomToSafeRatio(zoomRatioFromSliderValue(this.value));
            updatePreviewFromCropper();
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;
            cropper.rotate(90);
            setTimeout(function () {
                setFixedCenterCropBox();
                minZoomRatio = calculateMinZoomRatio();
                if (zoomRange) zoomRange.value = "0";
                zoomToSafeRatio(minZoomRatio);
                centerImageBehindCircle();
                updatePreviewFromCropper();
            }, 0);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (!cropper) return;
            cropper.reset();
            setTimeout(function () {
                setFixedCenterCropBox();
                minZoomRatio = calculateMinZoomRatio();
                if (zoomRange) zoomRange.value = "0";
                zoomToSafeRatio(minZoomRatio);
                centerImageBehindCircle();
                updatePreviewFromCropper();
            }, 0);
        });
    }

    if (applyBtn) {
        applyBtn.addEventListener("click", function () {
            const applied = applyCropToHiddenInput();
            if (applied && avatarModal) {
                avatarModal.hide();
            }
        });
    }

    form.addEventListener("submit", function (event) {
        const submitter = event.submitter;

        if (submitter && submitter.name === "delete_avatar") {
            hiddenInput.value = "";
            return;
        }

        if (cropper && !hiddenInput.value) {
            applyCropToHiddenInput();
        }
    });
});
