from pathlib import Path
import shutil

js_path = Path('blog/static/blog/js/blog_settings_avatar.js')
backup_path = Path('blog/static/blog/js/blog_settings_avatar.js.bak_avatar_quality_only')

if not backup_path.exists():
    raise SystemExit('Backup ne postoji, ne mogu vratiti promjenu.')

shutil.copy2(backup_path, js_path)
print('Vraćeno iz backupa:', backup_path)
