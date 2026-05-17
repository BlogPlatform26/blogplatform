from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "scripts" / "_avatar_quality_backups"
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
SIGNALS_PATH = ROOT / "blog" / "image_signals.py"

backups = [
    (BACKUP_DIR / "blog_settings_avatar.js.bak_before_avatar_high_quality", JS_PATH),
    (BACKUP_DIR / "image_signals.py.bak_before_avatar_high_quality", SIGNALS_PATH),
]

restored_any = False
for backup_path, target_path in backups:
    if backup_path.exists():
        shutil.copy2(backup_path, target_path)
        print(f"Vraćeno: {target_path}")
        restored_any = True
    else:
        print(f"Nema backupa: {backup_path}")

if not restored_any:
    print("Nije ništa vraćeno jer backup nije pronađen.")
else:
    print("Rollback gotov. Pokreni: python manage.py check")
