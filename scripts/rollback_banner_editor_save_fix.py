
from pathlib import Path
import shutil

BACKUP_ROOT = Path('scripts') / '_banner_editor_save_fix_backup'
if not BACKUP_ROOT.exists():
    raise SystemExit('Nema backup foldera za banner editor save fix.')
backups = sorted([p for p in BACKUP_ROOT.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
if not backups:
    raise SystemExit('Nema backupa za vratiti.')
backup = backups[0]
for src in backup.rglob('*'):
    if src.is_file():
        rel = src.relative_to(backup)
        dest = Path(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
print('Vraćeno iz backup foldera:', backup)
