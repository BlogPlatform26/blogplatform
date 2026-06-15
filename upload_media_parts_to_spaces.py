import os
import zipfile
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogplatform.settings")

import django
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def main():
    parts = sorted(Path("media_parts").glob("media_part_*.zip"))

    total = 0
    skipped = 0

    print("ZIP dijelova:", len(parts))
    print("Storage:", default_storage.__class__)

    for part in parts:
        print("Otvaram:", part)

        with zipfile.ZipFile(part) as zip_file:
            for name in zip_file.namelist():
                if default_storage.exists(name):
                    skipped += 1
                    continue

                with zip_file.open(name) as file:
                    default_storage.save(name, ContentFile(file.read()))
                    total += 1

    print("OK")
    print("Uploadano:", total)
    print("Preskoceno:", skipped)


if __name__ == "__main__":
    main()