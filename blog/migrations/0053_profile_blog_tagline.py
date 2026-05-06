from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0052_alter_profile_template_misticno_jezero"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="blog_tagline",
            field=models.CharField(blank=True, default="", max_length=220),
        ),
    ]
