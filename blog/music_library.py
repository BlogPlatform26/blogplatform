# Ambient music library now reads tracks from database/admin.

AMBIENT_MUSIC_CATEGORIES = [
    {
        "value": "calm",
        "label": "Mirno i opustajuce",
        "description": "Tise i laganije melodije za citanje.",
    },
    {
        "value": "romantic",
        "label": "Njezno i romanticno",
        "description": "Toplije, emotivne i mekse melodije.",
    },
    {
        "value": "jazz",
        "label": "Jazz i lounge",
        "description": "Lagani jazz, lounge i vecernja atmosfera.",
    },
    {
        "value": "fantasy",
        "label": "Carobno i fantasy",
        "description": "Bajkovita, misticna i carobna glazba.",
    },
    {
        "value": "mystery",
        "label": "Tajanstveno i napeto",
        "description": "Mracnije i napetije melodije.",
    },
    {
        "value": "cinematic",
        "label": "Putovanje i filmski ugodaj",
        "description": "Siri, putopisni ili dokumentarni ton.",
    },
    {
        "value": "fun",
        "label": "Veselo i posebno",
        "description": "Razigrane, tematske i posebne melodije.",
    },
]


def get_ambient_music_categories():
    return [dict(item) for item in AMBIENT_MUSIC_CATEGORIES]


def _track_queryset():
    from blog.models import AmbientMusicTrack

    return (
        AmbientMusicTrack.objects
        .filter(is_active=True)
        .exclude(audio_file="")
        .order_by("category", "order", "title")
    )


def get_ambient_music_tracks():
    try:
        return [track.as_library_item() for track in _track_queryset()]
    except Exception:
        return []


def get_ambient_music_track(track_id):
    track_id = str(track_id or "").strip()
    if not track_id:
        return None

    try:
        track = _track_queryset().filter(track_id=track_id).first()
    except Exception:
        return None

    return track.as_library_item() if track else None
