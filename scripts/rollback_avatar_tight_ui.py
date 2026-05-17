from pathlib import Path

ROOT = Path.cwd()
pairs = [
    (ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html", "bak_avatar_tight_ui_"),
    (ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js", "bak_avatar_tight_ui_"),
]

for target, marker in pairs:
    backups = sorted(target.parent.glob(target.name + "." + marker + "*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not backups:
        print(f"Nema backupa za: {target}")
        continue
    backup = backups[0]
    target.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Vraćeno: {target} iz {backup}")

print("Gotovo. Pokreni: python manage.py check")
