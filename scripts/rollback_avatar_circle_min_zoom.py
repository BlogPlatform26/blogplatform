from pathlib import Path

JS_PATH = Path("blog/static/blog/js/blog_settings_avatar.js")
BACKUP_PATH = Path("blog/static/blog/js/blog_settings_avatar.js.bak_before_avatar_circle_min_zoom")

if not BACKUP_PATH.exists():
    raise FileNotFoundError(f"Nema backupa: {BACKUP_PATH}")

JS_PATH.write_text(BACKUP_PATH.read_text(encoding="utf-8"), encoding="utf-8")
print("Vraćeno iz backupa.")
