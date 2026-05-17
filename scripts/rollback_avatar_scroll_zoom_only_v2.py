from pathlib import Path
import shutil

JS_PATH = Path('blog/static/blog/js/blog_settings_avatar.js')
BACKUP_PATH = Path('blog/static/blog/js/blog_settings_avatar.js.bak_scroll_zoom_only_v2')

if not BACKUP_PATH.exists():
    raise SystemExit('Nema backup datoteke za rollback.')

shutil.copy2(BACKUP_PATH, JS_PATH)
print('Vratio sam blog_settings_avatar.js iz backup kopije.')
