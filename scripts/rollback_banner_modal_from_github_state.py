from pathlib import Path
import shutil

ROOT = Path.cwd()
SCRIPTS = ROOT / "scripts"
backups = sorted(SCRIPTS.glob("_banner_modal_fix_backup_*"), key=lambda p: p.name)
if not backups:
    raise SystemExit("Nema backup foldera za rollback.")
backup = backups[-1]

mapping = {
    "_settings_tab.html": ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html",
    "blog_settings_banner.js": ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js",
}

for name, dest in mapping.items():
    src = backup / name
    if src.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print("Vraćeno:", dest)

print("Rollback gotov iz:", backup)
