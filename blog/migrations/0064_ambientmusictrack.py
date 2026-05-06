# Generated manually for BlogPlatform ambient music admin upload.

from django.db import migrations, models
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0063_categoryhomeimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="AmbientMusicTrack",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("category", models.CharField(choices=[
                    ("calm", "Mirno i opuštajuće"),
                    ("romantic", "Nježno i romantično"),
                    ("jazz", "Jazz i lounge"),
                    ("fantasy", "Čarobno i fantasy"),
                    ("mystery", "Tajanstveno i napeto"),
                    ("cinematic", "Putovanje i filmski ugođaj"),
                    ("fun", "Veselo i posebno"),
                    ("other", "Ostalo"),
                ], default="other", max_length=30)),
                ("description", models.CharField(blank=True, max_length=300)),
                ("artist", models.CharField(blank=True, default="BlogPlatform", max_length=120)),
                ("audio_file", models.FileField(upload_to="ambient_music/", validators=[
                    blog.models.validate_audio_size,
                    blog.models.validate_audio_extension,
                ])),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Pozadinska glazba",
                "verbose_name_plural": "Pozadinska glazba",
                "ordering": ["category", "title"],
            },
        ),
    ]
