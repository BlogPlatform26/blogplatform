from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0054_profile_author_fields_authorquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='author_contact',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_full_name',
            field=models.CharField(blank=True, default='', max_length=180),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_inspiration',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_languages',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_nickname',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_social_links',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_website',
            field=models.CharField(blank=True, default='', max_length=320),
        ),
    ]
