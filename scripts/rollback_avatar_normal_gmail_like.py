from pathlib import Path
import shutil

ROOT = Path.cwd()
BACKUP = ROOT / "backups" / "avatar_normal_gmail_like_20260517_082107"

html_backup = BACKUP / "_settings_tab.html"
js_backup = BACKUP / "blog_settings_avatar.js"
html_target = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
js_target = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

if html_backup.exists():
    shutil.copy2(html_backup, html_target)
if js_backup.exists():
    shutil.copy2(js_backup, js_target)

print("Vraćeno stanje prije avatar_normal_gmail_like fixa.")
