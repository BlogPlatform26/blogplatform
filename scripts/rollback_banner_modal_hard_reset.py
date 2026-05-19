from pathlib import Path

ROOT = Path.cwd()
backup_dir = ROOT / "scripts" / "_banner_modal_hard_reset_backup"
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
css_path = ROOT / "blog" / "static" / "css" / "style.css"

def restore_latest(path: Path):
    files = sorted(backup_dir.glob(f"{path.name}.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
    if files:
        path.write_text(files[0].read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        print("Vraćeno:", path)
    else:
        print("Nema backupa za:", path)

restore_latest(js_path)
restore_latest(css_path)
