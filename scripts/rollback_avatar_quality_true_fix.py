from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).parent.name == 'scripts' else Path.cwd()
files = [
    ROOT / 'blog' / 'static' / 'blog' / 'js' / 'blog_settings_avatar.js',
    ROOT / 'blog' / 'image_signals.py',
]

for path in files:
    backups = sorted(path.parent.glob(path.name + '.bak_avatar_quality_true_*'), key=lambda p: p.stat().st_mtime, reverse=True)
    if backups:
        shutil.copy2(backups[0], path)
        print(f'Vraćeno: {path.relative_to(ROOT)} iz {backups[0].name}')
    else:
        print(f'Nema backupa za: {path.relative_to(ROOT)}')
