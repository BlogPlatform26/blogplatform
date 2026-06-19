from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

ROOT = Path.cwd()
POSTS_TAB = ROOT / "blog" / "templates" / "blog" / "settings" / "_posts_tab.html"
STYLE_CSS = ROOT / "blog" / "static" / "css" / "style.css"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

NEW_POST_IMAGES_BLOCK = '''<div class="mb-3">
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

EDIT_POST_IMAGES_BLOCK = '''<div class="mb-3">
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

IMAGE_INPUT_SCRIPT = '''

<script>
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".add-post-image-input").forEach(function (button) {
            button.addEventListener("click", function () {
                const wrapper = button.closest(".mb-3");

                if (!wrapper) {
                    return;
                }

                const inputsBox = wrapper.querySelector(".post-image-inputs");
                const message = wrapper.querySelector(".post-image-limit-message");

                if (!inputsBox) {
                    return;
                }

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
                            class="btn btn-sm btn-outline-danger remove-post-image-input"
                            aria-label="Makni ovaj unos slike">
                        ×
                    </button>
                `;

                inputsBox.appendChild(row);

                const removeButton = row.querySelector(".remove-post-image-input");

                if (removeButton) {
                    removeButton.addEventListener("click", function () {
                        row.remove();

                        if (message) {
                            message.classList.add("d-none");
                        }
                    });
                }
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
'''

IMAGE_INPUT_CSS = '''

/* Dodavanje slika u post - dodatni inputi */
.post-image-input-row .remove-post-image-input {
    min-width: 34px;
    padding-left: 8px;
    padding-right: 8px;
}
'''


def backup_file(path: Path) -> Path:
    backup_path = path.with_suffix(path.suffix + f".bak_image_inputs_{STAMP}")
    shutil.copy2(path, backup_path)
    return backup_path


def replace_regex_once(text: str, pattern: str, replacement: str, label: str) -> tuple[str, bool]:
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count == 0:
        print(f"UPOZORENJE: nisam našao blok: {label}")
        return text, False
    print(f"OK: zamijenjen blok: {label}")
    return new_text, True


def main() -> int:
    if not POSTS_TAB.exists():
        print(f"GREŠKA: ne postoji file: {POSTS_TAB}")
        print("Pokreni skriptu iz root foldera projekta, npr. C:\\Users\\mario\\blogplatform")
        return 1

    if not STYLE_CSS.exists():
        print(f"GREŠKA: ne postoji file: {STYLE_CSS}")
        print("Pokreni skriptu iz root foldera projekta, npr. C:\\Users\\mario\\blogplatform")
        return 1

    posts_backup = backup_file(POSTS_TAB)
    css_backup = backup_file(STYLE_CSS)
    print(f"Backup napravljen: {posts_backup}")
    print(f"Backup napravljen: {css_backup}")

    text = POSTS_TAB.read_text(encoding="utf-8")

    if "post-image-inputs" in text:
        print("INFO: izgleda da su dodatni inputi za slike već dodani. Preskačem zamjenu HTML blokova.")
    else:
        new_post_pattern = r'''<div class="mb-3">\s*<label class="form-label d-block">Slike</label>\s*<input type="file"\s+name="images"\s+class="form-control"\s+accept="image/\*"\s+multiple>\s*<div class="small text-muted mt-1">Možeš odabrati više slika odjednom\.</div>\s*</div>'''
        edit_post_pattern = r'''<div class="mb-3">\s*<label class="form-label d-block">Dodaj nove slike</label>\s*<input type="file"\s+name="images"\s+class="form-control"\s+accept="image/\*"\s+multiple>\s*</div>'''

        text, ok_new = replace_regex_once(text, new_post_pattern, NEW_POST_IMAGES_BLOCK, "Slike - novi post")
        text, ok_edit = replace_regex_once(text, edit_post_pattern, EDIT_POST_IMAGES_BLOCK, "Dodaj nove slike - uredi post")

        if not (ok_new or ok_edit):
            print("GREŠKA: nisam našao ni jedan blok za slike. Vraćam backup.")
            shutil.copy2(posts_backup, POSTS_TAB)
            return 1

    if "add-post-image-input" not in text or "remove-post-image-input" not in text:
        text += IMAGE_INPUT_SCRIPT
        print("OK: dodan JavaScript za dodavanje slika.")
    else:
        if "remove-post-image-input" not in text:
            text += IMAGE_INPUT_SCRIPT
            print("OK: dodan JavaScript za dodavanje slika.")
        else:
            print("INFO: JavaScript za dodavanje slika već postoji. Preskačem.")

    POSTS_TAB.write_text(text, encoding="utf-8")

    css_text = STYLE_CSS.read_text(encoding="utf-8")
    if "Dodavanje slika u post - dodatni inputi" not in css_text:
        css_text += IMAGE_INPUT_CSS
        STYLE_CSS.write_text(css_text, encoding="utf-8")
        print("OK: dodan CSS za dodatne inpute slika.")
    else:
        print("INFO: CSS za dodatne inpute slika već postoji. Preskačem.")

    print("\nGOTOVO.")
    print("Sada pokreni/refreshaj stranicu i napravi Ctrl + F5.")
    print("Promijenjeni fileovi:")
    print(f"- {POSTS_TAB}")
    print(f"- {STYLE_CSS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
