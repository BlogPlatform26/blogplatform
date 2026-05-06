from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0048_profile_simple_background_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='template',
            field=models.CharField(
                max_length=50,
                default='default',
                choices=[
                    ('default', 'Default'),
                    ('dark', 'Dark'),
                    ('classic', 'Classic'),
                    ('default_right', 'Default Plus'),
                    ('dark_right', 'Dark Plus'),
                    ('classic_right', 'Classic Plus'),
                    ('simple_pattern', 'Simple Uzorak'),
                    ('simple_image', 'Simple Slika'),
                ],
            ),
        ),
    ]
