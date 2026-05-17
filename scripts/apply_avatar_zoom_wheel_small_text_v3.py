from pathlib import Path
from datetime import datetime

JS_PATH = Path('blog/static/blog/js/blog_settings_avatar.js')
BACKUP_PATH = Path('blog/static/blog/js/blog_settings_avatar.js.bak_before_zoom_wheel_small_text_v3')

if not JS_PATH.exists():
    raise SystemExit(f'Ne postoji: {JS_PATH}')

js = JS_PATH.read_text(encoding='utf-8')

if not BACKUP_PATH.exists():
    BACKUP_PATH.write_text(js, encoding='utf-8')

original = js

# 1) Uključi zoom kotačićem miša u postojećem Cropperu.
js = js.replace('zoomOnWheel: false', 'zoomOnWheel: true')
if 'wheelZoomRatio:' not in js:
    js = js.replace('zoomOnWheel: true, ready()', 'zoomOnWheel: true, wheelZoomRatio: 0.06, ready()')

# 2) Smanji samo UI tekst, X, gumbe i razmake u već postojećem injectAvatarEditorStyle CSS-u.
replacements = {
    'padding: 18px 22px !important;': 'padding: 12px 18px !important;',
    'font-size: 22px !important;': 'font-size: 18px !important;',
    'width: 22px !important; height: 22px !important; padding: 4px !important; transform: scale(0.8) !important;': 'width: 18px !important; height: 18px !important; padding: 2px !important; transform: scale(0.7) !important;',
    'font-size: 13px !important; line-height: 1.3 !important; margin: 0 0 10px 0 !important;': 'font-size: 12px !important; line-height: 1.25 !important; margin: 0 0 6px 0 !important;',
    'font-size: 14px !important; line-height: 1.2 !important; margin: 0 !important; white-space: nowrap !important;': 'font-size: 12px !important; line-height: 1.2 !important; margin: 0 !important; white-space: nowrap !important;',
    'font-size: 13px !important; line-height: 1.2 !important; padding: 6px 11px !important; border-radius: 8px !important; min-height: 0 !important; min-width: 0 !important;': 'font-size: 11px !important; line-height: 1.15 !important; padding: 4px 8px !important; border-radius: 6px !important; min-height: 0 !important; min-width: 0 !important;',
    'font-size: 14px !important; line-height: 1.2 !important; padding: 8px 16px !important; border-radius: 8px !important;': 'font-size: 12px !important; line-height: 1.15 !important; padding: 6px 12px !important; border-radius: 6px !important;',
    'gap: 10px !important;': 'gap: 7px !important;',
    'margin: 10px auto 12px auto !important;': 'margin: 8px auto 9px auto !important;',
}

changed_items = []
for old, new in replacements.items():
    if old in js:
        js = js.replace(old, new)
        changed_items.append(old[:45])

# 3) Za svaki slučaj, ako je ostao stari tekst gumba iz prošlih pokušaja, vrati normalne nazive.
js = js.replace('if (rotateBtn) rotateBtn.textContent = "Zakreni";', 'if (rotateBtn) rotateBtn.textContent = "Zakreni";')
js = js.replace('if (resetBtn) resetBtn.textContent = "Vrati";', 'if (resetBtn) resetBtn.textContent = "Vrati";')
js = js.replace('if (applyBtn) applyBtn.textContent = "Primijeni avatar";', 'if (applyBtn) applyBtn.textContent = "Primijeni avatar";')

JS_PATH.write_text(js, encoding='utf-8')

if js == original:
    print('Nema promjene. Datoteka je već možda uređena ili ima drugačiji format.')
else:
    print('Gotovo: uključen zoom kotačićem miša i smanjeni tekst/gumbi avatara.')
    print(f'Backup: {BACKUP_PATH}')
