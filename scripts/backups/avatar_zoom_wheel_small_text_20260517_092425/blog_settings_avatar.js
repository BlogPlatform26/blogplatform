document.addEventListener("DOMContentLoaded", function () {
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

    const frame = modalEl.querySelector(".avatar-crop-frame") || cropImage.parentElement;
    let avatarModal = null;
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

    function calculateInitialState() {
        const rect = getFrameRect();
        const baseSize = getRotatedBaseSize();
        updateCropSize();

        const fitScale = Math.min(rect.width / baseSize.width, rect.height / baseSize.height);
        const coverCropScale = Math.max(state.cropSize / baseSize.width, state.cropSize / baseSize.height);

        state.minScale = Math.max(fitScale, coverCropScale);
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
        const canvas = getCroppedCanvas(420);
        if (!canvas) return false;
        hiddenInput.value = canvas.toDataURL("image/jpeg", 0.92);
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
            if (avatarModal) {
                avatarModal.show();
            }
        };
        reader.readAsDataURL(file);
    }

    function handleZoomChange() {
        if (!imageLoaded || !zoomRange) return;
        const value = Number(zoomRange.value || 0);
        const zoomFactor = 1 + (value / 100) * 2.2;
        const centerX = getFrameRect().width / 2;
        const centerY = getFrameRect().height / 2;

        state.x = centerX + (state.x - centerX) * ((state.minScale * zoomFactor) / state.scale);
        state.y = centerY + (state.y - centerY) * ((state.minScale * zoomFactor) / state.scale);
        state.scale = state.minScale * zoomFactor;

        clampPosition();
        updateImageTransform();
        updatePreviewFromEditor();
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
