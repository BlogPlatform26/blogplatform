from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if not js_path.exists():
    raise SystemExit(f"Ne mogu pronaći file: {js_path}")

text = js_path.read_text(encoding="utf-8")
backup_path = js_path.with_suffix(js_path.suffix + ".bak_before_avatar_smaller_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup_path.write_text(text, encoding="utf-8")

replacements = {
    "max-width: 640px;": "max-width: 560px;",
    "width: calc(100% - 24px);": "width: calc(100% - 20px);",
    "margin: 1.25rem auto;": "margin: 0.5rem auto;",
    "padding: 18px;": "padding: 12px;",
    "max-width: 520px;": "max-width: 430px;",
    "height: 420px;": "height: 300px;",
    "margin: 0 auto 18px auto;": "margin: 0 auto 10px auto;",
    "height: 340px;": "height: 260px;",
    "if (!cropper) return 280;": "if (!cropper) return 220;",
    "const maxWidth = Math.max(180, containerData.width - 64);": "const maxWidth = Math.max(160, containerData.width - 70);",
    "const maxHeight = Math.max(180, containerData.height - 64);": "const maxHeight = Math.max(160, containerData.height - 70);",
    "return Math.round(Math.min(320, maxWidth, maxHeight));": "return Math.round(Math.min(240, maxWidth, maxHeight));",
}

changed = False
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
        changed = True

# Dodaj sigurnosno ograničenje visine modala ako već nije dodano.
if "max-height: calc(100vh - 24px);" not in text and "#avatarCropModal .modal-content" in text:
    text = text.replace(
        "#avatarCropModal .modal-content {\n                border-radius: 22px;\n                overflow: hidden;\n            }",
        "#avatarCropModal .modal-content {\n                border-radius: 22px;\n                overflow: hidden;\n                max-height: calc(100vh - 24px);\n            }"
    )
    changed = True

if not changed:
    raise SystemExit("Nisam pronašao očekivane vrijednosti u blog_settings_avatar.js. Pošalji mi sadržaj tog JS filea ili vrati zadnji fix pa pokreni ponovno.")

js_path.write_text(text, encoding="utf-8")
print("OK: Avatar editor je smanjen da bolje stane na ekran.")
print(f"Backup starog JS-a: {backup_path}")
print("Sada pokreni: python manage.py check")
