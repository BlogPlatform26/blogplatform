from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path.cwd()
BACKUP_DIR = ROOT / "scripts" / "_banner_rect_editor_backup"
FILES_TO_RESTORE = [
    ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html",
    ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js",
]


def main() -> None:
    if not BACKUP_DIR.exists():
        raise RuntimeError("Nema backup foldera: scripts/_banner_rect_editor_backup")

    restored = 0
    for target in FILES_TO_RESTORE:
        backup = BACKUP_DIR / target.relative_to(ROOT)
        if backup.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, target)
            restored += 1
        elif target.name == "blog_settings_banner.js" and target.exists():
            target.unlink()
            restored += 1

    print(f"Rollback gotov. Vraćeno/uklonjeno datoteka: {restored}")


if __name__ == "__main__":
    main()
