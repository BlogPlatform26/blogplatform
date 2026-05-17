from pathlib import Path
import re
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == 'scripts' else Path.cwd()
js_path = ROOT / 'blog' / 'static' / 'blog' / 'js' / 'blog_settings_avatar.js'
signals_path = ROOT / 'blog' / 'image_signals.py'

stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
changed = []

if not js_path.exists():
    raise FileNotFoundError(f'Nema datoteke: {js_path}')

shutil.copy2(js_path, js_path.with_suffix(js_path.suffix + f'.bak_avatar_quality_true_{stamp}'))
js = js_path.read_text(encoding='utf-8-sig')
old_js = js

# Spremi veći finalni avatar. Preview može ostati manji.
js = re.sub(r'getCroppedCanvas\(\s*420\s*\)', 'getCroppedCanvas(1200)', js)
js = re.sub(r'getCroppedCanvas\(\s*900\s*\)', 'getCroppedCanvas(1200)', js)
js = re.sub(r'getCroppedCanvas\(\s*1000\s*\)', 'getCroppedCanvas(1200)', js)

# Drži JPEG radi kompatibilnosti s postojećim backendom, ali s puno većom kvalitetom.
js = re.sub(
    r'toDataURL\(\s*([\"\'])image/jpeg\1\s*,\s*0?\.\d+\s*\)',
    'toDataURL("image/jpeg", 0.98)',
    js,
)
js = re.sub(
    r'toBlob\(\s*([^,]+),\s*([\"\'])image/jpeg\2\s*,\s*0?\.\d+\s*\)',
    r'toBlob(\1, "image/jpeg", 0.98)',
    js,
)

if js != old_js:
    js_path.write_text(js, encoding='utf-8')
    changed.append(str(js_path.relative_to(ROOT)))
else:
    print('U JS-u nisam našao stari 420/JPEG zapis. Preskačem JS promjenu.')

if signals_path.exists():
    shutil.copy2(signals_path, signals_path.with_suffix(signals_path.suffix + f'.bak_avatar_quality_true_{stamp}'))
    text = signals_path.read_text(encoding='utf-8-sig')
    old_text = text

    # Najvažnije: avatar ne smije proći kroz opću optimizaciju quality=82.
    # Radi i ako je kod u više redova, i ako je format malo drugačiji.
    pattern = r'(?m)^(\s*)optimize_image_field\(instance,\s*[\"\']avatar[\"\']\)\s*$'
    replacement = r'\1# Avatar se ne komprimira dodatno; crop editor već sprema avatar u visokoj kvaliteti.\n\1# optimize_image_field(instance, "avatar")'
    text = re.sub(pattern, replacement, text)

    if text == old_text:
        # fallback za slučaj da je datoteka čudno formatirana
        text = text.replace(
            'optimize_image_field(instance, "avatar")',
            '# Avatar se ne komprimira dodatno; crop editor već sprema avatar u visokoj kvaliteti.\n    # optimize_image_field(instance, "avatar")'
        )
        text = text.replace(
            "optimize_image_field(instance, 'avatar')",
            "# Avatar se ne komprimira dodatno; crop editor već sprema avatar u visokoj kvaliteti.\n    # optimize_image_field(instance, 'avatar')"
        )

    if text != old_text:
        signals_path.write_text(text, encoding='utf-8')
        changed.append(str(signals_path.relative_to(ROOT)))
    else:
        print('Nisam našao optimize_image_field(instance, "avatar") u image_signals.py. Preskačem signal promjenu.')
else:
    print('Nema blog/image_signals.py. Preskačem server optimizaciju.')

print('Gotovo. Promijenjeno:')
for item in changed:
    print(' -', item)
print('\nVAŽNO: za provjeru kvalitete odaberi novu sliku, klikni Primijeni avatar i Spremi promjene. Stari avatar ostaje stari.')
