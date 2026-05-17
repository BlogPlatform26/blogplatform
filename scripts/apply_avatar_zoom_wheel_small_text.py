from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

if not HTML_PATH.exists():
    raise SystemExit(f"Ne postoji file: {HTML_PATH}")
if not JS_PATH.exists():
    raise SystemExit(f"Ne postoji file: {JS_PATH}")

backup_dir = ROOT / "scripts" / "backups" / f"avatar_zoom_wheel_small_text_{STAMP}"
backup_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(HTML_PATH, backup_dir / "_settings_tab.html")
shutil.copy2(JS_PATH, backup_dir / "blog_settings_avatar.js")

# Spremi putanju za rollback.
rollback_info = ROOT / "scripts" / ".avatar_zoom_wheel_small_text_last_backup.txt"
rollback_info.write_text(str(backup_dir), encoding="utf-8")

html = HTML_PATH.read_text(encoding="utf-8")
html = html.replace("Uredite avatar prije spremanja.", "Uredite avatar prije spremanja.")
html = html.replace("Namjestite sliku unutar okvira prije spremanja.", "Namjestite sliku prije spremanja.")
HTML_PATH.write_text(html, encoding="utf-8")

js = JS_PATH.read_text(encoding="utf-8")

# Samo smanjujemo vizualni dio u postojećem CSS-u koji JS ubacuje.
replacements = {
    "max-width: 760px !important;": "max-width: 720px !important;",
    "padding: 18px 22px !important;": "padding: 14px 18px !important;",
    "border-radius: 20px !important;": "border-radius: 18px !important;",
    "font-size: 22px !important;": "font-size: 18px !important;",
    "font-size: 20px !important;": "font-size: 17px !important;",
    "font-size: 13px !important;": "font-size: 12px !important;",
    "font-size: 14px !important;": "font-size: 12px !important;",
    "padding: 6px 11px !important;": "padding: 4px 8px !important;",
    "padding: 8px 16px !important;": "padding: 6px 12px !important;",
    "border-radius: 8px !important;": "border-radius: 7px !important;",
    "width: 22px !important; height: 22px !important;": "width: 18px !important; height: 18px !important;",
    "transform: scale(0.8) !important;": "transform: scale(0.7) !important;",
}
for old, new in replacements.items():
    js = js.replace(old, new)

# Dodaj zoom na kotačić miša samo jednom.
wheel_marker = "avatar wheel zoom fix"
if wheel_marker not in js:
    old_block = 'if (zoomRange) { zoomRange.setAttribute("min", "0"); zoomRange.setAttribute("max", "100"); zoomRange.setAttribute("value", "0"); zoomRange.addEventListener("input", function () { setZoomFromRange(this.value); }); }'
    new_block = old_block + ' if (modalEl) { /* avatar wheel zoom fix */ modalEl.addEventListener("wheel", function (event) { if (!cropper) return; const insideEditor = event.target.closest(".avatar-crop-stage, .avatar-crop-frame, .cropper-container"); if (!insideEditor) return; event.preventDefault(); const currentValue = zoomRange ? Number(zoomRange.value || 0) : 0; const step = event.deltaY < 0 ? 5 : -5; const nextValue = Math.max(0, Math.min(100, currentValue + step)); if (zoomRange) zoomRange.value = String(nextValue); setZoomFromRange(nextValue); }, { passive: false }); }'
    if old_block not in js:
        raise SystemExit("Nisam našao očekivani zoomRange blok u blog_settings_avatar.js. Ništa nije promijenjeno.")
    js = js.replace(old_block, new_block, 1)

JS_PATH.write_text(js, encoding="utf-8")
print("Gotovo: dodan je zoom kotačićem miša i smanjeni su tekst/gumbi u avatar editoru.")
print(f"Backup: {backup_dir}")
