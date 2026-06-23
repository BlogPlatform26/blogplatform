# Generated manually for BlogPlatform design preferences DB storage

import json
from pathlib import Path

from django.conf import settings
from django.db import migrations, models


def import_existing_blog_preferences(apps, schema_editor):
    BlogDesignPreference = apps.get_model("blog", "BlogDesignPreference")

    path = Path(settings.BASE_DIR) / "blog" / "blog_preferences.json"

    if not path.exists():
        return

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return

    if not isinstance(raw, dict):
        return

    for template, data in raw.items():
        if not isinstance(template, str):
            continue

        if not isinstance(data, dict):
            continue

        BlogDesignPreference.objects.update_or_create(
            template=template,
            defaults={"data": data},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0073_accountstatus"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogDesignPreference",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("template", models.CharField(max_length=80, unique=True)),
                ("data", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Postavke dizajna bloga",
                "verbose_name_plural": "Postavke dizajna blogova",
            },
        ),
        migrations.RunPython(import_existing_blog_preferences, migrations.RunPython.noop),
    ]
