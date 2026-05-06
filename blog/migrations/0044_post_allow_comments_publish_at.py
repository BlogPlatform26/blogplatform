from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0043_userrestriction"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="allow_comments",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="post",
            name="publish_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[
                    ("published", "Objavljen"),
                    ("draft", "Skica"),
                    ("scheduled", "Na čekanju"),
                    ("deleted", "Obrisan"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
    ]
