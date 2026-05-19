from pathlib import Path
import shutil

ROOT = Path.cwd()
backup_dir = ROOT / "scripts" / "_banner_modal_clean_backups"

if not backup_dir.exists():
    print("Nema backup foldera.")
    raise SystemExit(0)

targets = {
    "_settings_tab.html": ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html",
    "blog_settings_banner.js": ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js",
}

for name, target in targets.items():
    backups = sorted(backup_dir.glob(f"{name}.*.bak"))
    if backups:
        shutil.copy2(backups[-1], target)
        print(f"Vraćeno: {target}")
    else:
        print(f"Nema backupa za: {name}")
