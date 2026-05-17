from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

if not HTML_PATH.exists():
    raise FileNotFoundError(f"Ne mogu naći: {HTML_PATH}")
if not JS_PATH.exists():
    raise FileNotFoundError(f"Ne mogu naći: {JS_PATH}")

backup_dir = ROOT / "backups" / f"avatar_normal_gmail_like_{STAMP}"
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(HTML_PATH, backup_dir / "_settings_tab.html")
shutil.copy2(JS_PATH, backup_dir / "blog_settings_avatar.js")

html = HTML_PATH.read_text(encoding="utf-8")

# Popravi tekstove u avatar sekciji da zvuče profesionalnije.
replacements = {
    "Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.": "Uredite avatar prije spremanja.",
    "Odaberi sliku, pomakni kadar, zumiraj i spremi okrugli izrez.": "Odaberite sliku i namjestite kadar prije spremanja.",
    "Povuci sliku, zumiraj i spremi okrugli izrez.": "Namjestite sliku unutar kruga prije spremanja.",
    "Zum": "Uvećanje",
    "Reset": "Vrati",
}
for old, new in replacements.items():
    html = html.replace(old, new)

# Ako su prethodni pokušaji slučajno ubacili CSS kao tekst unutar gumba, očisti gumbe po ID-u.
button_texts = {
    "avatarRotateBtn": "Zakreni",
    "avatarResetBtn": "Vrati",
    "avatarApplyBtn": "Primijeni avatar",
}
for button_id, text in button_texts.items():
    pattern = rf'(<button[^>]*id=["\\\']{button_id}["\\\'][^>]*>)(.*?)(</button>)'
    html = re.sub(pattern, rf'\1{text}\3', html, flags=re.DOTALL)

# Makni naše stare stilove ako postoje, da se ne gomilaju.
html = re.sub(
    r"\n?<!-- AVATAR_NORMAL_GMAIL_LIKE_START -->.*?<!-- AVATAR_NORMAL_GMAIL_LIKE_END -->\n?",
    "\n",
    html,
    flags=re.DOTALL,
)

style_block = r'''
<!-- AVATAR_NORMAL_GMAIL_LIKE_START -->
<style>
    /* Avatar editor - normalan, kompaktniji prikaz */
    #avatarCropModal .modal-dialog {
        max-width: 720px !important;
        width: min(720px, calc(100vw - 28px)) !important;
        margin: 18px auto !important;
    }

    #avatarCropModal .modal-content,
    #avatarCropModal .avatar-crop-modal {
        background: #111a2d !important;
        border-radius: 22px !important;
        padding: 18px 22px !important;
        border: 0 !important;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35) !important;
    }

    #avatarCropModal .modal-header {
        padding: 0 0 10px 0 !important;
        border-bottom: 0 !important;
    }

    #avatarCropModal .modal-title,
    #avatarCropModal h1,
    #avatarCropModal h2,
    #avatarCropModal h3 {
        font-size: 22px !important;
        line-height: 1.2 !important;
        margin: 0 0 4px 0 !important;
        font-weight: 700 !important;
    }

    #avatarCropModal p,
    #avatarCropModal .text-muted,
    #avatarCropModal .form-text {
        font-size: 13px !important;
        line-height: 1.35 !important;
        margin: 0 0 10px 0 !important;
        opacity: 0.8 !important;
    }

    #avatarCropModal .btn-close {
        width: 20px !important;
        height: 20px !important;
        padding: 4px !important;
        transform: scale(0.75) !important;
        opacity: 0.85 !important;
        margin: 0 !important;
    }

    #avatarCropModal .modal-body {
        padding: 0 !important;
    }

    #avatarCropModal .avatar-crop-frame,
    #avatarCropModal .avatar-crop-stage,
    #avatarCropModal .cropper-wrap,
    #avatarCropModal .cropper-area {
        max-width: 520px !important;
        height: 250px !important;
        max-height: 250px !important;
        margin: 0 auto 12px auto !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }

    #avatarCropModal #avatarCropImage {
        display: block !important;
        max-width: 100% !important;
        max-height: 250px !important;
    }

    #avatarCropModal .cropper-container {
        max-width: 520px !important;
        max-height: 250px !important;
    }

    #avatarCropModal .cropper-view-box,
    #avatarCropModal .cropper-face {
        border-radius: 50% !important;
    }

    #avatarCropModal .cropper-view-box {
        outline: 2px solid rgba(255,255,255,0.95) !important;
        outline-offset: -2px !important;
    }

    #avatarCropModal label,
    #avatarCropModal .form-label {
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-bottom: 0 !important;
    }

    #avatarCropModal input[type="range"] {
        height: 5px !important;
    }

    #avatarCropModal .avatar-crop-controls,
    #avatarCropModal .avatar-editor-controls {
        gap: 10px !important;
        margin-top: 8px !important;
    }

    #avatarCropModal .btn,
    #avatarCropModal button:not(.btn-close) {
        font-size: 13px !important;
        line-height: 1.2 !important;
        padding: 6px 10px !important;
        border-radius: 7px !important;
        min-height: 0 !important;
        min-width: 0 !important;
    }

    #avatarCropModal #avatarApplyBtn {
        font-size: 15px !important;
        padding: 8px 18px !important;
        min-width: 150px !important;
    }

    #avatarCropModal .modal-footer {
        padding: 10px 0 0 0 !important;
        border-top: 0 !important;
    }

    @media (max-width: 768px) {
        #avatarCropModal .modal-dialog {
            width: calc(100vw - 18px) !important;
            margin: 10px auto !important;
        }

        #avatarCropModal .modal-content,
        #avatarCropModal .avatar-crop-modal {
            padding: 14px !important;
        }

        #avatarCropModal .avatar-crop-frame,
        #avatarCropModal .avatar-crop-stage,
        #avatarCropModal .cropper-wrap,
        #avatarCropModal .cropper-area {
            height: 220px !important;
            max-height: 220px !important;
        }
    }
</style>
<!-- AVATAR_NORMAL_GMAIL_LIKE_END -->
'''

# Ubaci stil blizu kraja filea. Kasnije u dokumentu = jači od starijih stilova.
html = html.rstrip() + "\n" + style_block + "\n"
HTML_PATH.write_text(html, encoding="utf-8")

js = r'''document.addEventListener("DOMContentLoaded", function () {
    let cropper = null;
    let avatarModal = null;
    let pendingImageSource = "";
    let baseZoomRatio = null;
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

        baseZoomRatio = null;
    }

    function getSafeCropDiameter() {
        if (!cropper) return 160;

        const containerData = cropper.getContainerData();
        const canvasData = cropper.getCanvasData();

        const maxByContainer = Math.min(containerData.width, containerData.height) * 0.68;
        const maxByImage = Math.min(canvasData.width, canvasData.height) * 0.86;

        let diameter = Math.min(maxByContainer, maxByImage);
        diameter = Math.max(120, diameter);
        diameter = Math.min(diameter, 190);

        return Math.round(diameter);
    }

    function syncCropBoxToCenter() {
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

    function rememberBaseZoom() {
        if (!cropper) return;

        const canvasData = cropper.getCanvasData();
        const imageData = cropper.getImageData();

        if (!canvasData || !imageData || !imageData.naturalWidth) return;

        baseZoomRatio = canvasData.width / imageData.naturalWidth;

        if (zoomRange) {
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.value = "0";
        }
    }

    function queueCropBoxSync() {
        if (cropBoxSyncTimeout) clearTimeout(cropBoxSyncTimeout);

        cropBoxSyncTimeout = setTimeout(function () {
            syncCropBoxToCenter();
            updatePreviewFromCropper();
        }, 0);
    }

    function resetToFullImageView() {
        if (!cropper) return;

        cropper.reset();

        setTimeout(function () {
            syncCropBoxToCenter();
            rememberBaseZoom();
            updatePreviewFromCropper();
        }, 80);
    }

    function initCropper() {
        if (!cropImage || !cropImage.src || !window.Cropper) return;

        destroyCropper();
        hiddenInput.value = "";

        if (zoomRange) {
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.value = "0";
        }

        cropper = new Cropper(cropImage, {
            aspectRatio: 1,
            viewMode: 1,
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
            zoomOnWheel: false,
            ready() {
                setTimeout(function () {
                    syncCropBoxToCenter();
                    rememberBaseZoom();
                    updatePreviewFromCropper();
                }, 80);
            },
            crop() {
                updatePreviewFromCropper();
            },
            zoom(event) {
                if (baseZoomRatio && event.detail && event.detail.ratio < baseZoomRatio) {
                    event.preventDefault();
                    cropper.zoomTo(baseZoomRatio);
                    return;
                }

                queueCropBoxSync();
            },
        });
    }

    function openEditorFromFile(file) {
        if (!file) return;

        if (!file.type || !file.type.startsWith("image/")) {
            input.value = "";
            return;
        }

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
            if (!cropper || !baseZoomRatio) return;

            const currentValue = Number(this.value || 0);
            const zoomRatio = baseZoomRatio * (1 + currentValue / 40);

            cropper.zoomTo(zoomRatio);
            queueCropBoxSync();
        });
    }

    if (rotateBtn) {
        rotateBtn.addEventListener("click", function () {
            if (!cropper) return;

            cropper.rotate(90);

            setTimeout(function () {
                syncCropBoxToCenter();
                updatePreviewFromCropper();
            }, 80);
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            resetToFullImageView();
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

JS_PATH.write_text(js, encoding="utf-8")

rollback = ROOT / "scripts" / "rollback_avatar_normal_gmail_like.py"
rollback.parent.mkdir(parents=True, exist_ok=True)
rollback.write_text(f'''from pathlib import Path
import shutil

ROOT = Path.cwd()
BACKUP = ROOT / "backups" / "avatar_normal_gmail_like_{STAMP}"

html_backup = BACKUP / "_settings_tab.html"
js_backup = BACKUP / "blog_settings_avatar.js"
html_target = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
js_target = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if html_backup.exists():
    shutil.copy2(html_backup, html_target)
if js_backup.exists():
    shutil.copy2(js_backup, js_target)

print("Vraćeno stanje prije avatar_normal_gmail_like fixa.")
''', encoding="utf-8")

print("Avatar editor je postavljen na normalan prikaz.")
print(f"Backup je spremljen u: {backup_dir}")
print("Ako treba vratiti: python scripts\\rollback_avatar_normal_gmail_like.py")
