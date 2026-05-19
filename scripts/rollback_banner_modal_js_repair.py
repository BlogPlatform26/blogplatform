from pathlib import Path
import shutil

ROOT = Path.cwd()
backup_dir = ROOT / "scripts" / "_banner_modal_js_repair_backup"
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
css_path = ROOT / "blog" / "static" / "css" / "style.css"

def latest(pattern):
    files = sorted(backup_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

js_backup = latest("blog_settings_banner.js.*.bak")
css_backup = latest("style.css.*.bak")

if js_backup:
    shutil.copyfile(js_backup, js_path)
if css_backup:
    shutil.copyfile(css_backup, css_path)

print("Rollback gotov.")
