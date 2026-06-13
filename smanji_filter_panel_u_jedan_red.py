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
backup_dir = ROOT / f"backup_prije_smanjenja_filtera_postova_{timestamp}"
backup_dir.mkdir(exist_ok=True)

backup_path = backup_dir / posts_tab_path.relative_to(ROOT)
backup_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(posts_tab_path, backup_path)

print(f"Backup napravljen: {backup_dir.name}")

text = posts_tab_path.read_text(encoding="utf-8")

start_marker = '<div class="card mb-4 shadow-sm post-filter-panel">'
end_marker = '<!-- EDIT POST -->'

start = text.find(start_marker)
end = text.find(end_marker, start)

if start == -1 or end == -1:
    print("GREŠKA: Ne nalazim filter panel u _posts_tab.html.")
    print("Nisam ništa mijenjao.")
    raise SystemExit(1)

before = text[:start]
panel = text[start:end]
after = text[end:]

panel = panel.replace(
    '<div class="card mb-4 shadow-sm post-filter-panel">',
    '<div class="card mb-3 shadow-sm post-filter-panel post-filter-panel-compact">',
    1
)

panel = panel.replace(
    '<form method="GET" class="row g-3 align-items-end">',
    '<form method="GET" class="post-filter-form-compact">',
    1
)

panel = panel.replace('class="col-md-4"', 'class="post-filter-field"')
panel = panel.replace('class="col-md-3"', 'class="post-filter-field"')
panel = panel.replace('class="col-md-3 d-flex gap-2"', 'class="post-filter-actions"')
panel = panel.replace('class="form-label"', 'class="form-label post-filter-label"')
panel = panel.replace('class="form-control"', 'class="form-control form-control-sm post-filter-input"')
panel = panel.replace('class="form-select"', 'class="form-select form-select-sm post-filter-input"')
panel = panel.replace('class="btn btn-primary flex-fill"', 'class="btn btn-primary btn-sm post-filter-btn"')
panel = panel.replace('class="btn btn-outline-secondary flex-fill"', 'class="btn btn-outline-secondary btn-sm post-filter-btn"')

text = before + panel + after

compact_css = """
<style>
    .post-filter-panel-compact .card-body {
        padding: 12px 14px;
    }

    .post-filter-form-compact {
        display: grid;
        grid-template-columns: minmax(150px, 1.35fr) minmax(150px, 1.25fr) minmax(120px, 1fr) minmax(105px, .8fr) minmax(105px, .8fr) minmax(115px, .9fr) auto auto;
        gap: 10px;
        align-items: end;
    }

    .post-filter-label {
        font-size: 0.82rem;
        margin-bottom: 4px;
        white-space: nowrap;
    }

    .post-filter-input {
        min-height: 34px;
        font-size: 0.9rem;
    }

    .post-filter-actions {
        display: flex;
        gap: 8px;
        align-items: end;
    }

    .post-filter-btn {
        min-width: 84px;
        min-height: 34px;
        white-space: nowrap;
    }

    .post-filter-panel-compact .small.text-muted {
        margin-top: 8px !important;
    }

    @media (max-width: 1400px) {
        .post-filter-form-compact {
            grid-template-columns: repeat(3, minmax(160px, 1fr));
        }

        .post-filter-actions {
            grid-column: span 3;
        }
    }

    @media (max-width: 768px) {
        .post-filter-form-compact {
            grid-template-columns: 1fr;
        }

        .post-filter-actions {
            grid-column: auto;
            flex-direction: column;
            align-items: stretch;
        }

        .post-filter-btn {
            width: 100%;
        }
    }
</style>
"""

if "post-filter-form-compact" not in after and "post-filter-form-compact" not in before:
    # class je već u panelu, ali CSS možda ne postoji. Provjeravamo poseban CSS marker.
    pass

if ".post-filter-form-compact" not in text:
    # ovo se ne bi smjelo dogoditi jer smo gore dodali klasu
    print("GREŠKA: Nešto nije dobro dodano u panel.")
    raise SystemExit(1)

if "grid-template-columns: minmax(150px, 1.35fr)" not in text:
    insert_pos = text.rfind("</style>")
    if insert_pos != -1:
        text = text[:insert_pos] + "\n" + compact_css.replace("<style>", "").replace("</style>", "") + "\n" + text[insert_pos:]
    else:
        text += "\n" + compact_css + "\n"

posts_tab_path.write_text(text, encoding="utf-8")

print("GOTOVO.")
print("Filter panel je smanjen i složen u jedan red na većim ekranima.")
print("Na manjim ekranima se automatski prelama da ne pukne prikaz.")
print("\nSada pokreni:")
print("python manage.py runserver")
print("\nU browseru napravi CTRL + F5.")
