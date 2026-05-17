from pathlib import Path
import shutil

ROOT = Path.cwd()
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

JS_BACKUP = JS_PATH.with_suffix(JS_PATH.suffix + ".bak_avatar_zoom_wheel_text_v2")
HTML_BACKUP = HTML_PATH.with_suffix(HTML_PATH.suffix + ".bak_avatar_zoom_wheel_text_v2")

def backup_file(path, backup_path):
    if path.exists() and not backup_path.exists():
        shutil.copy2(path, backup_path)

def main():
    if not JS_PATH.exists():
        raise FileNotFoundError(f"Ne postoji: {JS_PATH}")

    backup_file(JS_PATH, JS_BACKUP)
    if HTML_PATH.exists():
        backup_file(HTML_PATH, HTML_BACKUP)

    js = JS_PATH.read_text(encoding="utf-8")

    changed = False

    # 1) Dodaj zoom kotačićem miša.
    if "avatarWheelZoomV2" not in js:
        wheel_block = """
    /* avatarWheelZoomV2 */
    if (modalEl && zoomRange) {
        const avatarWheelZoomTarget = modalEl.querySelector(".avatar-crop-frame") || modalEl.querySelector(".avatar-crop-stage") || modalEl;

        avatarWheelZoomTarget.addEventListener("wheel", function (event) {
            if (!cropper || !zoomRange) {
                return;
            }

            event.preventDefault();

            const currentValue = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 4 : -4;
            const nextValue = Math.max(0, Math.min(100, currentValue + step));

            zoomRange.value = String(nextValue);
            setZoomFromRange(nextValue);
        }, { passive: false });
    }

"""
        target = "if (rotateBtn) {"
        if target in js:
            js = js.replace(target, wheel_block + target, 1)
            changed = True
        else:
            raise RuntimeError("Nisam našao mjesto za ubacivanje zoom kotačića prije rotateBtn bloka.")

    # 2) Dodaj dodatni CSS override unutar postojećeg injectAvatarEditorStyle() bloka.
    if "avatarCompactTextButtonsV2" not in js:
        compact_css = """
    /* avatarCompactTextButtonsV2 */
    #avatarCropModal .modal-title,
    #avatarCropModal h1,
    #avatarCropModal h2,
    #avatarCropModal h3,
    #avatarCropModal h4,
    #avatarCropModal h5 {
        font-size: 18px !important;
        line-height: 1.15 !important;
        margin-bottom: 3px !important;
    }

    #avatarCropModal p,
    #avatarCropModal .text-muted,
    #avatarCropModal .form-text {
        font-size: 12px !important;
        line-height: 1.25 !important;
        margin-bottom: 8px !important;
    }

    #avatarCropModal .btn-close,
    #avatarCropModal [data-bs-dismiss="modal"] {
        width: 18px !important;
        height: 18px !important;
        padding: 2px !important;
        transform: scale(0.7) !important;
    }

    #avatarCropModal label,
    #avatarCropModal .form-label {
        font-size: 13px !important;
        line-height: 1.15 !important;
    }

    #avatarCropModal .btn:not(.btn-close),
    #avatarCropModal button:not(.btn-close) {
        font-size: 12px !important;
        line-height: 1.15 !important;
        padding: 5px 9px !important;
        border-radius: 7px !important;
        min-height: 0 !important;
    }

    #avatarCropModal #avatarApplyBtn {
        font-size: 13px !important;
        line-height: 1.15 !important;
        padding: 6px 12px !important;
        border-radius: 7px !important;
    }

    #avatarCropModal .avatar-crop-controls,
    #avatarCropModal .avatar-editor-controls,
    #avatarCropModal .modal-footer {
        gap: 8px !important;
    }

"""
        style_end = "`; document.head.appendChild(style);"
        if style_end in js:
            js = js.replace(style_end, compact_css + style_end, 1)
            changed = True
        else:
            raise RuntimeError("Nisam našao kraj CSS bloka u injectAvatarEditorStyle().")

    # 3) Profesionalniji tekstovi u HTML-u, ako postoje.
    if HTML_PATH.exists():
        html = HTML_PATH.read_text(encoding="utf-8")
        old_html = html
        html = html.replace("Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.", "Uredite avatar prije spremanja.")
        html = html.replace("Povuci sliku, zumiraj i spremi okrugli izrez.", "Namjestite sliku unutar okvira prije spremanja.")
        if html != old_html:
            HTML_PATH.write_text(html, encoding="utf-8")
            changed = True

    JS_PATH.write_text(js, encoding="utf-8")

    if changed:
        print("Gotovo: dodan je zoom kotačićem miša i smanjeni su tekst/gumbi u avatar editoru.")
        print(f"Backup JS: {JS_BACKUP}")
        if HTML_PATH.exists():
            print(f"Backup HTML: {HTML_BACKUP}")
    else:
        print("Nema promjena: sve je već bilo dodano.")

if __name__ == "__main__":
    main()
