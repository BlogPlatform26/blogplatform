from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
template_paths = [
    ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html",
    ROOT / "blog" / "templates" / "blog" / "blog_settings.html",
]

if not js_path.exists():
    raise SystemExit(f"Nisam pronašao file: {js_path}\nPokreni skriptu iz root foldera projekta, tamo gdje je manage.py.")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_js = js_path.with_suffix(js_path.suffix + f".bak_before_avatar_clean_ui_{stamp}")
backup_js.write_text(js_path.read_text(encoding="utf-8"), encoding="utf-8")

new_js = r'''document.addEventListener("DOMContentLoaded", function () {
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
        const oldStyleIds = [
            "avatar-normal-editor-style",
            "avatarCompactEditorFixStyles",
            "avatar-clean-compact-v2-style"
        ];

        oldStyleIds.forEach(function (styleId) {
            const oldStyle = document.getElementById(styleId);
            if (oldStyle) oldStyle.remove();
        });

        const style = document.createElement("style");
        style.id = "avatar-clean-compact-v2-style";
        style.textContent = `
            #avatarCropModal .modal-dialog {
                max-width: 640px !important;
                width: calc(100% - 28px) !important;
                margin: 14px auto !important;
            }

            #avatarCropModal .modal-content {
                border-radius: 22px !important;
                overflow: hidden !important;
                max-height: calc(100vh - 28px) !important;
            }

            #avatarCropModal .modal-header {
                padding: 16px 20px 8px 20px !important;
                border-bottom: 0 !important;
                align-items: flex-start !important;
            }

            #avatarCropModal .modal-title,
            #avatarCropModal h4,
            #avatarCropModal h5 {
                font-size: 1.35rem !important;
                line-height: 1.2 !important;
                margin: 0 !important;
            }

            #avatarCropModal .modal-header .text-muted,
            #avatarCropModal .modal-header p,
            #avatarCropModal .modal-body > p:first-child {
                font-size: 0.95rem !important;
                margin-top: 4px !important;
                margin-bottom: 0 !important;
            }

            #avatarCropModal .btn-close {
                width: 0.85rem !important;
                height: 0.85rem !important;
                padding: 0.55rem !important;
                margin: 0 !important;
                opacity: 0.75 !important;
            }

            #avatarCropModal .modal-body {
                padding: 10px 18px 18px 18px !important;
            }

            #avatarCropModal .avatar-crop-stage {
                width: 100% !important;
                max-width: 500px !important;
                height: 300px !important;
                margin: 0 auto 14px auto !important;
                border-radius: 18px !important;
                overflow: hidden !important;
                background: #050b12 !important;
                border: 1px solid rgba(255, 255, 255, 0.16) !important;
            }

            #avatarCropModal .avatar-crop-stage img {
                display: block !important;
                max-width: 100% !important;
            }

            #avatarCropModal .cropper-container {
                width: 100% !important;
                height: 100% !important;
            }

            #avatarCropModal .cropper-view-box {
                border-radius: 50% !important;
                outline: 3px solid rgba(255, 255, 255, 0.96) !important;
                box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.50) !important;
            }

            #avatarCropModal .cropper-face {
                border-radius: 50% !important;
                background-color: transparent !important;
            }

            #avatarCropModal .cropper-dashed,
            #avatarCropModal .cropper-center,
            #avatarCropModal .cropper-line,
            #avatarCropModal .cropper-point {
                display: none !important;
            }

            #avatarCropModal .cropper-crop-box {
                outline: none !important;
            }

            #avatarCropModal .avatar-zoom-row {
                max-width: 500px !important;
                margin: 0 auto 12px auto !important;
            }

            #avatarCropModal .avatar-zoom-row label,
            #avatarCropModal label[for="avatarZoomRange"] {
                font-size: 0.95rem !important;
                margin-bottom: 4px !important;
            }

            #avatarCropModal input[type="range"] {
                height: 1.2rem !important;
            }

            #avatarCropModal .avatar-actions-row {
                max-width: 500px !important;
                margin-left: auto !important;
                margin-right: auto !important;
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                gap: 12px !important;
            }

            #avatarCropModal .avatar-actions-row .btn,
            #avatarCropModal #avatarRotateBtn,
            #avatarCropModal #avatarResetBtn,
            #avatarCropModal #avatarApplyBtn {
                padding: 0.45rem 0.8rem !important;
                font-size: 0.95rem !important;
                line-height: 1.2 !important;
                border-radius: 8px !important;
            }

            #avatarCropModal #avatarApplyBtn {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                min-width: 150px !important;
            }

            @media (max-width: 576px) {
                #avatarCropModal .modal-dialog {
                    width: calc(100% - 16px) !important;
                    margin: 8px auto !important;
                }

                #avatarCropModal .modal-header {
                    padding: 14px 14px 6px 14px !important;
                }

                #avatarCropModal .modal-body {
                    padding: 8px 12px 14px 12px !important;
                }

                #avatarCropModal .avatar-crop-stage {
                    height: 260px !important;
                }

                #avatarCropModal .avatar-actions-row {
                    flex-wrap: wrap !important;
                }

                #avatarCropModal #avatarApplyBtn {
                    margin-left: auto !important;
                }
            }
        `;
        document.head.appendChild(style);
    }

    function prepareStage() {
        if (cropImage && cropImage.parentElement) {
            cropImage.parentElement.classList.add("avatar-crop-stage");
        }

        if (zoomRange && zoomRange.parentElement) {
            zoomRange.parentElement.classList.add("avatar-zoom-row");
        }

        if (applyBtn && applyBtn.parentElement) {
            applyBtn.parentElement.classList.add("avatar-actions-row");
        }

        if (resetBtn && resetBtn.textContent.trim().toLowerCase() === "reset") {
            resetBtn.textContent = "Vrati";
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
        if (!cropper) return 210;

        const containerData = cropper.getContainerData();
        const maxWidth = Math.max(170, containerData.width - 110);
        const maxHeight = Math.max(170, containerData.height - 90);

        return Math.round(Math.min(220, maxWidth, maxHeight));
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
        if (!cropImage || !cropImage.src || !window.Cropper) return;

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
                setTimeout(function () {
                    setFixedCenterCropBox();
                    updatePreviewFromCropper();
                }, 50);
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
'''

js_path.write_text(new_js, encoding="utf-8")

# Uredi neprofesionalne/privremene tekstove ako postoje u templateima.
replacements = {
    "Okrugli izrez kao na Gmailu, s pomicanjem, zoomom i rotacijom.": "Dodajte profilnu sliku i prilagodite izrez prije spremanja.",
    "Povuci sliku, zumiraj i spremi okrugli izrez.": "Namjestite sliku unutar okvira prije spremanja.",
    "Povuci sliku, zumiraj i spremi okrugli izrez": "Namjestite sliku unutar okvira prije spremanja",
    "Obrezivanje avatara": "Uređivanje avatara",
    ">Reset<": ">Vrati<",
    ">Zum<": ">Uvećanje<",
}

changed_templates = []
for path in template_paths:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements.items():
        text = text.replace(old, new)
    if text != original:
        backup = path.with_suffix(path.suffix + f".bak_before_avatar_clean_ui_{stamp}")
        backup.write_text(original, encoding="utf-8")
        path.write_text(text, encoding="utf-8")
        changed_templates.append(str(path.relative_to(ROOT)))

print("OK: Avatar editor je uređen bez diranja bannera, modela, baze ili migracija.")
print(f"Backup JS-a: {backup_js}")
if changed_templates:
    print("Uređeni tekstovi u:")
    for item in changed_templates:
        print(f"- {item}")
else:
    print("Nisam našao tekstove za zamjenu u templateima. To nije greška.")
print("Sada pokreni: python manage.py check")
