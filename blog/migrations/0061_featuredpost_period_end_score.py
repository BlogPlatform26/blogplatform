# Generated manually to align FeaturedPost with update_rankings command.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0060_profile_premium_until"),
    ]

    operations = [
        migrations.AddField(
            model_name="featuredpost",
            name="period_end",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="featuredpost",
            name="score",
            field=models.FloatField(default=0.0),
        ),
    ]
