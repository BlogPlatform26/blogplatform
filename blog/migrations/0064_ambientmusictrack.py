# Ova migracija je namjerno prazna.
# Stari 0064_ambientmusictrack.py je pucao jer je tražio validate_audio_size.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0063_categoryhomeimage"),
    ]

    operations = []
