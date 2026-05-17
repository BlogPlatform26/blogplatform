from pathlib import Path
import re
from datetime import datetime

HTML_PATH = Path("blog/templates/blog/settings/_settings_tab.html")

if not HTML_PATH.exists():
    raise SystemExit("Ne mogu pronaći blog/templates/blog/settings/_settings_tab.html")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = HTML_PATH.with_name(HTML_PATH.name + f".bak_avatar_modal_compact_{stamp}")
backup_path.write_text(HTML_PATH.read_text(encoding="utf-8"), encoding="utf-8")

html = HTML_PATH.read_text(encoding="utf-8")

# Profesionalniji tekstovi bez diranja JS/cropper logike.
replacements = {
    "Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.": "Uredite avatar prije spremanja.",
    "Odaberi sliku, pomakni kadar, zumiraj i spremi okrugli izrez.": "Odaberite sliku i namjestite prikaz avatara.",
    "Povuci sliku, zumiraj i spremi okrugli izrez.": "Namjestite sliku unutar okvira prije spremanja.",
    "Obrezivanje avatara": "Uređivanje avatara",
    "Zum": "Uvećanje",
    "Reset": "Vrati",
}

for old, new in replacements.items():
    html = html.replace(old, new)

style_id = "avatar-modal-compact-text-buttons-final"

# Makni staru verziju ovog istog CSS bloka ako postoji.
html = re.sub(
    rf"\n?<style id=[\"']{re.escape(style_id)}[\"']>.*?</style>\s*",
    "\n",
    html,
    flags=re.DOTALL | re.IGNORECASE,
)

style_block = """
<style id="avatar-modal-compact-text-buttons-final">
/* Avatar modal - finalno smanjenje samo teksta, gumba i razmaka.
   Ne dira CropperJS logiku, crop okvir, spremanje, modele ni bazu. */
#avatarCropModal .modal-dialog {
    max-width: 760px !important;
}

#avatarCropModal .modal-content,
#avatarCropModal .avatar-crop-modal {
    padding: 20px 26px !important;
    border-radius: 22px !important;
}

#avatarCropModal .modal-header,
#avatarCropModal .avatar-crop-header {
    padding: 0 0 8px 0 !important;
    margin: 0 !important;
}

#avatarCropModal .modal-title,
#avatarCropModal h1,
#avatarCropModal h2,
#avatarCropModal .avatar-crop-title {
    font-size: 22px !important;
    line-height: 1.2 !important;
    margin: 0 0 4px 0 !important;
    font-weight: 700 !important;
}

#avatarCropModal p,
#avatarCropModal .text-muted,
#avatarCropModal .avatar-crop-help,
#avatarCropModal .avatar-crop-subtitle {
    font-size: 13px !important;
    line-height: 1.35 !important;
    margin: 0 0 10px 0 !important;
}

#avatarCropModal .btn-close,
#avatarCropModal .avatar-crop-close,
#avatarCropModal [data-bs-dismiss="modal"] {
    width: 24px !important;
    height: 24px !important;
    padding: 0 !important;
    font-size: 20px !important;
    line-height: 1 !important;
    opacity: .85 !important;
}

#avatarCropModal .modal-body,
#avatarCropModal .avatar-crop-body {
    padding: 8px 0 0 0 !important;
}

#avatarCropModal .avatar-crop-stage,
#avatarCropModal .cropper-container-wrapper {
    margin-top: 8px !important;
    margin-bottom: 12px !important;
}

#avatarCropModal label,
#avatarCropModal .form-label,
#avatarCropModal .avatar-zoom-label {
    font-size: 15px !important;
    line-height: 1.2 !important;
    margin-bottom: 4px !important;
    font-weight: 600 !important;
}

#avatarCropModal input[type="range"],
#avatarZoomRange {
    height: 5px !important;
}

#avatarCropModal .avatar-crop-controls,
#avatarCropModal .avatar-actions,
#avatarCropModal .modal-footer {
    padding-top: 8px !important;
    padding-bottom: 0 !important;
    margin-top: 8px !important;
    gap: 10px !important;
}

#avatarCropModal .btn,
#avatarCropModal button {
    font-size: 14px !important;
    line-height: 1.2 !important;
    padding: 7px 13px !important;
    min-height: 0 !important;
    border-radius: 8px !important;
}

#avatarRotateBtn,
#avatarResetBtn {
    font-size: 14px !important;
    padding: 7px 13px !important;
    min-width: 0 !important;
}

#avatarApplyBtn {
    font-size: 16px !important;
    line-height: 1.2 !important;
    padding: 9px 18px !important;
    min-width: 165px !important;
    min-height: 0 !important;
}

#avatarForm button[type="submit"].btn-primary,
#avatarForm input[type="submit"].btn-primary {
    font-size: 15px !important;
    padding: 8px 14px !important;
    border-radius: 8px !important;
}

@media (max-height: 760px) {
    #avatarCropModal .modal-dialog {
        max-width: 700px !important;
    }

    #avatarCropModal .modal-content,
    #avatarCropModal .avatar-crop-modal {
        padding: 16px 22px !important;
    }

    #avatarCropModal .modal-title,
    #avatarCropModal h1,
    #avatarCropModal h2,
    #avatarCropModal .avatar-crop-title {
        font-size: 20px !important;
    }

    #avatarApplyBtn {
        font-size: 15px !important;
        padding: 8px 16px !important;
    }
}
</style>
"""

html = html.rstrip() + "\n" + style_block + "\n"
HTML_PATH.write_text(html, encoding="utf-8")

print("Gotovo: smanjen je tekst, X, gumbi i razmaci u avatar modalu.")
print(f"Backup: {backup_path}")
print("Sada pokreni: python manage.py check")
