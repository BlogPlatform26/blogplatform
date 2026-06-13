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
backup_dir = ROOT / f"backup_prije_jos_manjeg_filtera_postova_{timestamp}"
backup_dir.mkdir(exist_ok=True)

backup_path = backup_dir / posts_tab_path.relative_to(ROOT)
backup_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(posts_tab_path, backup_path)

print(f"Backup napravljen: {backup_dir.name}")

text = posts_tab_path.read_text(encoding="utf-8")

# Osiguraj da panel ima kompaktne klase ako ih prethodna skripta nije dobro dodala.
text = text.replace(
    '<div class="card mb-4 shadow-sm post-filter-panel">',
    '<div class="card mb-3 shadow-sm post-filter-panel post-filter-panel-compact">'
)

text = text.replace(
    '<form method="GET" class="row g-3 align-items-end">',
    '<form method="GET" class="post-filter-form-compact">'
)

text = text.replace('class="col-md-4"', 'class="post-filter-field"')
text = text.replace('class="col-md-3 d-flex gap-2"', 'class="post-filter-actions"')
text = text.replace('class="col-md-3"', 'class="post-filter-field"')

text = text.replace('class="form-label"', 'class="form-label post-filter-label"')
text = text.replace('class="form-control"', 'class="form-control form-control-sm post-filter-input"')
text = text.replace('class="form-select"', 'class="form-select form-select-sm post-filter-input"')

text = text.replace('class="btn btn-primary flex-fill"', 'class="btn btn-primary btn-sm post-filter-btn"')
text = text.replace('class="btn btn-outline-secondary flex-fill"', 'class="btn btn-outline-secondary btn-sm post-filter-btn"')

# Makni stariji override ako je već dodan.
start_marker = "/* === Super kompaktan filter postova === */"
start = text.find(start_marker)

if start != -1:
    style_start = text.rfind("<style>", 0, start)
    style_end = text.find("</style>", start)
    if style_start != -1 and style_end != -1:
        text = text[:style_start] + text[style_end + len("</style>"):]

css = """
<style>
/* === Super kompaktan filter postova === */
.post-filter-panel-compact {
    margin-bottom: 14px !important;
}

.post-filter-panel-compact .card-body {
    padding: 8px 10px !important;
}

.post-filter-form-compact {
    display: grid !important;
    grid-template-columns: minmax(130px, 1.2fr) minmax(130px, 1.15fr) minmax(105px, .85fr) minmax(88px, .68fr) minmax(88px, .68fr) minmax(96px, .75fr) auto !important;
    gap: 6px !important;
    align-items: end !important;
}

.post-filter-field,
.post-filter-actions {
    min-width: 0 !important;
}

.post-filter-label {
    font-size: 0.72rem !important;
    line-height: 1.1 !important;
    margin-bottom: 2px !important;
    white-space: nowrap !important;
}

.post-filter-input {
    min-height: 28px !important;
    height: 28px !important;
    font-size: 0.78rem !important;
    line-height: 1.1 !important;
    padding: 2px 8px !important;
}

.post-filter-actions {
    display: flex !important;
    gap: 5px !important;
    align-items: end !important;
    grid-column: auto !important;
}

.post-filter-btn {
    min-width: 58px !important;
    height: 28px !important;
    min-height: 28px !important;
    font-size: 0.76rem !important;
    line-height: 1 !important;
    padding: 3px 8px !important;
    white-space: nowrap !important;
}

.post-filter-panel-compact .small.text-muted {
    margin-top: 6px !important;
    font-size: 0.72rem !important;
}

/* Ne prelamaj u 2 reda na desktopu */
@media (min-width: 901px) {
    .post-filter-form-compact {
        grid-template-columns: minmax(130px, 1.2fr) minmax(130px, 1.15fr) minmax(105px, .85fr) minmax(88px, .68fr) minmax(88px, .68fr) minmax(96px, .75fr) auto !important;
    }

    .post-filter-actions {
        grid-column: auto !important;
        flex-direction: row !important;
    }
}

/* Tek na manjim ekranima prelamaj */
@media (max-width: 900px) {
    .post-filter-form-compact {
        grid-template-columns: 1fr 1fr !important;
    }

    .post-filter-actions {
        grid-column: span 2 !important;
    }
}

@media (max-width: 560px) {
    .post-filter-form-compact {
        grid-template-columns: 1fr !important;
    }

    .post-filter-actions {
        grid-column: auto !important;
        flex-direction: column !important;
        align-items: stretch !important;
    }

    .post-filter-btn {
        width: 100% !important;
    }
}
</style>
"""

text += "\n" + css + "\n"

posts_tab_path.write_text(text, encoding="utf-8")

print("GOTOVO.")
print("Filter panel je dodatno smanjen.")
print("Na desktopu ide u jedan red, a prelama se tek ispod 900px širine.")
print("\nSada pokreni:")
print("python manage.py runserver")
print("\nU browseru napravi CTRL + F5.")
