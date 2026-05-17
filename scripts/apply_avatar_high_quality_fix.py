from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / "blog" / "static" / "blog" / "js" / "blog_settings_avatar.js"
SIGNALS_PATH = ROOT / "blog" / "image_signals.py"
BACKUP_DIR = ROOT / "scripts" / "_avatar_quality_backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Ne postoji file: {path}")
    backup_path = BACKUP_DIR / (path.name + ".bak_before_avatar_high_quality")
    if not backup_path.exists():
        shutil.copy2(path, backup_path)
    return backup_path


def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

# 1) Frontend crop kvaliteta: veći canvas + bolji JPEG quality.
backup(JS_PATH)
js = read_text(JS_PATH)
original_js = js

replacements = [
    ("getCroppedCanvas(420)", "getCroppedCanvas(900)"),
    ("toDataURL(\"image/jpeg\", 0.92)", "toDataURL(\"image/jpeg\", 0.96)"),
    ("toDataURL('image/jpeg', 0.92)", "toDataURL('image/jpeg', 0.96)"),
]
for old, new in replacements:
    js = js.replace(old, new)

if js == original_js:
    print("UPOZORENJE: Avatar JS nije promijenjen. Možda je već promijenjen ili ima drugačiji oblik koda.")
else:
    write_text(JS_PATH, js)
    print("OK: Avatar JS sprema veći i kvalitetniji crop.")

# 2) Server kompresija: avatar ne smije ponovno pasti na kvalitetu 82.
backup(SIGNALS_PATH)
signals = read_text(SIGNALS_PATH)
original_signals = signals

signals = signals.replace(
    'optimize_image_field(instance, "avatar")',
    'optimize_image_field(instance, "avatar", max_width=900, max_height=900, quality=95)'
)
signals = signals.replace(
    "optimize_image_field(instance, 'avatar')",
    "optimize_image_field(instance, 'avatar', max_width=900, max_height=900, quality=95)"
)

if signals == original_signals:
    if "quality=95" in signals and "avatar" in signals:
        print("OK: Avatar server kvaliteta je već podešena.")
    else:
        print("UPOZORENJE: image_signals.py nije promijenjen. Provjeri ručno dio optimize_profile_images.")
else:
    write_text(SIGNALS_PATH, signals)
    print("OK: Server optimizacija avatara je podešena na 900x900 i quality=95.")

print("Gotovo. Pokreni: python manage.py check")
