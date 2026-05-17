from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if not js_path.exists():
    raise SystemExit(f"Ne mogu naći datoteku: {js_path}")

backup_path = js_path.with_suffix(js_path.suffix + ".bak_before_avatar_gmail_center")
if not backup_path.exists():
    backup_path.write_text(js_path.read_text(encoding="utf-8"), encoding="utf-8")

new_js = r'''document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let pendingImageSource = "";
    let lastZoomValue = 0;
    let cropApplied = false;
    let isFixingCanvas = false;
    let updatePreviewTimeout = null;

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

    if (!form || !input || !hiddenInput || !previewCanvas || !previewMiniCanvas || !cropImage) {
        return;
    }

    function installAvatarEditorStyles() {
        if (document.getElementById("avatarGmailStyleFix")) {
            return;
        }

        const style = document.createElement("style");
        style.id = "avatarGmailStyleFix";
        style.textContent = `
            #avatarCropModal .cropper-container {
                width: 100% !important;
            }

            #avatarCropModal .cropper-view-box,
            #avatarCropModal .cropper-face {
                border-radius: 50% !important;
            }

            #avatarCropModal .cropper-crop-box {
                box-shadow: 0 0 0 9999px rgba(2, 6, 23, 0.58) !important;
            }

            #avatarCropModal .cropper-line,
            #avatarCropModal .cropper-point {
                display: none !important;
            }

            #avatarCropModal .cropper-view-box {
                outline: 2px solid rgba(255, 255, 255, 0.95) !important;
                outline-color: rgba(255, 255, 255, 0.95) !important;
            }

            #avatarCropModal .cropper-face {
                background-color: transparent !important;
            }
        `;
        document.head.appendChild(style);
    }

    installAvatarEditorStyles();

    if (modalEl && window.bootstrap) {
        avatarModal = new bootstrap.Modal(modalEl, {
            backdrop: true,
            keyboard: true,
            focus: true,
        });
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

        window.clearTimeout(updatePreviewTimeout);
        updatePreviewTimeout = window.setTimeout(function () {
            if (!cropper) return;

            const canvas = cropper.getCroppedCanvas({
                width: 320,
                height: 320,
                imageSmoothingEnabled: true,
                imageSmoothingQuality: "high",
            });

            if (canvas) {
                renderImagePreview(canvas);
            }
        }, 30);
    }

    function applyCropToHiddenInput() {
        if (!cropper) return false;

        const canvas = cropper.getCroppedCanvas({
            width: 500,
            height: 500,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: "high",
        });

        if (!canvas) return false;

        hiddenInput.value = canvas.toDataURL("image/jpeg", 0.92);
        renderImagePreview(canvas);
        cropApplied = true;
        return true;
    }

    function destroyCropper() {
        window.clearTimeout(updatePreviewTimeout);
        updatePreviewTimeout = null;

        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    }

    function getSafeCropDiameter() {
        if (!cropper) return 260;

        const containerData = cropper.getContainerData();
        const maxByWidth = containerData.width * 0.42;
        const maxByHeight = containerData.height * 0.72;
        const diameter = Math.min(320, maxByWidth, maxByHeight);

        return Math.max(180, Math.round(diameter));
    }

    function centerFixedCropCircle() {
        if (!cropper) return;

        const containerData = cropper.getContainerData();
        const diameter = getSafeCropDiameter();

        cropper.setCropBoxData({
            left: Math.round((containerData.width - diameter) / 2),
            top: Math.round((containerData.height - diameter) / 2),
            width: diameter,
            height: diameter,
        });
    }

    function ensureImageCoversCropCircle() {
        if (!cropper || isFixingCanvas) return;

        const cropBoxData = cropper.getCropBoxData();
        let canvasData = cropper.getCanvasData();

        if (!cropBoxData || !canvasData || !canvasData.width || !canvasData.height) {
            return;
        }

        isFixingCanvas = true;

        let nextCanvasData = {
            left: canvasData.left,
            top: canvasData.top,
            width: canvasData.width,
            height: canvasData.height,
        };

        const neededScale = Math.max(
            cropBoxData.width / canvasData.width,
            cropBoxData.height / canvasData.height,
            1
        );

        if (neededScale > 1.0001) {
            const centerX = cropBoxData.left + cropBoxData.width / 2;
            const centerY = cropBoxData.top + cropBoxData.height / 2;

            nextCanvasData.width = canvasData.width * neededScale;
            nextCanvasData.height = canvasData.height * neededScale;
            nextCanvasData.left = centerX - nextCanvasData.width / 2;
            nextCanvasData.top = centerY - nextCanvasData.height / 2;
        }

        if (nextCanvasData.left > cropBoxData.left) {
            nextCanvasData.left = cropBoxData.left;
        }

        if (nextCanvasData.top > cropBoxData.top) {
            nextCanvasData.top = cropBoxData.top;
        }

        if (nextCanvasData.left + nextCanvasData.width < cropBoxData.left + cropBoxData.width) {
            nextCanvasData.left = cropBoxData.left + cropBoxData.width - nextCanvasData.width;
        }

        if (nextCanvasData.top + nextCanvasData.height < cropBoxData.top + cropBoxData.height) {
            nextCanvasData.top = cropBoxData.top + cropBoxData.height - nextCanvasData.height;
        }

        cropper.setCanvasData(nextCanvasData);
        isFixingCanvas = false;
    }

    function lockGmailStyleCircle() {
        if (!cropper) return;
        centerFixedCropCircle();
        ensureImageCoversCropCircle();
        updatePreviewFromCropper();
    }

    function resetZoomSlider() {
        if (!zoomRange) return;
        zoomRange.min = "0";
        zoomRange.max = "100";
        zoomRange.step = "1";
        zoomRange.value = "0";
        lastZoomValue = 0;
    }

    function initCropper() {
        if (!cropImage || !cropImage.src) return;

        destroyCropper();
        hiddenInput.value = "";
        cropApplied = false;
        resetZoomSlider();

        cropper = new Cropper(cropImage, {
            aspectRatio: 1,
            viewMode: 3,
            dragMode: "move",
            autoCrop: true,
            autoCropArea: 0.55,
            background: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: false,
            cropBoxResizable: false,
            toggleDragModeOnDblclick: false,
            responsive: true,
            restore: false,
            modal: true,
            ready() {
                lockGmailStyleCircle();
            },
            cropmove() {
                ensureImageCoversCropCircle();
            },
            cropend() {
                ensureImageCoversCropCircle();
                updatePreviewFromCropper();
            },
            zoom() {
                window.setTimeout(function () {
                    ensureImageCoversCropCircle();
                    updatePreviewFromCropper();
                }, 0);
            },
            crop() {
                updatePreviewFromCropper();
            },
        });
    }

    function openEditorFromFile(file) {
        if (!file) return;

        if (!file.type || !file.type.startsWith("image/")) {
            input.value = "";
            alert("Odaberi sliku u JPG, PNG ili WEBP formatu.");
            return;
        }

        const reader = new FileReader();
        reader.onload = function (event) {
            pendingImageSource = event.target.result;
            cropApplied = false;
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

    cropImage.addEventListener("load", function () {
        if (!pendingImageSource) return;
        if (!modalEl || modalEl.classList.contains("show")) {
            initCropper();
        }
    });

    input.addEventListener("change", function (event) {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        openEditorFromFile(file);
    });

    if (modalEl) {
        modalEl.addEventListener("shown.bs.modal", function () {
            if (pendingImageSource && cropImage.complete && cropImage.naturalWidth > 0) {
                initCropper();
            }
        });

        modalEl.addEventListener("hidden.bs.modal", function () {
            destroyCropper();

            if (!cropApplied) {
                input.value = "";
                hiddenInput.value = "";
            }
        });
    }

    if (zoomRange) {
        zoomRange.addEventListener("input", function () {
            if (!cropper) return;

            const currentValue = Number(this.value || 0);
            const delta = (currentValue - lastZoomValue) / 35;

            cropper.zoom(delta);
            lastZoomValue = currentValue;

            window.setTimeout(function () {
                ensureImageCoversCropCircle();
                updatePreviewFromCropper();
            }, 0);
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;

            cropper.rotate(90);
            window.setTimeout(function () {
                lockGmailStyleCircle();
            }, 0);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (!cropper) return;

            cropper.reset();
            resetZoomSlider();

            window.setTimeout(function () {
                lockGmailStyleCircle();
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

    window.addEventListener("resize", function () {
        if (!cropper) return;
        window.setTimeout(function () {
            lockGmailStyleCircle();
        }, 100);
    });

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
'''

js_path.write_text(new_js, encoding="utf-8")
print("Avatar editor je zamijenjen Gmail-style verzijom.")
print(f"Backup stare verzije: {backup_path}")
print("Sada pokreni: python manage.py check")
