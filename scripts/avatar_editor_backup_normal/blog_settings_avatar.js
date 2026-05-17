document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let pendingImageSource = "";
    let baseCanvasData = null;
    let currentRotation = 0;

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

    injectAvatarEditorStyle();
    cleanAvatarButtonText();

    if (modalEl && window.bootstrap) {
        avatarModal = new bootstrap.Modal(modalEl);
    }

    function injectAvatarEditorStyle() {
        const oldStyle = document.getElementById("avatarFinalEditorStyle");
        if (oldStyle) oldStyle.remove();

        const style = document.createElement("style");
        style.id = "avatarFinalEditorStyle";
        style.textContent = `
            #avatarCropModal .modal-dialog {
                max-width: 760px !important;
                margin: 1.25rem auto !important;
            }

            #avatarCropModal .modal-content {
                padding: 18px 22px !important;
                border-radius: 20px !important;
            }

            #avatarCropModal .modal-header {
                padding: 0 0 8px 0 !important;
                min-height: 0 !important;
                border: 0 !important;
            }

            #avatarCropModal .modal-title,
            #avatarCropModal h1,
            #avatarCropModal h2,
            #avatarCropModal h3,
            #avatarCropModal h4,
            #avatarCropModal h5 {
                font-size: 22px !important;
                line-height: 1.2 !important;
                margin: 0 0 4px 0 !important;
            }

            #avatarCropModal .btn-close,
            #avatarCropModal [data-bs-dismiss="modal"] {
                width: 22px !important;
                height: 22px !important;
                padding: 4px !important;
                transform: scale(0.8) !important;
                opacity: 0.9 !important;
            }

            #avatarCropModal .modal-body {
                padding: 4px 0 0 0 !important;
            }

            #avatarCropModal p,
            #avatarCropModal .text-muted,
            #avatarCropModal .form-text {
                font-size: 13px !important;
                line-height: 1.3 !important;
                margin: 0 0 10px 0 !important;
            }

            #avatarCropModal .avatar-crop-stage,
            #avatarCropModal .avatar-crop-frame {
                max-width: 620px !important;
                width: 100% !important;
                height: 290px !important;
                margin: 10px auto 12px auto !important;
                padding: 10px !important;
                box-sizing: border-box !important;
                border-radius: 16px !important;
            }

            #avatarCropModal .avatar-crop-frame {
                padding: 0 !important;
                overflow: hidden !important;
            }

            #avatarCropModal #avatarCropImage {
                display: block !important;
                max-width: 100% !important;
            }

            #avatarCropModal .avatar-crop-controls,
            #avatarCropModal .avatar-editor-controls,
            #avatarCropModal .modal-footer {
                max-width: 620px !important;
                width: 100% !important;
                margin: 0 auto !important;
                padding: 0 !important;
                gap: 10px !important;
            }

            #avatarCropModal label,
            #avatarCropModal .form-label {
                font-size: 14px !important;
                line-height: 1.2 !important;
                margin: 0 !important;
                white-space: nowrap !important;
            }

            #avatarCropModal input[type="range"] {
                height: 5px !important;
                margin: 0 !important;
            }

            #avatarCropModal .btn,
            #avatarCropModal button {
                font-size: 13px !important;
                line-height: 1.2 !important;
                padding: 6px 11px !important;
                border-radius: 8px !important;
                min-height: 0 !important;
                min-width: 0 !important;
            }

            #avatarCropModal #avatarApplyBtn {
                font-size: 14px !important;
                line-height: 1.2 !important;
                padding: 8px 16px !important;
                border-radius: 8px !important;
            }

            #avatarCropModal .cropper-view-box,
            #avatarCropModal .cropper-face {
                border-radius: 50% !important;
            }

            #avatarCropModal .cropper-view-box {
                outline: 2px solid #ffffff !important;
                outline-color: #ffffff !important;
                box-shadow: 0 0 0 1px rgba(0,0,0,0.25) !important;
            }

            #avatarCropModal .cropper-line,
            #avatarCropModal .cropper-point {
                display: none !important;
            }

            @media (max-height: 760px) {
                #avatarCropModal .modal-dialog { margin: 0.5rem auto !important; }
                #avatarCropModal .avatar-crop-stage,
                #avatarCropModal .avatar-crop-frame { height: 250px !important; }
                #avatarCropModal .modal-title,
                #avatarCropModal h1,
                #avatarCropModal h2,
                #avatarCropModal h3,
                #avatarCropModal h4,
                #avatarCropModal h5 { font-size: 20px !important; }
            }
        `;
        document.head.appendChild(style);
    }

    function cleanAvatarButtonText() {
        if (rotateBtn) rotateBtn.textContent = "Zakreni";
        if (resetBtn) resetBtn.textContent = "Vrati";
        if (applyBtn) applyBtn.textContent = "Primijeni avatar";
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
        baseCanvasData = null;
        currentRotation = 0;
    }

    function getCropDiameter(containerData) {
        const maxByContainer = Math.min(containerData.width, containerData.height) - 54;
        return Math.max(150, Math.min(215, maxByContainer));
    }

    function getNaturalSize() {
        const imageData = cropper.getImageData();
        let naturalWidth = imageData.naturalWidth || cropImage.naturalWidth || 1;
        let naturalHeight = imageData.naturalHeight || cropImage.naturalHeight || 1;

        if (Math.abs(currentRotation) % 180 === 90) {
            const temp = naturalWidth;
            naturalWidth = naturalHeight;
            naturalHeight = temp;
        }

        return { naturalWidth, naturalHeight };
    }

    function setCenteredInitialView() {
        if (!cropper) return;

        const containerData = cropper.getContainerData();
        if (!containerData.width || !containerData.height) return;

        const diameter = getCropDiameter(containerData);
        const cropLeft = (containerData.width - diameter) / 2;
        const cropTop = (containerData.height - diameter) / 2;

        cropper.setCropBoxData({
            left: cropLeft,
            top: cropTop,
            width: diameter,
            height: diameter,
        });

        const { naturalWidth, naturalHeight } = getNaturalSize();
        const fitScale = Math.min(
            (containerData.width * 0.78) / naturalWidth,
            (containerData.height * 0.78) / naturalHeight
        );
        const coverCropScale = Math.max(diameter / naturalWidth, diameter / naturalHeight);
        const scale = Math.max(fitScale, coverCropScale);

        const canvasWidth = naturalWidth * scale;
        const canvasHeight = naturalHeight * scale;
        const canvasLeft = (containerData.width - canvasWidth) / 2;
        const canvasTop = (containerData.height - canvasHeight) / 2;

        cropper.setCanvasData({
            left: canvasLeft,
            top: canvasTop,
            width: canvasWidth,
            height: canvasHeight,
        });

        baseCanvasData = {
            left: canvasLeft,
            top: canvasTop,
            width: canvasWidth,
            height: canvasHeight,
        };

        enforceCanvasCoversCropBox();
        updatePreviewFromCropper();
    }

    function enforceCanvasCoversCropBox() {
        if (!cropper) return;

        const cropBox = cropper.getCropBoxData();
        let canvas = cropper.getCanvasData();

        if (!cropBox.width || !cropBox.height || !canvas.width || !canvas.height) return;

        let width = canvas.width;
        let height = canvas.height;
        let left = canvas.left;
        let top = canvas.top;

        const scale = Math.max(cropBox.width / width, cropBox.height / height, 1);
        if (scale > 1) {
            const centerX = left + width / 2;
            const centerY = top + height / 2;
            width *= scale;
            height *= scale;
            left = centerX - width / 2;
            top = centerY - height / 2;
        }

        if (left > cropBox.left) left = cropBox.left;
        if (top > cropBox.top) top = cropBox.top;
        if (left + width < cropBox.left + cropBox.width) {
            left = cropBox.left + cropBox.width - width;
        }
        if (top + height < cropBox.top + cropBox.height) {
            top = cropBox.top + cropBox.height - height;
        }

        cropper.setCanvasData({ left, top, width, height });
    }

    function setZoomFromRange(value) {
        if (!cropper || !baseCanvasData) return;

        const cropBox = cropper.getCropBoxData();
        const oldCanvas = cropper.getCanvasData();
        const cropCenterX = cropBox.left + cropBox.width / 2;
        const cropCenterY = cropBox.top + cropBox.height / 2;

        const relativeX = oldCanvas.width ? (cropCenterX - oldCanvas.left) / oldCanvas.width : 0.5;
        const relativeY = oldCanvas.height ? (cropCenterY - oldCanvas.top) / oldCanvas.height : 0.5;

        const zoomFactor = 1 + (Number(value || 0) / 100) * 2.2;
        const newWidth = baseCanvasData.width * zoomFactor;
        const newHeight = baseCanvasData.height * zoomFactor;

        cropper.setCanvasData({
            left: cropCenterX - relativeX * newWidth,
            top: cropCenterY - relativeY * newHeight,
            width: newWidth,
            height: newHeight,
        });

        enforceCanvasCoversCropBox();
        updatePreviewFromCropper();
    }

    function initCropper() {
        if (!cropImage || !cropImage.src) return;

        destroyCropper();
        hiddenInput.value = "";
        currentRotation = 0;
        if (zoomRange) zoomRange.value = "0";

        cropper = new Cropper(cropImage, {
            aspectRatio: 1,
            viewMode: 1,
            dragMode: "move",
            autoCrop: true,
            autoCropArea: 0.6,
            background: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
            responsive: true,
            zoomOnWheel: false,
            ready() {
                window.setTimeout(function () {
                    setCenteredInitialView();
                }, 0);
            },
            crop() {
                updatePreviewFromCropper();
            },
            cropmove() {
                window.setTimeout(function () {
                    enforceCanvasCoversCropBox();
                    updatePreviewFromCropper();
                }, 0);
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
            cleanAvatarButtonText();
            if (pendingImageSource && cropImage && cropImage.complete && cropImage.naturalWidth > 0) {
                initCropper();
            }
        });

        modalEl.addEventListener("hidden.bs.modal", function () {
            destroyCropper();
            pendingImageSource = cropImage.src || "";
        });
    }

    if (zoomRange) {
        zoomRange.setAttribute("min", "0");
        zoomRange.setAttribute("max", "100");
        zoomRange.setAttribute("value", "0");

        zoomRange.addEventListener("input", function () {
            setZoomFromRange(this.value);
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;
            currentRotation = (currentRotation + 90) % 360;
            cropper.rotate(90);
            if (zoomRange) zoomRange.value = "0";
            window.setTimeout(function () {
                setCenteredInitialView();
            }, 80);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (!cropper) return;
            currentRotation = 0;
            cropper.reset();
            if (zoomRange) zoomRange.value = "0";
            window.setTimeout(function () {
                setCenteredInitialView();
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
