from pathlib import Path

BASE = Path.cwd()
BACKUP_DIR = BASE / "scripts" / "_banner_modal_body_fix_backup"
JS_PATH = BASE / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
TPL_PATH = BASE / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"

if not BACKUP_DIR.exists():
    raise SystemExit("Nema backup foldera: scripts/_banner_modal_body_fix_backup")

def restore_latest(path: Path):
    backups = sorted(BACKUP_DIR.glob(f"{path.name}.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
    if backups:
        path.write_bytes(backups[0].read_bytes())
        print(f"Vraćeno: {path}")
    else:
        print(f"Nema backupa za: {path}")

restore_latest(JS_PATH)
restore_latest(TPL_PATH)
