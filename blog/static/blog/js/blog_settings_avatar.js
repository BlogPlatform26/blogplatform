document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let lastZoomValue = 50;
    let pendingImageSource = "";
    let cropBoxSyncTimeout = null;

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
        if (cropBoxSyncTimeout) {
            clearTimeout(cropBoxSyncTimeout);
            cropBoxSyncTimeout = null;
        }
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    }

    function syncCropBoxToVisibleImage() {
        if (!cropper) return;

        const canvasData = cropper.getCanvasData();
        if (!canvasData || !canvasData.width || !canvasData.height) return;

        const diameter = Math.max(140, Math.min(canvasData.width, canvasData.height) * 0.78);
        const left = canvasData.left + (canvasData.width - diameter) / 2;
        const top = canvasData.top + (canvasData.height - diameter) / 2;

        cropper.setCropBoxData({
            left,
            top,
            width: diameter,
            height: diameter,
        });
    }

    function queueCropBoxSync() {
        if (cropBoxSyncTimeout) clearTimeout(cropBoxSyncTimeout);
        cropBoxSyncTimeout = setTimeout(function () {
            syncCropBoxToVisibleImage();
            updatePreviewFromCropper();
        }, 0);
    }

    function initCropper() {
        if (!cropImage || !cropImage.src) return;

        destroyCropper();
        hiddenInput.value = "";
        lastZoomValue = 50;
        if (zoomRange) zoomRange.value = "50";

        cropper = new Cropper(cropImage, {
            aspectRatio: 1,
            viewMode: 1,
            dragMode: "move",
            autoCrop: true,
            autoCropArea: 0.8,
            background: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
            responsive: true,
            ready() {
                syncCropBoxToVisibleImage();
                updatePreviewFromCropper();
            },
            crop() {
                updatePreviewFromCropper();
            },
            zoom() {
                queueCropBoxSync();
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
            pendingImageSource = cropImage.src || "";
        });
    }

    if (zoomRange) {
        zoomRange.addEventListener("input", function () {
            if (!cropper) return;
            const currentValue = Number(this.value || 50);
            const delta = (currentValue - lastZoomValue) / 40;
            cropper.zoom(delta);
            lastZoomValue = currentValue;
            queueCropBoxSync();
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;
            cropper.rotate(90);
            queueCropBoxSync();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (!cropper) return;
            cropper.reset();
            if (zoomRange) zoomRange.value = "50";
            lastZoomValue = 50;
            queueCropBoxSync();
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
