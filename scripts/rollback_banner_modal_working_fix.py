from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "scripts" / "_banner_modal_working_backup"

if not BACKUP_DIR.exists():
    print("Nema backup foldera za ovaj fix.")
    raise SystemExit(0)

for backup in BACKUP_DIR.glob("*.bak"):
    original = ROOT / backup.name[:-4].replace("__", "/")
    original.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup, original)
    print(f"Vraćeno: {original}")

print("Rollback gotov. Pokreni: python manage.py check")
