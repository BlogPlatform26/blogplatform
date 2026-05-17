from pathlib import Path

js_path = Path('blog/static/blog/js/blog_settings_avatar.js')
backup_path = Path('blog/static/blog/js/blog_settings_avatar.js.bak_avatar_scroll_zoom_only')

if not js_path.exists():
    raise SystemExit('Ne postoji blog/static/blog/js/blog_settings_avatar.js')

text = js_path.read_text(encoding='utf-8')

if not backup_path.exists():
    backup_path.write_text(text, encoding='utf-8')

# Ne koristimo Cropperov automatski wheel zoom jer može zaobići tvoje ograničenje.
# Ostaje false, a ispod dodajemo naš zoom preko slidera.
text = text.replace('zoomOnWheel: true,', 'zoomOnWheel: false,')

if 'avatarScrollZoomOnly' not in text:
    wheel_block = ''' if (modalEl && zoomRange) { const avatarScrollZoomOnlyTarget = modalEl.querySelector(".avatar-crop-frame") || modalEl.querySelector(".avatar-crop-stage") || modalEl; avatarScrollZoomOnlyTarget.addEventListener("wheel", function (event) { if (!cropper || !zoomRange) return; event.preventDefault(); const currentValue = Number(zoomRange.value || 0); const minValue = Number(zoomRange.min || 0); const maxValue = Number(zoomRange.max || 100); const step = event.deltaY < 0 ? 5 : -5; const nextValue = Math.max(minValue, Math.min(maxValue, currentValue + step)); if (nextValue === currentValue) return; zoomRange.value = String(nextValue); setZoomFromRange(nextValue); }, { passive: false }); }'''
    marker = ' if (rotateBtn) {'
    if marker not in text:
        raise SystemExit('Nisam našao mjesto za ubacivanje wheel zooma. Ništa nije promijenjeno.')
    text = text.replace(marker, wheel_block + marker, 1)

js_path.write_text(text, encoding='utf-8')
print('Dodao sam zoom kotačićem miša samo za avatar.')
