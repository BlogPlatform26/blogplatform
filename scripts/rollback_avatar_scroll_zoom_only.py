from pathlib import Path

js_path = Path('blog/static/blog/js/blog_settings_avatar.js')
backup_path = Path('blog/static/blog/js/blog_settings_avatar.js.bak_avatar_scroll_zoom_only')

if not backup_path.exists():
    raise SystemExit('Nema backup datoteke za rollback.')

js_path.write_text(backup_path.read_text(encoding='utf-8'), encoding='utf-8')
print('Vraćeno je stanje prije scroll zoom fixa.')
