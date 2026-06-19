from pathlib import Path
from datetime import datetime
import sys

ROOT = Path.cwd()
POSTS_TAB = ROOT / "blog" / "templates" / "blog" / "settings" / "_posts_tab.html"
STYLE_CSS = ROOT / "blog" / "static" / "css" / "style.css"

MARKER_HTML = "post-image-inputs"
MARKER_JS = "POST_IMAGE_INPUTS_SCRIPT_START"
MARKER_CSS = "POST_IMAGE_INPUTS_CSS_START"

OLD_NEW_POST = '''<div class="mb-3">
                                        <label class="form-label d-block">Slike</label>
                                        <input type="file" name="images" class="form-control" accept="image/*" multiple>
                                        <div class="small text-muted mt-1">Možeš odabrati više slika odjednom.</div>
                                    </div>'''

NEW_NEW_POST = '''<div class="mb-3 post-image-upload-box">
                                        <label class="form-label d-block">Slike</label>

                                        <div class="post-image-inputs" data-max-images="5">
                                            <div class="post-image-input-row mb-2">
                                                <input type="file"
                                                       name="images"
                                                       class="form-control post-image-input"
                                                       accept="image/*"
                                                       multiple>
                                            </div>
                                        </div>

                                        <button type="button"
                                                class="btn btn-sm btn-outline-primary mt-1 add-post-image-input">
                                            + Dodaj još sliku
                                        </button>

                                        <div class="small text-muted mt-1">
                                            Možeš odabrati više slika odjednom ili dodavati jednu po jednu. Maksimalno 5 slika.
                                        </div>

                                        <div class="small text-danger mt-1 d-none post-image-limit-message">
                                            Možeš dodati najviše 5 slika.
                                        </div>
                                    </div>'''

OLD_EDIT_POST = '''<div class="mb-3">
                                    <label class="form-label d-block">Dodaj nove slike</label>
                                    <input type="file" name="images" class="form-control" accept="image/*" multiple>
                                </div>'''

NEW_EDIT_POST = '''<div class="mb-3 post-image-upload-box">
                                    <label class="form-label d-block">Dodaj nove slike</label>

                                    <div class="post-image-inputs" data-max-images="5">
                                        <div class="post-image-input-row mb-2">
                                            <input type="file"
                                                   name="images"
                                                   class="form-control post-image-input"
                                                   accept="image/*"
                                                   multiple>
                                        </div>
                                    </div>

                                    <button type="button"
                                            class="btn btn-sm btn-outline-primary mt-1 add-post-image-input">
                                        + Dodaj još sliku
                                    </button>

                                    <div class="small text-muted mt-1">
                                        Možeš dodati više slika odjednom ili jednu po jednu. Maksimalno 5 slika.
                                    </div>

                                    <div class="small text-danger mt-1 d-none post-image-limit-message">
                                        Možeš dodati najviše 5 slika.
                                    </div>
                                </div>'''

JS_BLOCK = '''

<!-- POST_IMAGE_INPUTS_SCRIPT_START -->
<script>
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".add-post-image-input").forEach(function (button) {
            button.addEventListener("click", function () {
                const wrapper = button.closest(".post-image-upload-box");
                if (!wrapper) {
                    return;
                }

                const inputsBox = wrapper.querySelector(".post-image-inputs");
                const message = wrapper.querySelector(".post-image-limit-message");
                const maxImages = Number(inputsBox.dataset.maxImages || 5);
                const currentInputs = inputsBox.querySelectorAll(".post-image-input").length;

                if (currentInputs >= maxImages) {
                    if (message) {
                        message.classList.remove("d-none");
                    }
                    return;
                }

                if (message) {
                    message.classList.add("d-none");
                }

                const row = document.createElement("div");
                row.className = "post-image-input-row mb-2 d-flex gap-2";

                row.innerHTML = `
                    <input type="file"
                           name="images"
                           class="form-control post-image-input"
                           accept="image/*"
                           multiple>

                    <button type="button"
                            class="btn btn-sm btn-outline-danger remove-post-image-input">
                        ×
                    </button>
                `;

                inputsBox.appendChild(row);

                row.querySelector(".remove-post-image-input").addEventListener("click", function () {
                    row.remove();
                    if (message) {
                        message.classList.add("d-none");
                    }
                });
            });
        });

        document.querySelectorAll("form").forEach(function (form) {
            form.addEventListener("submit", function (event) {
                const inputsBox = form.querySelector(".post-image-inputs");

                if (!inputsBox) {
                    return;
                }

                const message = form.querySelector(".post-image-limit-message");
                const maxImages = Number(inputsBox.dataset.maxImages || 5);
                let totalFiles = 0;

                inputsBox.querySelectorAll(".post-image-input").forEach(function (input) {
                    totalFiles += input.files.length;
                });

                if (totalFiles > maxImages) {
                    event.preventDefault();

                    if (message) {
                        message.classList.remove("d-none");
                    }
                }
            });
        });
    });
</script>
<!-- POST_IMAGE_INPUTS_SCRIPT_END -->
'''

CSS_BLOCK = '''

/* POST_IMAGE_INPUTS_CSS_START */
.post-image-input-row .remove-post-image-input {
    min-width: 38px;
}
/* POST_IMAGE_INPUTS_CSS_END */
'''

def make_backup(path: Path):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(path.name + f".backup_prije_slika_{stamp}")
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def main():
    if not POSTS_TAB.exists():
        print(f"GRESKA: Ne postoji file: {POSTS_TAB}")
        print("Pokreni skriptu iz root foldera projekta, npr. C:\\Users\\mario\\blogplatform")
        sys.exit(1)

    if not STYLE_CSS.exists():
        print(f"GRESKA: Ne postoji file: {STYLE_CSS}")
        print("Pokreni skriptu iz root foldera projekta, npr. C:\\Users\\mario\\blogplatform")
        sys.exit(1)

    html = POSTS_TAB.read_text(encoding="utf-8")
    css = STYLE_CSS.read_text(encoding="utf-8")

    html_backup = make_backup(POSTS_TAB)
    css_backup = make_backup(STYLE_CSS)

    changed_html = False
    changed_css = False

    if MARKER_HTML in html:
        print("HTML dio za dodavanje slika vec postoji. Ne mijenjam ga ponovno.")
    else:
        if OLD_NEW_POST in html:
            html = html.replace(OLD_NEW_POST, NEW_NEW_POST, 1)
            changed_html = True
            print("Dodano u NOVI POST.")
        else:
            print("UPOZORENJE: Nisam nasao tocno mjesto za slike u NOVI POST.")

        if OLD_EDIT_POST in html:
            html = html.replace(OLD_EDIT_POST, NEW_EDIT_POST, 1)
            changed_html = True
            print("Dodano u UREDI POST.")
        else:
            print("UPOZORENJE: Nisam nasao tocno mjesto za slike u UREDI POST.")

    if MARKER_JS not in html:
        html = html.rstrip() + JS_BLOCK + "\n"
        changed_html = True
        print("Dodan JavaScript za dodavanje slika.")
    else:
        print("JavaScript za dodavanje slika vec postoji.")

    if MARKER_CSS not in css:
        css = css.rstrip() + CSS_BLOCK + "\n"
        changed_css = True
        print("Dodan CSS za dodavanje slika.")
    else:
        print("CSS za dodavanje slika vec postoji.")

    if changed_html:
        POSTS_TAB.write_text(html, encoding="utf-8")
    if changed_css:
        STYLE_CSS.write_text(css, encoding="utf-8")

    print("\nGotovo.")
    print(f"Backup HTML: {html_backup}")
    print(f"Backup CSS:  {css_backup}")
    print("Sada otvori stranicu i napravi Ctrl + F5.")

if __name__ == "__main__":
    main()
