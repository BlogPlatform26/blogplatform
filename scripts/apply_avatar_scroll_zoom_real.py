from pathlib import Path
import re
import shutil

path = Path('blog/static/blog/js/blog_settings_avatar.js')
if not path.exists():
    raise SystemExit('Ne mogu naći blog/static/blog/js/blog_settings_avatar.js')

backup = path.with_suffix(path.suffix + '.bak_before_scroll_zoom_real')
if not backup.exists():
    shutil.copy2(path, backup)

js = path.read_text(encoding='utf-8')
original = js

# Makni pokvareni wheel blok ako postoji. Taj blok koristi cropper/setZoomFromRange,
# a trenutni avatar editor koristi vlastiti state i handleZoomChange().
js = re.sub(
    r'if \(modalEl && zoomRange\) \{\s*const avatarScrollZoomOnlyTarget\s*=\s*modalEl\.querySelector\("\.avatar-crop-frame"\)\s*\|\|\s*modalEl\.querySelector\("\.avatar-crop-stage"\)\s*\|\|\s*modalEl;\s*avatarScrollZoomOnlyTarget\.addEventListener\("wheel", function \(event\) \{.*?\}, \{ passive: false \}\);\s*\}\s*',
    '',
    js,
    flags=re.S,
)

block = '''if (frame && zoomRange) { frame.addEventListener("wheel", function (event) { if (!imageLoaded) return; event.preventDefault(); const currentValue = Number(zoomRange.value || 0); const minValue = Number(zoomRange.min || 0); const maxValue = Number(zoomRange.max || 100); const step = event.deltaY < 0 ? 4 : -4; const nextValue = Math.max(minValue, Math.min(maxValue, currentValue + step)); if (nextValue === currentValue) return; zoomRange.value = String(nextValue); handleZoomChange(); }, { passive: false }); } '''

if 'frame.addEventListener("wheel"' not in js:
    marker = 'if (rotateBtn) {'
    index = js.find(marker)
    if index == -1:
        raise SystemExit('Ne mogu naći mjesto prije rotateBtn za ubacivanje scroll zooma.')
    js = js[:index] + block + js[index:]

path.write_text(js, encoding='utf-8')

print('OK: scroll zoom za avatar je dodan.')
print('Backup:', backup)
