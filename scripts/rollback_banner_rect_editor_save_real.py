from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "scripts" else Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
BACKUP_DIR = ROOT / "scripts" / "_banner_rect_editor_save_real_backup"

html_backup = BACKUP_DIR / "_settings_tab.html"
js_backup = BACKUP_DIR / "blog_settings_banner.js"

if html_backup.exists():
    shutil.copy2(html_backup, HTML_PATH)
    print(f"Vraćen: {HTML_PATH}")
else:
    print("Nema HTML backupa.")

if js_backup.exists():
    shutil.copy2(js_backup, JS_PATH)
    print(f"Vraćen: {JS_PATH}")
elif JS_PATH.exists():
    JS_PATH.unlink()
    print(f"Obrisan novi JS: {JS_PATH}")
else:
    print("Nema JS backupa i nema JS filea za brisanje.")
