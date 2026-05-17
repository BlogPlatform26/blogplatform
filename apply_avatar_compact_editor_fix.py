from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if not js_path.exists():
    raise SystemExit(f"Nisam našao file: {js_path}\nPokreni skriptu iz root foldera projekta, tamo gdje je manage.py.")

backup_path = js_path.with_suffix(js_path.suffix + ".bak_avatar_compact_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup_path.write_text(js_path.read_text(encoding="utf-8"), encoding="utf-8")

new_js = r'''document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let pendingImageSource = "";
    let minZoomRatio = 1;
    let maxZoomRatio = 4;
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

    if (!form || !input || !hiddenInput || !previewCanvas || !previewMiniCanvas || !modalEl || !cropImage) {
        return;
    }

    addCompactAvatarStyles();
    prepareModalLayout();

    if (window.bootstrap) {
        avatarModal = new bootstrap.Modal(modalEl);
    }

    function addCompactAvatarStyles() {
        if (document.getElementById("avatarCompactEditorFixStyles")) {
            return;
        }

        const style = document.createElement("style");
        style.id = "avatarCompactEditorFixStyles";
        style.textContent = `
            #avatarCropModal .modal-dialog {
                max-width: 760px !important;
                margin: 1.1rem auto !important;
            }

            #avatarCropModal .modal-content {
                border-radius: 22px !important;
                overflow: hidden !important;
            }

            #avatarCropModal .modal-header {
                padding: 14px 20px 6px !important;
                border-bottom: 0 !important;
            }

            #avatarCropModal .modal-title,
            #avatarCropModal h5,
            #avatarCropModal h4 {
                font-size: 1.35rem !important;
                line-height: 1.2 !important;
                margin: 0 !important;
            }

            #avatarCropModal .btn-close {
                width: 0.8rem !important;
                height: 0.8rem !important;
                padding: 0.55rem !important;
                margin: 0 !important;
                transform: scale(0.85) !important;
            }

            #avatarCropModal .modal-body {
                padding: 8px 20px 16px !important;
            }

            #avatarCropModal .avatar-editor-help {
                margin: 0 0 8px !important;
                font-size: 0.92rem !important;
                opacity: 0.85 !important;
            }

            #avatarCropModal .avatar-editor-area {
                height: 310px !important;
                min-height: 260px !important;
                max-height: calc(100vh - 270px) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                overflow: hidden !important;
                border-radius: 18px !important;
                padding: 0 !important;
            }

            #avatarCropModal #avatarCropImage {
                display: block !important;
                max-width: 100% !important;
            }

            #avatarCropModal .cropper-container {
                max-width: 100% !important;
            }

            #avatarCropModal .cropper-view-box,
            #avatarCropModal .cropper-face {
                border-radius: 50% !important;
            }

            #avatarCropModal .cropper-view-box {
                outline: 3px solid #ffffff !important;
                outline-offset: -1px !important;
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.48) !important;
            }

            #avatarCropModal .cropper-line,
            #avatarCropModal .cropper-point {
                display: none !important;
            }

            #avatarCropModal .avatar-editor-controls {
                display: grid !important;
                grid-template-columns: 90px 1fr !important;
                gap: 12px !important;
                align-items: center !important;
                margin-top: 10px !important;
            }

            #avatarCropModal .avatar-editor-controls label,
            #avatarCropModal .avatar-editor-controls .form-label {
                margin: 0 !important;
                font-size: 1rem !important;
            }

            #avatarCropModal .avatar-editor-actions {
                display: flex !important;
                justify-content: space-between !important;
                align-items: center !important;
                gap: 10px !important;
                margin-top: 12px !important;
            }

            #avatarCropModal .avatar-editor-actions-left,
            #avatarCropModal .avatar-editor-actions-right {
                display: flex !important;
                gap: 8px !important;
                align-items: center !important;
            }

            #avatarCropModal .btn {
                padding: 0.42rem 0.75rem !important;
                font-size: 0.95rem !important;
                border-radius: 8px !important;
            }

            #avatarCropModal #avatarApplyBtn {
                padding: 0.52rem 0.95rem !important;
                min-width: 150px !important;
            }

            @media (max-height: 720px) {
                #avatarCropModal .avatar-editor-area {
                    height: 270px !important;
                    max-height: calc(100vh - 245px) !important;
                }

                #avatarCropModal .modal-header {
                    padding-top: 10px !important;
                }

                #avatarCropModal .modal-body {
                    padding-bottom: 12px !important;
                }
            }

            @media (max-width: 768px) {
                #avatarCropModal .modal-dialog {
                    max-width: calc(100vw - 20px) !important;
                    margin: 0.6rem auto !important;
                }

                #avatarCropModal .avatar-editor-area {
                    height: 260px !important;
                }

                #avatarCropModal .avatar-editor-controls {
                    grid-template-columns: 70px 1fr !important;
                }
            }
        `;
        document.head.appendChild(style);
    }

    function prepareModalLayout() {
        const modalBody = modalEl.querySelector(".modal-body");
        const cropParent = cropImage.parentElement;

        if (cropParent) {
            cropParent.classList.add("avatar-editor-area");
        }

        const helpText = Array.from(modalEl.querySelectorAll("p, .text-muted, .small")).find(function (el) {
            return (el.textContent || "").toLowerCase().includes("povuci") ||
                   (el.textContent || "").toLowerCase().includes("zumiraj");
        });
        if (helpText) {
            helpText.classList.add("avatar-editor-help");
        }

        if (zoomRange && modalBody) {
            const label = findZoomLabel(modalBody);
            const controls = document.createElement("div");
            controls.className = "avatar-editor-controls";

            if (label) {
                controls.appendChild(label);
            } else {
                const newLabel = document.createElement("label");
                newLabel.textContent = "Zum";
                newLabel.setAttribute("for", "avatarZoomRange");
                controls.appendChild(newLabel);
            }

            controls.appendChild(zoomRange);
            cropParent.insertAdjacentElement("afterend", controls);
        }

        if (rotateBtn && resetBtn && applyBtn && modalBody) {
            const actions = document.createElement("div");
            actions.className = "avatar-editor-actions";

            const left = document.createElement("div");
            left.className = "avatar-editor-actions-left";
            left.appendChild(rotateBtn);
            left.appendChild(resetBtn);

            const right = document.createElement("div");
            right.className = "avatar-editor-actions-right";
            right.appendChild(applyBtn);

            actions.appendChild(left);
            actions.appendChild(right);
            modalBody.appendChild(actions);
        }
    }

    function findZoomLabel(root) {
        const labels = Array.from(root.querySelectorAll("label, strong, span, div"));
        return labels.find(function (el) {
            return (el.textContent || "").trim().toLowerCase() === "zum";
        }) || null;
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
        if (canvas) {
            renderImagePreview(canvas);
        }
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

    function getCropDiameter() {
        const containerData = cropper.getContainerData();
        const safeWidth = Math.max(180, containerData.width - 52);
        const safeHeight = Math.max(180, containerData.height - 52);
        return Math.floor(Math.min(300, safeWidth, safeHeight));
    }

    function setFixedCenteredCropBox() {
        if (!cropper) return;
        const containerData = cropper.getContainerData();
        const diameter = getCropDiameter();
        const left = Math.round((containerData.width - diameter) / 2);
        const top = Math.round((containerData.height - diameter) / 2);

        cropper.setCropBoxData({
            left: left,
            top: top,
            width: diameter,
            height: diameter,
        });
    }

    function calculateMinZoomRatio() {
        const imageData = cropper.getImageData();
        const cropBoxData = cropper.getCropBoxData();

        const naturalWidth = Math.max(1, imageData.naturalWidth || cropImage.naturalWidth || 1);
        const naturalHeight = Math.max(1, imageData.naturalHeight || cropImage.naturalHeight || 1);

        return Math.max(
            (cropBoxData.width + 4) / naturalWidth,
            (cropBoxData.height + 4) / naturalHeight
        );
    }

    function centerImageAtRatio(ratio) {
        if (!cropper) return;
        const imageData = cropper.getImageData();
        const cropBoxData = cropper.getCropBoxData();
        const naturalWidth = Math.max(1, imageData.naturalWidth || cropImage.naturalWidth || 1);
        const naturalHeight = Math.max(1, imageData.naturalHeight || cropImage.naturalHeight || 1);
        const width = naturalWidth * ratio;
        const height = naturalHeight * ratio;

        cropper.setCanvasData({
            width: width,
            height: height,
            left: cropBoxData.left + (cropBoxData.width / 2) - (width / 2),
            top: cropBoxData.top + (cropBoxData.height / 2) - (height / 2),
        });
    }

    function setZoomFromSlider() {
        if (!cropper || !zoomRange) return;
        const percent = Number(zoomRange.value || 0) / 100;
        const ratio = minZoomRatio + ((maxZoomRatio - minZoomRatio) * percent);
        const cropBoxData = cropper.getCropBoxData();

        cropper.zoomTo(ratio, {
            x: cropBoxData.left + cropBoxData.width / 2,
            y: cropBoxData.top + cropBoxData.height / 2,
        });
    }

    function resetEditorView() {
        if (!cropper) return;
        currentRotation = 0;
        cropper.reset();
        setFixedCenteredCropBox();
        minZoomRatio = calculateMinZoomRatio();
        maxZoomRatio = Math.max(minZoomRatio * 4, minZoomRatio + 0.5);
        centerImageAtRatio(minZoomRatio);
        if (zoomRange) {
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";
        }
        updatePreviewFromCropper();
    }

    function initCropper() {
        if (!cropImage || !cropImage.src) return;
        destroyCropper();
        hiddenInput.value = "";
        currentRotation = 0;

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
            modal: false,
            ready: function () {
                resetEditorView();
            },
            crop: function () {
                updatePreviewFromCropper();
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

    input.addEventListener("change", function (event) {
        const file = event.target.files && event.target.files[0];
        if (!file) return;
        openEditorFromFile(file);
    });

    cropImage.addEventListener("load", function () {
        if (!pendingImageSource) return;
        if (!avatarModal || modalEl.classList.contains("show")) {
            initCropper();
        }
    });

    modalEl.addEventListener("shown.bs.modal", function () {
        if (pendingImageSource && cropImage.complete && cropImage.naturalWidth > 0) {
            initCropper();
        }
    });

    modalEl.addEventListener("hidden.bs.modal", function () {
        destroyCropper();
    });

    if (zoomRange) {
        zoomRange.addEventListener("input", function () {
            setZoomFromSlider();
            updatePreviewFromCropper();
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;
            currentRotation = (currentRotation + 90) % 360;
            cropper.rotateTo(currentRotation);
            setFixedCenteredCropBox();
            minZoomRatio = calculateMinZoomRatio();
            maxZoomRatio = Math.max(minZoomRatio * 4, minZoomRatio + 0.5);
            if (zoomRange) zoomRange.value = "0";
            centerImageAtRatio(minZoomRatio);
            updatePreviewFromCropper();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            resetEditorView();
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
'''

js_path.write_text(new_js, encoding="utf-8")
print("OK: Avatar editor je smanjen i uređen.")
print(f"Backup starog JS-a: {backup_path}")
print("Sada pokreni: python manage.py check")
