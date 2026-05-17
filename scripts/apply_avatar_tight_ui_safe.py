from pathlib import Path
from datetime import datetime
import re
import sys

ROOT = Path.cwd()
html_path = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path: Path):
    if not path.exists():
        print(f"GREŠKA: Ne postoji file: {path}")
        sys.exit(1)
    bak = path.with_name(path.name + f".bak_avatar_tight_ui_{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Backup: {bak}")

backup(html_path)
backup(js_path)

html = html_path.read_text(encoding="utf-8")
js = js_path.read_text(encoding="utf-8")

replacements = {
    "Okrugli izrez kao na Gmailu, s pomicanjem, zumom i rotacijom.": "Uredite avatar prije spremanja.",
    "Odaberi sliku, pomakni kadar, zumiraj i spremi okrugli izrez.": "Odaberite sliku i namjestite okrugli izrez.",
    "Povuci sliku, zumiraj i spremi okrugli izrez.": "Namjestite sliku unutar okvira.",
    "Zum": "Uvećanje",
}
for old, new in replacements.items():
    html = html.replace(old, new)

html = re.sub(
    r"\n?<style>\s*/\*\s*Avatar tight UI - safe CSS\s*\*/.*?</style>\s*",
    "\n",
    html,
    flags=re.DOTALL,
)

style = """
<style>
/* Avatar tight UI - safe CSS */
#avatarCropModal .modal-dialog {
    max-width: 820px !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1.5rem !important;
}

#avatarCropModal .modal-content {
    padding: 18px 22px !important;
    border-radius: 22px !important;
}

#avatarCropModal .modal-header {
    padding: 0 0 8px 0 !important;
    min-height: auto !important;
}

#avatarCropModal .modal-body {
    padding: 6px 0 8px 0 !important;
}

#avatarCropModal .modal-footer {
    padding: 8px 0 0 0 !important;
    margin-top: 0 !important;
}

#avatarCropModal .modal-title,
#avatarCropModal h1,
#avatarCropModal h2,
#avatarCropModal h3 {
    font-size: 24px !important;
    line-height: 1.15 !important;
    margin: 0 0 4px 0 !important;
}

#avatarCropModal p,
#avatarCropModal .text-muted,
#avatarCropModal .small {
    font-size: 14px !important;
    line-height: 1.35 !important;
    margin-bottom: 10px !important;
}

#avatarCropModal .btn-close {
    width: 20px !important;
    height: 20px !important;
    padding: 4px !important;
    transform: scale(0.75);
    opacity: 0.8;
}

#avatarCropModal .btn,
#avatarCropModal button {
    font-size: 15px !important;
    padding: 7px 13px !important;
    border-radius: 8px !important;
}

#avatarApplyBtn {
    font-size: 17px !important;
    padding: 9px 20px !important;
    min-width: 170px !important;
}

#avatarCropModal label,
#avatarCropModal .form-label {
    font-size: 16px !important;
    margin-bottom: 4px !important;
}

#avatarCropModal input[type="range"] {
    height: 6px !important;
}

#avatarCropModal .cropper-container,
#avatarCropModal .cropper-wrap-box,
#avatarCropModal .cropper-canvas,
#avatarCropModal .cropper-crop-box {
    max-height: 430px !important;
}

#avatarCropModal .cropper-view-box {
    outline-width: 2px !important;
}
</style>
"""

if "</form>" in html:
    html = html.replace("</form>", style + "\n</form>", 1)
else:
    html = html + "\n" + style

patterns = [
    (r"Math\.min\(canvasData\.width,\s*canvasData\.height\)\s*\*\s*0\.78", "Math.min(canvasData.width, canvasData.height) * 0.68"),
    (r"Math\.min\(canvasData\.width,\s*canvasData\.height\)\s*\*\s*0\.75", "Math.min(canvasData.width, canvasData.height) * 0.68"),
    (r"Math\.min\(canvasData\.width,\s*canvasData\.height\)\s*\*\s*0\.70", "Math.min(canvasData.width, canvasData.height) * 0.68"),
]
changed_circle = False
for pat, rep in patterns:
    js, n = re.subn(pat, rep, js, count=1)
    if n:
        changed_circle = True
        break
if not changed_circle:
    for old in ["* 0.78", "*0.78", "* 0.75", "*0.75", "* 0.70", "*0.70"]:
        if old in js:
            js = js.replace(old, "* 0.68", 1)
            changed_circle = True
            break

html_path.write_text(html, encoding="utf-8")
js_path.write_text(js, encoding="utf-8")

print("")
print("Gotovo.")
print("- Smanjen je vizualni dio avatar editora.")
print("- Tekstovi su profesionalniji.")
print("- Crop krug je malo smanjen da ne bude odrezan.")
print("- Banner, modeli, baza i migracije nisu dirani.")
print("")
print("Sada pokreni:")
print("python manage.py check")
print("python manage.py runserver")
print("")
print("U browseru napravi Ctrl + F5.")
