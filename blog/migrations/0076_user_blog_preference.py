import logging
import re

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


logger = logging.getLogger(__name__)
NUMERIC_LEGACY_KEY = re.compile(r"^[0-9]+$")


def backfill_numeric_user_preferences(apps, schema_editor):
    User = apps.get_model("auth", "User")
    BlogDesignPreference = apps.get_model("blog", "BlogDesignPreference")
    UserBlogPreference = apps.get_model("blog", "UserBlogPreference")

    counts = {
        "migrated": 0,
        "non_numeric": 0,
        "orphan_numeric": 0,
        "invalid_data": 0,
        "existing_target": 0,
    }

    for legacy in BlogDesignPreference.objects.all().iterator():
        legacy_key = str(legacy.template or "")

        if not NUMERIC_LEGACY_KEY.fullmatch(legacy_key):
            counts["non_numeric"] += 1
            continue

        user_id = int(legacy_key)
        if not User.objects.filter(pk=user_id).exists():
            counts["orphan_numeric"] += 1
            continue

        if not isinstance(legacy.data, dict):
            counts["invalid_data"] += 1
            continue

        _, created = UserBlogPreference.objects.get_or_create(
            user_id=user_id,
            defaults={"data": legacy.data},
        )
        if created:
            counts["migrated"] += 1
        else:
            counts["existing_target"] += 1

    logger.warning(
        "UserBlogPreference legacy backfill: migrated=%d, non_numeric=%d, "
        "orphan_numeric=%d, invalid_data=%d, existing_target=%d",
        counts["migrated"],
        counts["non_numeric"],
        counts["orphan_numeric"],
        counts["invalid_data"],
        counts["existing_target"],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0075_alter_comment_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserBlogPreference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blog_preferences",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Korisničke postavke bloga",
                "verbose_name_plural": "Korisničke postavke blogova",
            },
        ),
        migrations.RunPython(
            backfill_numeric_user_preferences,
            migrations.RunPython.noop,
        ),
    ]
