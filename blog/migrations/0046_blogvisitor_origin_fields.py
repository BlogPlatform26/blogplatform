from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0045_blogvisitor'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogvisitor',
            name='city',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AddField(
            model_name='blogvisitor',
            name='country',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AddField(
            model_name='blogvisitor',
            name='country_code',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
    ]
