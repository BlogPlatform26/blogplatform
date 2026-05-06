from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0059_profile_is_premium_and_homefeaturedpost_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='premium_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
