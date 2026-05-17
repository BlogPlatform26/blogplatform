from pathlib import Path
from datetime import datetime
import re

ROOT = Path.cwd()
html_path = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if not html_path.exists():
    raise FileNotFoundError(f"Ne mogu pronaći: {html_path}")
if not js_path.exists():
    raise FileNotFoundError(f"Ne mogu pronaći: {js_path}")

html_backup = html_path.with_suffix(html_path.suffix + f".bak_avatar_smaller_css_only_{stamp}")
js_backup = js_path.with_suffix(js_path.suffix + f".bak_avatar_smaller_css_only_{stamp}")
html_backup.write_text(html_path.read_text(encoding="utf-8"), encoding="utf-8")
js_backup.write_text(js_path.read_text(encoding="utf-8"), encoding="utf-8")

html = html_path.read_text(encoding="utf-8")

# Profesionalniji tekstovi, bez mijenjanja strukture forme.
replacements = {
    "Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.": "Uredi sliku avatara prije spremanja.",
    "Odaberi sliku, pomakni kadar, zumiraj i spremi okrugli izrez.": "Odaberi sliku i namjesti prikaz avatara.",
    "Obrezivanje avatara": "Uređivanje avatara",
    "Povuci sliku, zumiraj i spremi okrugli izrez.": "Namjestite sliku unutar okvira prije spremanja.",
    ">Zum<": ">Uvećanje<",
    ">Reset<": ">Vrati<",
}
for old, new in replacements.items():
    html = html.replace(old, new)

# Makni staru verziju ovog istog CSS bloka ako je već dodana.
html = re.sub(
    r"\n?<!-- AVATAR_SMALLER_CSS_ONLY_FIX_START -->.*?<!-- AVATAR_SMALLER_CSS_ONLY_FIX_END -->\n?",
    "\n",
    html,
    flags=re.DOTALL,
)

css_block = r'''
<!-- AVATAR_SMALLER_CSS_ONLY_FIX_START -->
<style>
/* Samo vizualno smanjivanje avatar editora. Ne mijenja spremanje ni osnovnu cropper logiku. */
#avatarCropModal.avatar-crop-modal .modal-dialog {
    max-width: 720px !important;
    width: calc(100vw - 40px) !important;
    margin: 12px auto !important;
}

#avatarCropModal.avatar-crop-modal .modal-content {
    border-radius: 22px !important;
    max-height: calc(100vh - 24px) !important;
    overflow: hidden !important;
}

#avatarCropModal.avatar-crop-modal .modal-header {
    padding: 18px 22px 10px 22px !important;
}

#avatarCropModal.avatar-crop-modal .modal-title {
    font-size: 25px !important;
    line-height: 1.15 !important;
    margin: 0 !important;
}

#avatarCropModal.avatar-crop-modal .modal-header .small {
    font-size: 14px !important;
    margin-top: 4px !important;
    opacity: 0.75 !important;
}

#avatarCropModal.avatar-crop-modal .btn-close {
    width: 18px !important;
    height: 18px !important;
    padding: 8px !important;
    transform: scale(0.78) !important;
    opacity: 0.85 !important;
}

#avatarCropModal.avatar-crop-modal .modal-body {
    padding: 0 22px 18px 22px !important;
}

#avatarCropModal.avatar-crop-modal .avatar-crop-stage {
    height: min(42vh, 330px) !important;
    min-height: 250px !important;
    padding: 12px !important;
}

#avatarCropModal.avatar-crop-modal .avatar-crop-frame {
    height: 100% !important;
    max-height: 310px !important;
    border-radius: 18px !important;
}

#avatarCropModal.avatar-crop-modal .cropper-container,
#avatarCropModal.avatar-crop-modal .cropper-wrap-box,
#avatarCropModal.avatar-crop-modal .cropper-canvas,
#avatarCropModal.avatar-crop-modal .cropper-drag-box {
    max-height: 100% !important;
}

#avatarCropModal.avatar-crop-modal .avatar-crop-controls {
    margin-top: 12px !important;
}

#avatarCropModal.avatar-crop-modal .avatar-crop-control-row {
    display: grid !important;
    grid-template-columns: 105px 1fr !important;
    gap: 12px !important;
    align-items: center !important;
}

#avatarCropModal.avatar-crop-modal .form-label {
    font-size: 16px !important;
    margin-bottom: 0 !important;
}

#avatarCropModal.avatar-crop-modal .form-range {
    height: 6px !important;
}

#avatarCropModal.avatar-crop-modal .d-flex.flex-wrap.gap-2.justify-content-between.align-items-center.mt-3 {
    margin-top: 12px !important;
}

#avatarCropModal.avatar-crop-modal .btn {
    font-size: 15px !important;
    padding: 7px 13px !important;
    border-radius: 8px !important;
}

#avatarCropModal.avatar-crop-modal #avatarApplyBtn {
    font-size: 17px !important;
    padding: 9px 22px !important;
}

@media (max-height: 760px) {
    #avatarCropModal.avatar-crop-modal .modal-dialog {
        margin: 8px auto !important;
    }

    #avatarCropModal.avatar-crop-modal .modal-header {
        padding: 14px 20px 8px 20px !important;
    }

    #avatarCropModal.avatar-crop-modal .modal-title {
        font-size: 22px !important;
    }

    #avatarCropModal.avatar-crop-modal .modal-header .small {
        font-size: 13px !important;
    }

    #avatarCropModal.avatar-crop-modal .modal-body {
        padding: 0 20px 14px 20px !important;
    }

    #avatarCropModal.avatar-crop-modal .avatar-crop-stage {
        height: min(38vh, 285px) !important;
        min-height: 220px !important;
    }

    #avatarCropModal.avatar-crop-modal .btn {
        font-size: 14px !important;
        padding: 6px 11px !important;
    }

    #avatarCropModal.avatar-crop-modal #avatarApplyBtn {
        font-size: 16px !important;
        padding: 8px 18px !important;
    }
}
</style>
<!-- AVATAR_SMALLER_CSS_ONLY_FIX_END -->
'''

html = html.rstrip() + "\n" + css_block + "\n"
html_path.write_text(html, encoding="utf-8")

js = js_path.read_text(encoding="utf-8")

# Smanji fiksni krug malo, da se više ne reže na dnu. Ne mijenja se ostatak logike.
js = js.replace(
    "const diameter = Math.max(140, Math.min(canvasData.width, canvasData.height) * 0.78);",
    "const diameter = Math.max(120, Math.min(canvasData.width, canvasData.height) * 0.70);",
)
js = js.replace(
    "const diameter = Math.max(140, Math.min(canvasData.width, canvasData.height) * 0.68);",
    "const diameter = Math.max(120, Math.min(canvasData.width, canvasData.height) * 0.70);",
)
js = js.replace(
    "autoCropArea: 0.8,",
    "autoCropArea: 0.72,",
)

js_path.write_text(js, encoding="utf-8")

print("Gotovo: avatar editor je samo vizualno smanjen.")
print(f"Backup HTML: {html_backup}")
print(f"Backup JS: {js_backup}")
