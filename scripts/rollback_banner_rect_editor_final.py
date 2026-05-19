from pathlib import Path
import shutil

ROOT = Path.cwd()
BACKUP_DIR = ROOT / "scripts" / "_banner_rect_editor_final_backup"
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"

html_backup = BACKUP_DIR / "_settings_tab.html"
js_backup = BACKUP_DIR / "blog_settings_banner.js"

if html_backup.exists():
    shutil.copy2(html_backup, HTML_PATH)
    print("Vraćen je _settings_tab.html")
else:
    print("Nema backup-a za _settings_tab.html")

if js_backup.exists():
    shutil.copy2(js_backup, JS_PATH)
    print("Vraćen je blog_settings_banner.js")
else:
    if JS_PATH.exists():
        JS_PATH.unlink()
        print("Obrisan je blog_settings_banner.js")
    else:
        print("Nema blog_settings_banner.js za vratiti/brisati")
