from pathlib import Path
import shutil

folder = Path("blog/templates/blog/settings")
current = folder / "_settings_tab.html"
backups = sorted(folder.glob("_settings_tab.html.bak_avatar_modal_compact_*"), key=lambda p: p.stat().st_mtime, reverse=True)

if not backups:
    raise SystemExit("Nema backup datoteke za avatar modal compact fix.")

shutil.copy2(backups[0], current)
print(f"Vraćeno iz backupa: {backups[0]}")
print("Sada pokreni: python manage.py check")
