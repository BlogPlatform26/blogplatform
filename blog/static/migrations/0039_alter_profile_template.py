from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0038_alter_profile_template"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="template",
            field=models.CharField(
                choices=[
                    ("default", "Default"),
                    ("dark", "Dark stil"),
                    ("classic", "Classic stil"),
                ],
                default="default",
                max_length=50,
            ),
        ),
    ]
