from pathlib import Path
import shutil

ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
rollback_info = ROOT / "scripts" / ".avatar_zoom_wheel_small_text_last_backup.txt"

if not rollback_info.exists():
    raise SystemExit("Nema zapisa o backupu za rollback.")
backup_dir = Path(rollback_info.read_text(encoding="utf-8").strip())

html_backup = backup_dir / "_settings_tab.html"
js_backup = backup_dir / "blog_settings_avatar.js"
if not html_backup.exists() or not js_backup.exists():
    raise SystemExit(f"Backup nije potpun: {backup_dir}")

shutil.copy2(html_backup, HTML_PATH)
shutil.copy2(js_backup, JS_PATH)
print("Rollback gotov: vraćeni su avatar HTML i JS iz zadnjeg backupa.")
