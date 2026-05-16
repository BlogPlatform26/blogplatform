import os
from pathlib import Path

from PIL import Image, ImageOps


DEFAULT_MAX_WIDTH = int(os.environ.get("IMAGE_OPTIMIZE_MAX_WIDTH", 1600))
DEFAULT_MAX_HEIGHT = int(os.environ.get("IMAGE_OPTIMIZE_MAX_HEIGHT", 1600))
DEFAULT_QUALITY = int(os.environ.get("IMAGE_OPTIMIZE_QUALITY", 82))

SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def optimize_image_path(path, max_width=None, max_height=None, quality=None):
    """
    Smanjuje i komprimira uploadane slike na disku.
    Ne dira bazu i ne mijenja naziv datoteke.
    """
    path = Path(path)

    if not path.exists() or not path.is_file():
        return False

    max_width = _safe_int(max_width, DEFAULT_MAX_WIDTH)
    max_height = _safe_int(max_height, DEFAULT_MAX_HEIGHT)
    quality = _safe_int(quality, DEFAULT_QUALITY)

    try:
        with Image.open(path) as img:
            if getattr(img, "is_animated", False):
                return False

            image_format = (img.format or "").upper()
            if image_format not in SUPPORTED_FORMATS:
                return False

            img = ImageOps.exif_transpose(img)

            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            save_kwargs = {}

            if image_format == "JPEG":
                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")
                save_kwargs.update({
                    "format": "JPEG",
                    "quality": quality,
                    "optimize": True,
                    "progressive": True,
                })

            elif image_format == "PNG":
                save_kwargs.update({
                    "format": "PNG",
                    "optimize": True,
                })

            elif image_format == "WEBP":
                save_kwargs.update({
                    "format": "WEBP",
                    "quality": quality,
                    "method": 6,
                })

            img.save(path, **save_kwargs)
            return True

    except Exception:
        # Ne rušimo spremanje posta/profila ako optimizacija slike ne uspije.
        return False


def optimize_image_field(instance, field_name, max_width=None, max_height=None, quality=None):
    """
    Optimizira ImageField nakon što je model spremljen.
    Radi za lokalne datoteke koje imaju .path.
    """
    image_field = getattr(instance, field_name, None)

    if not image_field:
        return False

    try:
        image_path = image_field.path
    except (NotImplementedError, ValueError, AttributeError):
        return False

    return optimize_image_path(
        image_path,
        max_width=max_width,
        max_height=max_height,
        quality=quality,
    )
