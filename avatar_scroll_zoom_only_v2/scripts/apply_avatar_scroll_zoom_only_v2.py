from pathlib import Path
from datetime import datetime
import shutil

JS_PATH = Path('blog/static/blog/js/blog_settings_avatar.js')
BACKUP_PATH = Path('blog/static/blog/js/blog_settings_avatar.js.bak_scroll_zoom_only_v2')

WHEEL_CODE = '''

    const avatarWheelArea = modalEl ? modalEl.querySelector(".avatar-crop-frame") : null;
    if (avatarWheelArea && zoomRange) {
        avatarWheelArea.addEventListener("wheel", function (event) {
            if (!cropper) return;

            event.preventDefault();

            const minValue = Number(zoomRange.min || 0);
            const maxValue = Number(zoomRange.max || 100);
            const currentValue = Number(zoomRange.value || 0);
            const step = event.deltaY < 0 ? 5 : -5;
            const nextValue = Math.max(minValue, Math.min(maxValue, currentValue + step));

            if (nextValue === currentValue) return;

            zoomRange.value = String(nextValue);
            setZoomFromRange(nextValue);
        }, { passive: false });
    }
'''

ONE_LINE_WHEEL_CODE = ' const avatarWheelArea = modalEl ? modalEl.querySelector(".avatar-crop-frame") : null; if (avatarWheelArea && zoomRange) { avatarWheelArea.addEventListener("wheel", function (event) { if (!cropper) return; event.preventDefault(); const minValue = Number(zoomRange.min || 0); const maxValue = Number(zoomRange.max || 100); const currentValue = Number(zoomRange.value || 0); const step = event.deltaY < 0 ? 5 : -5; const nextValue = Math.max(minValue, Math.min(maxValue, currentValue + step)); if (nextValue === currentValue) return; zoomRange.value = String(nextValue); setZoomFromRange(nextValue); }, { passive: false }); } '

MARKER = 'avatarWheelArea'


def main():
    if not JS_PATH.exists():
        raise SystemExit(f'Nisam našao {JS_PATH}')

    original = JS_PATH.read_text(encoding='utf-8')

    if not BACKUP_PATH.exists():
        shutil.copy2(JS_PATH, BACKUP_PATH)

    if MARKER in original:
        print('Scroll zoom već postoji. Ništa nije mijenjano.')
        return

    text = original

    # Ne koristimo Cropperov native zoom jer želimo da radi preko postojećeg slidera
    # i da ne ide ispod minimalne vrijednosti.
    text = text.replace('zoomOnWheel: true', 'zoomOnWheel: false')

    target = 'if (zoomRange) { zoomRange.setAttribute("min", "0"); zoomRange.setAttribute("max", "100"); zoomRange.setAttribute("value", "0"); zoomRange.addEventListener("input", function () { setZoomFromRange(this.value); }); } if (rotateBtn) {'
    replacement = 'if (zoomRange) { zoomRange.setAttribute("min", "0"); zoomRange.setAttribute("max", "100"); zoomRange.setAttribute("value", "0"); zoomRange.addEventListener("input", function () { setZoomFromRange(this.value); }); }' + ONE_LINE_WHEEL_CODE + 'if (rotateBtn) {'

    if target in text:
        text = text.replace(target, replacement, 1)
    else:
        # Fallback za formatirani JS: ubaci prije rotateBtn dijela.
        fallback = 'if (rotateBtn) {'
        if fallback not in text:
            raise SystemExit('Nisam našao mjesto za ubaciti scroll zoom. Datoteka nije promijenjena.')
        text = text.replace(fallback, WHEEL_CODE + '\n    if (rotateBtn) {', 1)

    JS_PATH.write_text(text, encoding='utf-8')
    print('Dodao sam scroll zoom samo za avatar editor.')
    print('Backup:', BACKUP_PATH)


if __name__ == '__main__':
    main()
