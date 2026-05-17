from pathlib import Path
import shutil

ROOT = Path.cwd()
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
HTML_PATH = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

JS_BACKUP = JS_PATH.with_suffix(JS_PATH.suffix + ".bak_avatar_zoom_wheel_text_v2")
HTML_BACKUP = HTML_PATH.with_suffix(HTML_PATH.suffix + ".bak_avatar_zoom_wheel_text_v2")

def restore(backup_path, target_path):
    if backup_path.exists():
        shutil.copy2(backup_path, target_path)
        print(f"Vraćeno: {target_path}")
    else:
        print(f"Nema backup datoteke: {backup_path}")

def main():
    restore(JS_BACKUP, JS_PATH)
    if HTML_PATH.exists():
        restore(HTML_BACKUP, HTML_PATH)

if __name__ == "__main__":
    main()
