from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

if not HTML_PATH.exists():
    raise SystemExit(f"Ne mogu pronaći file: {HTML_PATH}")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = HTML_PATH.with_suffix(HTML_PATH.suffix + f".bak_avatar_button_text_repair_{stamp}")
shutil.copy2(HTML_PATH, backup)

html = HTML_PATH.read_text(encoding="utf-8")
original = html

# Makni stare CSS blokove koje su prethodni pokušaji možda dodali više puta.
old_markers = [
    "Avatar buttons compact fix",
    "Avatar compact UI - safe CSS",
    "Avatar editor - kompaktniji izgled",
    "Avatar smaller CSS only fix",
    "Avatar tight UI safe fix",
    "Avatar clean UI fix",
]
for marker in old_markers:
    html = re.sub(r"\n?<style>\s*/\*\s*" + re.escape(marker) + r"[\s\S]*?</style>", "", html, flags=re.IGNORECASE)

# Popravi gumbe po ID-ju. Ovo uklanja slučajno ubačen CSS koji se sada vidi kao tekst u gumbu.
def replace_button_by_id(text, button_id, replacement):
    pattern1 = r'<button\b(?=[^>]*\bid=["\']' + re.escape(button_id) + r'["\'])(?:[^>]|\n)*>[\s\S]*?</button>'
    text, count1 = re.subn(pattern1, replacement, text, flags=re.IGNORECASE)

    # Drugi slučaj: ako je id završio kasnije u pokvarenom tagu, hvataj po najbližem buttonu oko ID-ja.
    if count1 == 0 and button_id in text:
        idx = text.find(button_id)
        start = text.rfind("<button", 0, idx)
        end = text.find("</button>", idx)
        if start != -1 and end != -1:
            text = text[:start] + replacement + text[end + len("</button>"):]
    return text

rotate_button = '<button type="button" class="btn btn-outline-secondary avatar-crop-btn" id="avatarRotateBtn">Zakreni</button>'
reset_button = '<button type="button" class="btn btn-outline-secondary avatar-crop-btn" id="avatarResetBtn">Vrati</button>'
apply_button = '<button type="button" class="btn btn-primary avatar-crop-apply" id="avatarApplyBtn">Primijeni avatar</button>'

html = replace_button_by_id(html, "avatarRotateBtn", rotate_button)
html = replace_button_by_id(html, "avatarResetBtn", reset_button)
html = replace_button_by_id(html, "avatarApplyBtn", apply_button)

# Ako je CSS tekst ostao van gumba, makni samo taj specifični pokvareni tekst.
broken_css_fragments = [
    r"padding:\s*5px\s+10px\s*!important;\s*font-size:\s*13px\s*!important;\s*line-height:\s*1\.2\s*!important;\s*border-radius:\s*7px\s*!important;\s*min-height:\s*0\s*!important;?\s*style=\"?",
    r"padding:\s*5px\s+10px\s*!important;\s*font-size:\s*13px\s*!important;\s*line-height:\s*1\.2\s*!important;\s*border-radius:\s*7px\s*!important;?\s*\"?>?",
]
for pattern in broken_css_fragments:
    html = re.sub(pattern, "", html, flags=re.IGNORECASE)

# Normalniji tekstovi, bez neprofesionalnog spominjanja Gmaila.
html = html.replace(
    "Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.",
    "Uredite sliku avatara prije spremanja."
)
html = html.replace(
    "Povuci sliku, zumiraj i spremi okrugli izrez.",
    "Namjestite sliku unutar okvira prije spremanja."
)
html = html.replace("Zum", "Uvećanje")
html = html.replace("Reset", "Vrati")

# Dodaj mali, dobro formiran CSS samo za gumbe i razmake. Ne dira cropper logiku.
css_marker = "Avatar button text repair"
css = """
<style>
/* Avatar button text repair */
#avatarCropModal .avatar-crop-btn,
#avatarCropModal #avatarRotateBtn,
#avatarCropModal #avatarResetBtn {
    padding: 6px 12px !important;
    font-size: 14px !important;
    line-height: 1.2 !important;
    min-height: 0 !important;
    min-width: 0 !important;
    width: auto !important;
    height: auto !important;
    border-radius: 8px !important;
    white-space: nowrap !important;
}

#avatarCropModal .avatar-crop-apply,
#avatarCropModal #avatarApplyBtn {
    padding: 8px 18px !important;
    font-size: 16px !important;
    line-height: 1.2 !important;
    min-height: 0 !important;
    min-width: 0 !important;
    width: auto !important;
    height: auto !important;
    border-radius: 9px !important;
    white-space: nowrap !important;
}

#avatarCropModal .avatar-crop-actions,
#avatarCropModal .avatar-editor-actions,
#avatarCropModal .avatar-actions,
#avatarCropModal .modal-footer {
    gap: 10px !important;
    padding-top: 10px !important;
    padding-bottom: 8px !important;
}

#avatarCropModal .avatar-crop-controls,
#avatarCropModal .avatar-editor-controls,
#avatarCropModal .avatar-controls {
    margin-top: 12px !important;
    gap: 10px !important;
}

#avatarCropModal input[type="range"] {
    height: 6px !important;
}

#avatarCropModal .btn-close {
    transform: scale(0.78) !important;
    opacity: 0.85 !important;
}
</style>
"""

if css_marker not in html:
    # Ubaci prije kraja filea. Ako ima formu, CSS na dnu templatea je OK i neće utjecati na druge stranice.
    html = html.rstrip() + "\n" + css + "\n"

HTML_PATH.write_text(html, encoding="utf-8")

print("Gotovo: popravljeni su avatar gumbi i maknut je CSS tekst iz gumba.")
print(f"Backup: {backup}")
print("Sada pokreni: python manage.py check")
