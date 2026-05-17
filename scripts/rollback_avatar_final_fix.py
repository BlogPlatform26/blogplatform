from pathlib import Path
import shutil

ROOT = Path.cwd()
BACKUP_DIR = ROOT / "scripts" / "_avatar_final_backup"
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if not BACKUP_DIR.exists():
    raise SystemExit("Nema backup foldera: scripts/_avatar_final_backup")

html_backups = sorted(BACKUP_DIR.glob("_settings_tab.html.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
js_backups = sorted(BACKUP_DIR.glob("blog_settings_avatar.js.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)

if not html_backups or not js_backups:
    raise SystemExit("Nema backup datoteka za vraćanje.")

shutil.copy2(html_backups[0], HTML_PATH)
shutil.copy2(js_backups[0], JS_PATH)
print(f"Vraćeno: {html_backups[0]}")
print(f"Vraćeno: {js_backups[0]}")
