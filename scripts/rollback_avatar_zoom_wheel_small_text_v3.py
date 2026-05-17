from pathlib import Path
JS_PATH = Path('blog/static/blog/js/blog_settings_avatar.js')
BACKUP_PATH = Path('blog/static/blog/js/blog_settings_avatar.js.bak_before_zoom_wheel_small_text_v3')
if not BACKUP_PATH.exists():
    raise SystemExit(f'Nema backup datoteke: {BACKUP_PATH}')
JS_PATH.write_text(BACKUP_PATH.read_text(encoding='utf-8'), encoding='utf-8')
print('Vraćeno iz backupa za avatar zoom/text v3.')
