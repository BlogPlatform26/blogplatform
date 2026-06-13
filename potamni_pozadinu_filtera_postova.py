from pathlib import Path
import shutil
import datetime

ROOT = Path.cwd()

if not (ROOT / "manage.py").exists():
    print("GREŠKA: Pokreni skriptu iz glavnog foldera projekta: C:\\Users\\mario\\blogplatform")
    raise SystemExit(1)

posts_tab_path = ROOT / "blog" / "templates" / "blog" / "settings" / "_posts_tab.html"

if not posts_tab_path.exists():
    print("GREŠKA: Ne nalazim blog\\templates\\blog\\settings\\_posts_tab.html")
    raise SystemExit(1)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = ROOT / f"backup_prije_tamnije_pozadine_filtera_{timestamp}"
backup_dir.mkdir(exist_ok=True)

backup_path = backup_dir / posts_tab_path.relative_to(ROOT)
backup_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(posts_tab_path, backup_path)

print(f"Backup napravljen: {backup_dir.name}")

text = posts_tab_path.read_text(encoding="utf-8")

# Ako već postoji stariji override za tamniju pozadinu, makni ga da se ne gomila.
marker = "/* === Tamnija pozadina filter panela postova === */"
start = text.find(marker)
if start != -1:
    style_start = text.rfind("<style>", 0, start)
    style_end = text.find("</style>", start)
    if style_start != -1 and style_end != -1:
        text = text[:style_start] + text[style_end + len("</style>"):]

css = """
<style>
/* === Tamnija pozadina filter panela postova === */
.post-filter-panel,
.post-filter-panel-compact {
    background: #f1f3f5 !important;
    border: 1px solid #d7dbe0 !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
}

.post-filter-panel .card-body,
.post-filter-panel-compact .card-body {
    background: #f1f3f5 !important;
}

.post-filter-panel .post-filter-input,
.post-filter-panel-compact .post-filter-input {
    background: #ffffff !important;
    border-color: #cfd6dd !important;
}

.post-filter-panel .post-filter-input:focus,
.post-filter-panel-compact .post-filter-input:focus {
    background: #ffffff !important;
}

.post-filter-panel .post-filter-label,
.post-filter-panel-compact .post-filter-label {
    color: #2f3b46 !important;
}
</style>
"""

text += "\n" + css + "\n"

posts_tab_path.write_text(text, encoding="utf-8")

print("GOTOVO.")
print("Filter panel sada ima malo tamniju pozadinu.")
print("\nSada pokreni:")
print("python manage.py runserver")
print("\nU browseru napravi CTRL + F5.")
