from pathlib import Path

ROOT = Path.cwd()
HTML_PATH = ROOT / 'blog' / 'templates' / 'blog' / 'settings' / '_settings_tab.html'
JS_PATH = ROOT / 'blog' / 'static' / 'blog' / 'js' / 'blog_settings_avatar.js'
BACKUP_DIR = ROOT / 'scripts' / 'avatar_editor_backup_normal'
html_backup = BACKUP_DIR / '_settings_tab.html'
js_backup = BACKUP_DIR / 'blog_settings_avatar.js'

if not html_backup.exists() or not js_backup.exists():
    raise FileNotFoundError('Backup nije pronađen: scripts/avatar_editor_backup_normal')

HTML_PATH.write_text(html_backup.read_text(encoding='utf-8'), encoding='utf-8')
JS_PATH.write_text(js_backup.read_text(encoding='utf-8'), encoding='utf-8')
print('Avatar editor je vraćen iz backupa.')
