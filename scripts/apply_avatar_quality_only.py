from pathlib import Path
import shutil
import re

js_path = Path('blog/static/blog/js/blog_settings_avatar.js')
backup_path = Path('blog/static/blog/js/blog_settings_avatar.js.bak_avatar_quality_only')

if not js_path.exists():
    raise SystemExit('Ne mogu naći blog/static/blog/js/blog_settings_avatar.js')

if not backup_path.exists():
    shutil.copy2(js_path, backup_path)

js = js_path.read_text(encoding='utf-8')
original = js

# Mijenjamo samo finalni export avatara, ne preview, ne izgled, ne zoom i ne cropper logiku.
# Cilj: veći avatar i PNG bez JPEG gubitka kvalitete.
pattern = re.compile(
    r'const\s+canvas\s*=\s*cropper\.getCroppedCanvas\(\{\s*'
    r'width:\s*\d+\s*,\s*'
    r'height:\s*\d+\s*,\s*'
    r'imageSmoothingEnabled:\s*true\s*,\s*'
    r'imageSmoothingQuality:\s*["\']high["\']\s*,?\s*'
    r'\}\);\s*'
    r'if\s*\(!canvas\)\s*return\s*false;\s*'
    r'hiddenInput\.value\s*=\s*canvas\.toDataURL\(["\']image/[^"\']+["\'](?:\s*,\s*[0-9.]+)?\);'
)

replacement = (
    'const canvas = cropper.getCroppedCanvas({ width: 1000, height: 1000, '
    'imageSmoothingEnabled: true, imageSmoothingQuality: "high", }); '
    'if (!canvas) return false; '
    'hiddenInput.value = canvas.toDataURL("image/png");'
)

js, count = pattern.subn(replacement, js, count=1)

if count != 1:
    raise SystemExit('Nisam našao točan dio za spremanje avatara. Ništa nije promijenjeno.')

js_path.write_text(js, encoding='utf-8')

print('Gotovo: avatar se sada sprema kao 1000x1000 PNG bez JPEG kompresije.')
print('Backup:', backup_path)
