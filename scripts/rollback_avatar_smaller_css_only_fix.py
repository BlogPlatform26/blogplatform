from pathlib import Path

ROOT = Path.cwd()
html_path = ROOT / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
js_path = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"

html_backups = sorted(html_path.parent.glob(html_path.name + ".bak_avatar_smaller_css_only_*"), key=lambda p: p.stat().st_mtime, reverse=True)
js_backups = sorted(js_path.parent.glob(js_path.name + ".bak_avatar_smaller_css_only_*"), key=lambda p: p.stat().st_mtime, reverse=True)

if not html_backups or not js_backups:
    raise FileNotFoundError("Nema backup datoteka za ovaj fix.")

html_path.write_text(html_backups[0].read_text(encoding="utf-8"), encoding="utf-8")
js_path.write_text(js_backups[0].read_text(encoding="utf-8"), encoding="utf-8")

print("Vraćeno stanje prije avatar_smaller_css_only fixa.")
print(f"Vraćen HTML backup: {html_backups[0]}")
print(f"Vraćen JS backup: {js_backups[0]}")
