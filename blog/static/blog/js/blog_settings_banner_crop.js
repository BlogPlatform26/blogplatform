document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let bannerModal = null;
    let lastZoomValue = 50;
    let pendingImageSource = "";
    let cropBoxSyncTimeout = null;

    const form = document.getElementById("avatarForm") || document.querySelector('form[method="post"]');
    const input = document.getElementById("blogBannerInput") || document.querySelector('input[name="blog_banner"]');
    const triggerBtn = document.getElementById("blogBannerChangeBtn");
    const hiddenInput = document.getElementById("croppedBlogBanner");
    const modalEl = document.getElementById("blogBannerCropModal");
    const cropImage = document.getElementById("blogBannerCropImage");
    const zoomRange = document.getElementById("blogBannerZoomRange");
    const rotateBtn = document.getElementById("blogBannerRotateBtn");
    const resetBtn = document.getElementById("blogBannerResetBtn");
    const applyBtn = document.getElementById("blogBannerApplyBtn");
    const previewWrap = document.getElementById("blogBannerCropPreviewWrap");
    const previewCanvas = document.getElementById("blogBannerPreviewCanvas");

    if (!form || !input || !hiddenInput || !modalEl || !cropImage || typeof Cropper === "undefined") {
        return;
    }

    input.setAttribute("accept", "image/*");

    if (window.bootstrap) {
        bannerModal = new bootstrap.Modal(modalEl);
    }

    function clearCanvas(targetCanvas) {
        if (!targetCanvas) return;
        const ctx = targetCanvas.getContext("2d");
        ctx.clearRect(0, 0, targetCanvas.width, targetCanvas.height);
    }

    function renderPreview(sourceCanvas) {
        if (!previewCanvas) return;
        if (!sourceCanvas) {
            clearCanvas(previewCanvas);
            if (previewWrap) previewWrap.classList.add("d-none");
            return;
        }

        const ctx = previewCanvas.getContext("2d");
        ctx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
        ctx.drawImage(sourceCanvas, 0, 0, previewCanvas.width, previewCanvas.height);
        if (previewWrap) previewWrap.classList.remove("d-none");
    }

    function getBannerCanvas(width, height) {
        if (!cropper) return null;
        return cropper.getCroppedCanvas({
            width: width,
            height: height,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: "high",
            fillColor: "#ffffff"
        });
    }

    function updatePreviewFromCropper() {
        const canvas = getBannerCanvas(440, 180);
        if (!canvas) return;
        renderPreview(canvas);
    }

    function applyCropToHiddenInput() {
        const canvas = getBannerCanvas(1760, 720);
        if (!canvas) return false;
        hiddenInput.value = canvas.toDataURL("image/jpeg", 0.9);
        renderPreview(canvas);
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

        const ratio = 22 / 9;
        let width = canvasData.width * 0.92;
        let height = width / ratio;

        if (height > canvasData.height * 0.82) {
            height = canvasData.height * 0.82;
            width = height * ratio;
        }

        width = Math.max(260, width);
        height = Math.max(105, height);

        const left = canvasData.left + (canvasData.width - width) / 2;
        const top = canvasData.top + (canvasData.height - height) / 2;

        cropper.setCropBoxData({
            left: left,
            top: top,
            width: width,
            height: height
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
            aspectRatio: 22 / 9,
            viewMode: 1,
            dragMode: "move",
            autoCrop: true,
            autoCropArea: 0.92,
            background: false,
            guides: true,
            center: true,
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
            }
        });
    }

    function openEditorFromFile(file) {
        if (!file) return;
        if (!file.type || !file.type.startsWith("image/")) {
            alert("Odaberi slikovnu datoteku.");
            input.value = "";
            return;
        }

        const reader = new FileReader();
        reader.onload = function (event) {
            pendingImageSource = event.target.result;
            cropImage.src = pendingImageSource;
            if (bannerModal) {
                bannerModal.show();
            } else {
                initCropper();
            }
        };
        reader.readAsDataURL(file);
    }

    if (triggerBtn) {
        triggerBtn.addEventListener("click", function () {
            input.click();
        });
    }

    cropImage.addEventListener("load", function () {
        if (!pendingImageSource) return;
        if (!modalEl || modalEl.classList.contains("show")) {
            initCropper();
        }
    });

    input.addEventListener("change", function (event) {
        const file = event.target.files && event.target.files[0];
        hiddenInput.value = "";
        if (!file) return;
        openEditorFromFile(file);
    });

    modalEl.addEventListener("shown.bs.modal", function () {
        if (pendingImageSource && cropImage.complete && cropImage.naturalWidth > 0) {
            initCropper();
        }
    });

    modalEl.addEventListener("hidden.bs.modal", function () {
        destroyCropper();
        pendingImageSource = cropImage.src || "";
    });

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
            if (applied && bannerModal) {
                bannerModal.hide();
            }
        });
    }

    form.addEventListener("submit", function (event) {
        const submitter = event.submitter;
        if (submitter && submitter.name === "delete_blog_banner") {
            hiddenInput.value = "";
            return;
        }

        if (input.files && input.files.length > 0 && !hiddenInput.value && cropper) {
            applyCropToHiddenInput();
        }
    });
});
