from pathlib import Path
import re
from datetime import datetime

GOOD_AVATAR_JS = r'''document.addEventListener("DOMContentLoaded", function () {
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

    if (!form || !input || !hiddenInput || !modalEl || !cropImage) {
        return;
    }

    // File input mora biti sakriven. Koristi se samo gumb "Odaberi i uredi avatar".
    input.classList.add("d-none");
    input.style.display = "none";

    const frame = modalEl.querySelector(".avatar-crop-frame") || cropImage.parentElement;
    let avatarModal = null;
    let manualBackdrop = null;
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
        cropSize: 170,
        naturalWidth: 0,
        naturalHeight: 0,
    };

    if (window.bootstrap) {
        avatarModal = new bootstrap.Modal(modalEl);
    }

    function showAvatarModal() {
        if (avatarModal) {
            avatarModal.show();
            return;
        }

        modalEl.style.display = "block";
        modalEl.removeAttribute("aria-hidden");
        modalEl.setAttribute("aria-modal", "true");
        modalEl.classList.add("show");
        document.body.classList.add("modal-open");

        if (!manualBackdrop) {
            manualBackdrop = document.createElement("div");
            manualBackdrop.className = "modal-backdrop fade show";
            document.body.appendChild(manualBackdrop);
        }

        setTimeout(function () {
            modalEl.dispatchEvent(new Event("shown.bs.modal"));
        }, 0);
    }

    function hideAvatarModal() {
        if (avatarModal) {
            avatarModal.hide();
            return;
        }

        modalEl.classList.remove("show");
        modalEl.style.display = "none";
        modalEl.setAttribute("aria-hidden", "true");
        modalEl.removeAttribute("aria-modal");
        document.body.classList.remove("modal-open");

        if (manualBackdrop) {
            manualBackdrop.remove();
            manualBackdrop = null;
        }
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
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = "high";
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

    function updateCropSize() {
        const rect = getFrameRect();
        const size = Math.round(Math.min(rect.width, rect.height) * 0.62);
        state.cropSize = Math.max(130, Math.min(size, 170));
        frame.style.setProperty("--avatar-crop-size", state.cropSize + "px");
    }

    function clampPosition() {
        const rect = getFrameRect();
        const baseSize = getRotatedBaseSize();
        const renderedWidth = baseSize.width * state.scale;
        const renderedHeight = baseSize.height * state.scale;

        const halfCrop = state.cropSize / 2;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const minX = centerX + halfCrop - renderedWidth / 2;
        const maxX = centerX - halfCrop + renderedWidth / 2;
        const minY = centerY + halfCrop - renderedHeight / 2;
        const maxY = centerY - halfCrop + renderedHeight / 2;

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

        updateCropSize();

        // Minimalni zoom se računa po krugu avatara.
        // Tako slika potpuno pokriva krug, ali se ipak može vidjeti što veći dio slike.
        state.minScale = Math.max(
            state.cropSize / baseSize.width,
            state.cropSize / baseSize.height
        );

        state.scale = state.minScale;
        state.x = rect.width / 2;
        state.y = rect.height / 2;

        if (zoomRange) {
            zoomRange.min = "0";
            zoomRange.max = "100";
            zoomRange.step = "1";
            zoomRange.value = "0";
        }

        clampPosition();
        updateImageTransform();
    }

    function getScaleForZoomValue(value) {
        const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
        const zoomFactor = 1 + (safeValue / 100) * 3;
        return state.minScale * zoomFactor;
    }

    function setZoomValue(nextValue) {
        if (!imageLoaded || !zoomRange) return;

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
        updatePreviewFromEditor();
    }

    function handleZoomChange() {
        if (!imageLoaded || !zoomRange) return;
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

    function getCroppedCanvas(size) {
        if (!imageLoaded) return null;

        const stageCanvas = drawStageToCanvas();
        const rect = getFrameRect();
        const sourceSize = state.cropSize;
        const sourceX = Math.round(rect.width / 2 - sourceSize / 2);
        const sourceY = Math.round(rect.height / 2 - sourceSize / 2);

        const outputCanvas = document.createElement("canvas");
        outputCanvas.width = size;
        outputCanvas.height = size;

        const ctx = outputCanvas.getContext("2d");
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = "high";
        ctx.drawImage(stageCanvas, sourceX, sourceY, sourceSize, sourceSize, 0, 0, size, size);

        return outputCanvas;
    }

    function updatePreviewFromEditor() {
        const canvas = getCroppedCanvas(320);

        if (canvas) {
            renderImagePreview(canvas);
        }
    }

    function applyCropToHiddenInput() {
        const canvas = getCroppedCanvas(1200);
        if (!canvas) return false;

        hiddenInput.value = canvas.toDataURL("image/png");
        renderImagePreview(canvas);
        return true;
    }

    function setupImageAfterLoad() {
        imageLoaded = true;
        state.naturalWidth = cropImage.naturalWidth;
        state.naturalHeight = cropImage.naturalHeight;
        state.rotation = 0;
        hiddenInput.value = "";

        requestAnimationFrame(function () {
            calculateInitialState();
            updatePreviewFromEditor();
        });
    }

    function openEditorFromFile(file) {
        if (!file || !file.type || !file.type.startsWith("image/")) return;

        const reader = new FileReader();
        reader.onload = function (event) {
            imageLoaded = false;
            cropImage.src = event.target.result;
            showAvatarModal();
        };
        reader.readAsDataURL(file);
    }

    if (triggerBtn) {
        triggerBtn.addEventListener("click", function (event) {
            event.preventDefault();
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
            if (!avatarModal || modalEl.classList.contains("show")) {
                setupImageAfterLoad();
            }
        }
    });

    modalEl.addEventListener("shown.bs.modal", function () {
        if (cropImage.complete && cropImage.naturalWidth > 0 && cropImage.naturalHeight > 0) {
            setupImageAfterLoad();
        }
    });

    if (zoomRange) {
        zoomRange.addEventListener("input", handleZoomChange);
    }

    frame.addEventListener("wheel", function (event) {
        if (!imageLoaded || !zoomRange) return;

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
        updatePreviewFromEditor();
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
            updatePreviewFromEditor();
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener("click", function () {
            if (!imageLoaded) return;

            state.rotation = 0;
            calculateInitialState();
            updatePreviewFromEditor();
        });
    }

    if (applyBtn) {
        applyBtn.addEventListener("click", function () {
            const applied = applyCropToHiddenInput();

            if (applied) {
                hideAvatarModal();
            }
        });
    }

    form.addEventListener("submit", function (event) {
        const submitter = event.submitter;

        if (submitter && submitter.name === "delete_avatar") {
            hiddenInput.value = "";
            return;
        }

        if (imageLoaded && !hiddenInput.value) {
            applyCropToHiddenInput();
        }
    });

    window.addEventListener("resize", function () {
        if (!imageLoaded || !modalEl.classList.contains("show")) return;

        calculateInitialState();
        updatePreviewFromEditor();
    });

    if (currentAvatarImage) {
        if (currentAvatarImage.complete) {
            renderImagePreview(currentAvatarImage);
        } else {
            currentAvatarImage.addEventListener("load", function () {
                renderImagePreview(currentAvatarImage);
            }, { once: true });
        }
    }
});
'''


def find_project_root() -> Path:
    start = Path.cwd().resolve()
    candidates = [start] + list(start.parents)
    for c in candidates:
        if (c / "manage.py").exists() and (c / "blog").exists():
            return c
    # Ako je skripta u scripts folderu, probaj roditelja.
    if start.name.lower() == "scripts" and (start.parent / "manage.py").exists():
        return start.parent
    raise SystemExit("Nisam našao glavni folder projekta. Pokreni iz foldera gdje je manage.py ili iz scripts foldera.")


def backup_file(path: Path) -> None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".avatar_backup_{stamp}")
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Backup: {backup}")


def patch_template(template_path: Path) -> None:
    text = template_path.read_text(encoding="utf-8")
    original = text

    # Sakrij native file input za avatar ako se slučajno prikazuje.
    def fix_avatar_input(match):
        tag = match.group(0)
        if "d-none" not in tag:
            if "class=" in tag:
                tag = re.sub(r'class=(\"|\')([^\"\']*)(\"|\')', lambda m: f'class={m.group(1)}{m.group(2)} d-none{m.group(3)}', tag, count=1)
            else:
                tag = tag[:-1] + ' class="d-none">'
        # osiguraj da je id dobar
        if 'id=' not in tag:
            tag = tag[:-1] + ' id="avatarInput">'
        return tag

    text = re.sub(
        r'<input\b(?=[^>]*\btype=[\"\']file[\"\'])(?=[^>]*\bname=[\"\']avatar[\"\'])[^>]*>',
        fix_avatar_input,
        text,
        flags=re.IGNORECASE,
    )

    # Ako hidden cropped input nedostaje, dodaj ga odmah poslije avatar inputa.
    if 'id="croppedImage"' not in text and "id='croppedImage'" not in text:
        text = re.sub(
            r'(<input\b(?=[^>]*\btype=[\"\']file[\"\'])(?=[^>]*\bname=[\"\']avatar[\"\'])[^>]*>)',
            r'\1\n<input type="hidden" name="cropped_image" id="croppedImage">',
            text,
            count=1,
            flags=re.IGNORECASE,
        )

    # Osvježi cache za avatar JS.
    text = re.sub(
        r"\{\% static ['\"]blog/js/blog_settings_avatar\.js['\"] \%\}(\?v=[^'\"]*)?",
        "{% static 'blog/js/blog_settings_avatar.js' %}?v=avatar_restore_3",
        text,
    )

    if text != original:
        backup_file(template_path)
        template_path.write_text(text, encoding="utf-8")
        print("Popravljen template: _settings_tab.html")
    else:
        print("Template nije trebalo mijenjati.")


def main():
    root = find_project_root()
    print("=== Vraćanje avatar editora ===")
    print(f"Projekt: {root}")

    avatar_js = root / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
    template = root / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

    missing = [p for p in [avatar_js, template] if not p.exists()]
    if missing:
        print("Nisam našao ove datoteke:")
        for p in missing:
            print("-", p)
        raise SystemExit(1)

    backup_file(avatar_js)
    avatar_js.write_text(GOOD_AVATAR_JS, encoding="utf-8")
    print("Popravljen JS: blog_settings_avatar.js")

    patch_template(template)

    print("\nGOTOVO.")
    print("Sada pokreni server i u browseru napravi Ctrl + F5.")
    print("Test: Odaberi i uredi avatar -> odaberi sliku -> mora se otvoriti editor -> kotačić miša mora zumirati.")


if __name__ == "__main__":
    main()
