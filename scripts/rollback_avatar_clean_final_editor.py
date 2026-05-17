from pathlib import Path
ROOT = Path.cwd()
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

def latest_backup(path, marker):
    backups = sorted(path.parent.glob(path.name + marker), key=lambda p: p.stat().st_mtime, reverse=True)
    return backups[0] if backups else None

html_backup = latest_backup(HTML_PATH, ".bak_avatar_clean_final_*")
js_backup = latest_backup(JS_PATH, ".bak_avatar_clean_final_*")
if html_backup:
    HTML_PATH.write_text(html_backup.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Vraćen HTML iz: {html_backup}")
else:
    print("Nema HTML backupa za ovaj fix.")
if js_backup:
    JS_PATH.write_text(js_backup.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Vraćen JS iz: {js_backup}")
else:
    print("Nema JS backupa za ovaj fix.")
