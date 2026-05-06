from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0046_blogvisitor_origin_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='template',
            field=models.CharField(
                choices=[
                    ('default', 'Default'),
                    ('dark', 'Dark'),
                    ('classic', 'Classic'),
                    ('simple', 'Simple'),
                    ('default_right', 'Default Plus'),
                    ('dark_right', 'Dark Plus'),
                    ('classic_right', 'Classic Plus'),
                ],
                default='default',
                max_length=50,
            ),
        ),
    ]
