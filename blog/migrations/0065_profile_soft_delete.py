from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0064_ambientmusictrack"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="profile",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="anonymize_after",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="anonymized_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
