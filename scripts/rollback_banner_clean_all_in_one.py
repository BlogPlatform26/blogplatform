from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
BACKUPS_ROOT = ROOT / "scripts"
candidates = sorted(BACKUPS_ROOT.glob("_banner_clean_backup_*"), reverse=True)

if not candidates:
    print("Nema backup foldera za banner clean fix.")
    sys.exit(1)

backup_dir = candidates[0]

for src in backup_dir.rglob("*"):
    if src.is_file():
        rel = src.relative_to(backup_dir)
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

print(f"Vraćeno iz backupa: {backup_dir}")
print("Pokreni: python manage.py check")
