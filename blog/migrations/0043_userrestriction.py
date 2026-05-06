from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0042_remove_profile_allow_anonymous_comments_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRestriction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="restricted_users", to=settings.AUTH_USER_MODEL)),
                ("restricted", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="restricted_by_users", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("owner", "restricted")},
            },
        ),
    ]
