from pathlib import Path
import shutil

ROOT = Path.cwd()
BACKUPS_ROOT = ROOT / 'scripts' / 'banner_modal_final_repair_backups'

if not BACKUPS_ROOT.exists():
    raise SystemExit('Nema backup foldera za rollback.')

backups = sorted([p for p in BACKUPS_ROOT.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
if not backups:
    raise SystemExit('Nema backup foldera za rollback.')

backup = backups[0]
for src in backup.rglob('*'):
    if src.is_file():
        rel = src.relative_to(backup)
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

print('Vraćeno iz backupa:', backup)
