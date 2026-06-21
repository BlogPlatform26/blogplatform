import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from django.core.files import File
from django.utils.text import slugify

from blog.models import AmbientMusicTrack


AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a"}


CATEGORY_KEYWORDS = [
    ("jazz", ["jazz", "lounge", "cafe", "night-summer-lounge", "easy-jazz"]),
    ("fantasy", ["magic", "fantasy", "elvish", "forest", "moon", "harry", "rpg"]),
    ("mystery", ["horror", "creepy", "mystery", "shadows", "halloween"]),
    ("cinematic", ["cinematic", "documentary", "travel", "trailer", "orchestra", "middle-east"]),
    ("fun", ["comedy", "cartoon", "funny", "food", "cooking", "christmas", "bells"]),
    ("romantic", ["love", "romantic", "lyrical", "beautiful", "piano", "cello", "emotional"]),
    ("calm", ["calm", "soft", "relax", "relaxing", "soothing", "lullaby", "hopeful", "sad"]),
]


def guess_category(track_id):
    lowered = track_id.lower()

    for category, keywords in CATEGORY_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            return category

    return "calm"


def title_from_track_id(track_id):
    parts = track_id.split("-")

    if parts and parts[-1].isdigit():
        parts = parts[:-1]

    if len(parts) > 1:
        title_parts = parts[1:]
    else:
        title_parts = parts

    title = " ".join(title_parts).replace("_", " ").strip()
    return title.title() if title else track_id


def artist_from_track_id(track_id):
    first = track_id.split("-")[0]
    return first.replace("_", " ").title()


def parse_attributions(text):
    data = {}
    current_id = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        match = re.match(r"^\d+\.\s*(.+)$", line)
        if match:
            current_id = match.group(1).strip()
            data.setdefault(current_id, {})
            continue

        if not current_id:
            continue

        artist_match = re.search(r">([^<]+)</a>\s+from\s+<a", line)
        links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', line)

        if artist_match:
            data[current_id]["artist"] = artist_match.group(1).strip()

        if links:
            data[current_id]["artist_url"] = links[0][0]
            if len(links) > 1:
                data[current_id]["source_url"] = links[1][0]
                data[current_id]["source_name"] = links[1][1].strip()

    return data


def import_ambient_music_from_path(source_path, replace=False, is_active=True):
    source = Path(source_path).expanduser().resolve()

    if not source.exists():
        raise FileNotFoundError(f"Path ne postoji: {source}")

    temp_dir = None

    if source.is_file():
        if source.suffix.lower() != ".zip":
            raise ValueError("Datoteka mora biti .zip")

        temp_dir = Path(tempfile.mkdtemp(prefix="ambient_music_import_"))

        with zipfile.ZipFile(source, "r") as archive:
            archive.extractall(temp_dir)

        scan_root = temp_dir
    else:
        scan_root = source

    try:
        attribution_text = ""

        for txt_path in scan_root.rglob("*.txt"):
            try:
                attribution_text += "\n" + txt_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                attribution_text += "\n" + txt_path.read_text(encoding="cp1250", errors="ignore")

        attributions = parse_attributions(attribution_text)

        audio_files = [
            path for path in scan_root.rglob("*")
            if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS
        ]

        created = 0
        updated = 0
        skipped = 0

        for index, audio_path in enumerate(sorted(audio_files), start=1):
            track_id = slugify(audio_path.stem)

            if not track_id:
                skipped += 1
                continue

            attribution = attributions.get(audio_path.stem, {}) or attributions.get(track_id, {})

            defaults = {
                "title": title_from_track_id(audio_path.stem),
                "category": guess_category(audio_path.stem),
                "description": "",
                "artist": attribution.get("artist") or artist_from_track_id(audio_path.stem),
                "artist_url": attribution.get("artist_url", ""),
                "source_name": attribution.get("source_name", "Pixabay"),
                "source_url": attribution.get("source_url", ""),
                "license_label": "Pixabay licenca",
                "is_active": is_active,
                "order": index,
            }

            track, was_created = AmbientMusicTrack.objects.get_or_create(
                track_id=track_id,
                defaults=defaults,
            )

            if was_created:
                with audio_path.open("rb") as handle:
                    track.audio_file.save(audio_path.name, File(handle), save=True)

                created += 1
                continue

            if replace:
                for field, value in defaults.items():
                    setattr(track, field, value)

                with audio_path.open("rb") as handle:
                    track.audio_file.save(audio_path.name, File(handle), save=False)

                track.save()
                updated += 1
            else:
                skipped += 1

        return {
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "total_audio_files": len(audio_files),
        }

    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)