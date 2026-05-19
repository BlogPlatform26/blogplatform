from pathlib import Path
BASE = Path.cwd()
backup_dir = BASE / "scripts" / "_banner_final_modal_backups"
js_bak = backup_dir / "blog_settings_banner.js.bak"
tpl_bak = backup_dir / "_settings_tab.html.bak"
js_path = BASE / "blog" / "static" / "blog" / "js" / "blog_settings_banner.js"
tpl_path = BASE / "blog" / "templates" / "blog" / "settings" / "_settings_tab.html"
if js_bak.exists():
    js_path.write_text(js_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
if tpl_bak.exists():
    tpl_path.write_text(tpl_bak.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
print("Rollback za banner modal je napravljen.")
