from pathlib import Path
import shutil

path = Path('blog/static/blog/js/blog_settings_avatar.js')
backup = path.with_suffix(path.suffix + '.bak_before_scroll_zoom_real')
if not backup.exists():
    raise SystemExit('Nema backup datoteke za rollback.')
shutil.copy2(backup, path)
print('OK: vraćen je backup avatar JS-a.')
