document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector('input[name="blog_banner"]');

    if (!input) {
        return;
    }

    const form = input.closest("form") || document.querySelector("form");

    if (!form) {
        return;
    }

    let hiddenInput = form.querySelector('input[name="cropped_blog_banner"]') || document.getElementById("croppedBlogBanner");

    if (!hiddenInput) {
        hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = "cropped_blog_banner";
        hiddenInput.id = "croppedBlogBanner";
        input.insertAdjacentElement("afterend", hiddenInput);
    }

    let infoText = document.getElementById("blogBannerEditorInfo");
    if (!infoText) {
        infoText = document.createElement("div");
        infoText.id = "blogBannerEditorInfo";
        infoText.className = "small text-muted mt-2";
        input.insertAdjacentElement("afterend", infoText);
    }

    const styleId = "blogBannerRectEditorStyle";
    if (!document.getElementById(styleId)) {
        const style = document.createElement("style");
        style.id = styleId;
        style.textContent = `
            #bannerCropModal .modal-dialog { max-width: 820px; }
            #bannerCropModal .modal-content { border-radius: 18px; overflow: hidden; }
            .banner-crop-stage { position: relative; width: 100%; height: 360px; background: #080b12; overflow: hidden; border-radius: 14px; user-select: none; touch-action: none; }
            .banner-crop-stage img { position: absolute; left: 0; top: 0; max-width: none; transform-origin: center center; cursor: grab; user-select: none; -webkit-user-drag: none; }
            .banner-crop-stage img.is-dragging { cursor: grabbing; }
            .banner-crop-rect { position: absolute; left: 50%; top: 50%; width: min(92%, 680px); aspect-ratio: 22 / 9; transform: translate(-50%, -50%); border: 2px solid rgba(255,255,255,0.98); box-shadow: 0 0 0 9999px rgba(0,0,0,0.48); border-radius: 8px; pointer-events: none; z-index: 4; }
            .banner-crop-grid { position: absolute; inset: 0; background: linear-gradient(to right, transparent 33.333%, rgba(255,255,255,0.42) 33.333%, rgba(255,255,255,0.42) 33.7%, transparent 33.7%, transparent 66.333%, rgba(255,255,255,0.42) 66.333%, rgba(255,255,255,0.42) 66.7%, transparent 66.7%), linear-gradient(to bottom, transparent 33.333%, rgba(255,255,255,0.42) 33.333%, rgba(255,255,255,0.42) 33.7%, transparent 33.7%, transparent 66.333%, rgba(255,255,255,0.42) 66.333%, rgba(255,255,255,0.42) 66.7%, transparent 66.7%); opacity: 0.5; }
            #bannerCropModal .modal-title { font-size: 1.15rem; }
            #bannerCropModal .btn { padding: 0.38rem 0.72rem; font-size: 0.92rem; }
            #bannerZoomRange { max-width: 420px; }
            @media (max-width: 768px) { #bannerCropModal .modal-dialog { max-width: calc(100vw - 18px); margin: 9px auto; } .banner-crop-stage { height: 280px; } }
        `;
        document.head.appendChild(style);
    }

    let modalEl = document.getElementById("bannerCropModal");

    if (!modalEl) {
        modalEl = document.createElement("div");
        modalEl.id = "bannerCropModal";
        modalEl.className = "modal fade";
        modalEl.tabIndex = -1;
        modalEl.setAttribute("aria-hidden", "true");
        modalEl.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header py-2">
                        <h5 class="modal-title">Uređivanje bannera</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Zatvori"></button>
                    </div>
                    <div class="modal-body">
                        <div class="banner-crop-stage" id="bannerCropStage">
                            <img id="bannerCropImage" alt="Uređivanje bannera">
                            <div class="banner-crop-rect"><div class="banner-crop-grid"></div></div>
                        </div>
                        <div class="mt-3">
                            <label for="bannerZoomRange" class="form-label mb-1">Uvećanje</label>
                            <input type="range" class="form-range" id="bannerZoomRange" min="0" max="100" step="1" value="0">
                        </div>
                    </div>
                    <div class="modal-footer py-2">
                        <button type="button" class="btn btn-outline-secondary" id="bannerRotateBtn">Zakreni</button>
                        <button type="button" class="btn btn-outline-secondary" id="bannerResetBtn">Vrati</button>
                        <button type="button" class="btn btn-primary" id="bannerApplyBtn">Primijeni banner</button>
                    </div>
                </div>
            </div>`;
        document.body.appendChild(modalEl);
    }

    const stage = modalEl.querySelector("#bannerCropStage");
    const cropImage = modalEl.querySelector("#bannerCropImage");
    const cropRect = modalEl.querySelector(".banner-crop-rect");
    const zoomRange = modalEl.querySelector("#bannerZoomRange");
    const rotateBtn = modalEl.querySelector("#bannerRotateBtn");
    const resetBtn = modalEl.querySelector("#bannerResetBtn");
    const applyBtn = modalEl.querySelector("#bannerApplyBtn");

    let bannerModal = null;
    if (window.bootstrap) {
        bannerModal = new bootstrap.Modal(modalEl);
    }

    const state = { x: 0, y: 0, scale: 1, minScale: 1, rotation: 0, naturalWidth: 0, naturalHeight: 0, imageLoaded: false, dragging: false, dragStartX: 0, dragStartY: 0, startX: 0, startY: 0 };

    function getStageRect() { return stage.getBoundingClientRect(); }
    function getCropBox() {
        const stageRect = getStageRect();
        const rect = cropRect.getBoundingClientRect();
        return { x: rect.left - stageRect.left, y: rect.top - stageRect.top, width: rect.width, height: rect.height };
    }
    function getRotatedBaseSize() {
        const normalized = ((state.rotation % 360) + 360) % 360;
        if (normalized === 90 || normalized === 270) { return { width: state.naturalHeight, height: state.naturalWidth }; }
        return { width: state.naturalWidth, height: state.naturalHeight };
    }
    function updateTransform() {
        cropImage.style.width = state.naturalWidth + "px";
        cropImage.style.height = state.naturalHeight + "px";
        cropImage.style.transform = "translate(" + (state.x - state.naturalWidth / 2) + "px, " + (state.y - state.naturalHeight / 2) + "px) rotate(" + state.rotation + "deg) scale(" + state.scale + ")";
    }
    function clampPosition() {
        const crop = getCropBox();
        const base = getRotatedBaseSize();
        const renderedWidth = base.width * state.scale;
        const renderedHeight = base.height * state.scale;
        const minX = crop.x + crop.width - renderedWidth / 2;
        const maxX = crop.x + renderedWidth / 2;
        const minY = crop.y + crop.height - renderedHeight / 2;
        const maxY = crop.y + renderedHeight / 2;
        if (minX <= maxX) state.x = Math.min(maxX, Math.max(minX, state.x));
        if (minY <= maxY) state.y = Math.min(maxY, Math.max(minY, state.y));
    }
    function calculateInitialState() {
        const stageRect = getStageRect();
        const crop = getCropBox();
        const base = getRotatedBaseSize();
        state.minScale = Math.max(crop.width / base.width, crop.height / base.height);
        state.scale = state.minScale;
        state.x = stageRect.width / 2;
        state.y = stageRect.height / 2;
        zoomRange.value = "0";
        clampPosition();
        updateTransform();
    }
    function getScaleFromRange(value) {
        const safeValue = Math.max(0, Math.min(100, Number(value || 0)));
        return state.minScale * (1 + (safeValue / 100) * 3);
    }
    function setZoomValue(value) {
        if (!state.imageLoaded) return;
        const oldScale = state.scale;
        const nextValue = Math.max(0, Math.min(100, Number(value || 0)));
        const nextScale = getScaleFromRange(nextValue);
        const stageRect = getStageRect();
        const centerX = stageRect.width / 2;
        const centerY = stageRect.height / 2;
        const ratio = nextScale / oldScale;
        state.x = centerX + (state.x - centerX) * ratio;
        state.y = centerY + (state.y - centerY) * ratio;
        state.scale = nextScale;
        zoomRange.value = String(nextValue);
        clampPosition();
        updateTransform();
    }
    function drawStageToCanvas() {
        const stageRect = getStageRect();
        const canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.round(stageRect.width));
        canvas.height = Math.max(1, Math.round(stageRect.height));
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "#05080d";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.save();
        ctx.translate(state.x, state.y);
        ctx.rotate((state.rotation * Math.PI) / 180);
        ctx.scale(state.scale, state.scale);
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = "high";
        ctx.drawImage(cropImage, -state.naturalWidth / 2, -state.naturalHeight / 2, state.naturalWidth, state.naturalHeight);
        ctx.restore();
        return canvas;
    }
    function getCroppedBannerData() {
        if (!state.imageLoaded) return "";
        const stageCanvas = drawStageToCanvas();
        const crop = getCropBox();
        const outputCanvas = document.createElement("canvas");
        outputCanvas.width = 2200;
        outputCanvas.height = 900;
        const ctx = outputCanvas.getContext("2d");
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = "high";
        ctx.drawImage(stageCanvas, crop.x, crop.y, crop.width, crop.height, 0, 0, outputCanvas.width, outputCanvas.height);
        return outputCanvas.toDataURL("image/jpeg", 0.94);
    }
    function applyBanner() {
        const data = getCroppedBannerData();
        if (!data) return false;
        hiddenInput.value = data;
        infoText.textContent = "Banner je pripremljen. Klikni Spremi promjene za završetak.";
        return true;
    }
    function openEditorFromFile(file) {
        if (!file || !file.type || !file.type.startsWith("image/")) return;
        const reader = new FileReader();
        reader.onload = function (event) {
            state.imageLoaded = false;
            hiddenInput.value = "";
            infoText.textContent = "";
            cropImage.src = event.target.result;
            if (bannerModal) bannerModal.show();
            else { modalEl.style.display = "block"; modalEl.classList.add("show"); modalEl.removeAttribute("aria-hidden"); }
        };
        reader.readAsDataURL(file);
    }

    input.addEventListener("change", function () {
        const file = input.files && input.files[0];
        if (!file) return;
        openEditorFromFile(file);
    });
    cropImage.addEventListener("load", function () {
        if (!cropImage.naturalWidth || !cropImage.naturalHeight) return;
        state.naturalWidth = cropImage.naturalWidth;
        state.naturalHeight = cropImage.naturalHeight;
        state.rotation = 0;
        state.imageLoaded = true;
        requestAnimationFrame(calculateInitialState);
    });
    modalEl.addEventListener("shown.bs.modal", function () { if (state.imageLoaded) requestAnimationFrame(calculateInitialState); });
    zoomRange.addEventListener("input", function () { setZoomValue(zoomRange.value); });
    stage.addEventListener("wheel", function (event) {
        if (!state.imageLoaded) return;
        event.preventDefault();
        const currentValue = Number(zoomRange.value || 0);
        const step = event.deltaY < 0 ? 4 : -4;
        setZoomValue(currentValue + step);
    }, { passive: false });
    stage.addEventListener("pointerdown", function (event) {
        if (!state.imageLoaded) return;
        state.dragging = true;
        cropImage.classList.add("is-dragging");
        stage.setPointerCapture(event.pointerId);
        state.dragStartX = event.clientX;
        state.dragStartY = event.clientY;
        state.startX = state.x;
        state.startY = state.y;
    });
    stage.addEventListener("pointermove", function (event) {
        if (!state.dragging || !state.imageLoaded) return;
        state.x = state.startX + (event.clientX - state.dragStartX);
        state.y = state.startY + (event.clientY - state.dragStartY);
        clampPosition();
        updateTransform();
    });
    function stopDragging(event) {
        if (!state.dragging) return;
        state.dragging = false;
        cropImage.classList.remove("is-dragging");
        if (event && stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
    }
    stage.addEventListener("pointerup", stopDragging);
    stage.addEventListener("pointercancel", stopDragging);
    stage.addEventListener("pointerleave", stopDragging);
    rotateBtn.addEventListener("click", function () { if (!state.imageLoaded) return; state.rotation = (state.rotation + 90) % 360; calculateInitialState(); });
    resetBtn.addEventListener("click", function () { if (!state.imageLoaded) return; state.rotation = 0; calculateInitialState(); });
    applyBtn.addEventListener("click", function () { const ok = applyBanner(); if (ok && bannerModal) bannerModal.hide(); });
    form.addEventListener("submit", function () {
        const deleteBanner = form.querySelector('input[name="delete_blog_banner"]');
        if (deleteBanner && deleteBanner.value === "1") { hiddenInput.value = ""; return; }
        if (state.imageLoaded && !hiddenInput.value) applyBanner();
    });
    window.addEventListener("resize", function () { if (!state.imageLoaded || !modalEl.classList.contains("show")) return; calculateInitialState(); });
});
