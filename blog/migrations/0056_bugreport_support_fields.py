from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0055_profile_author_extra_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugreport',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='bugreport',
            name='page_url',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='bugreport',
            name='request_type',
            field=models.CharField(choices=[('bug', 'Kvar'), ('question', 'Pitanje'), ('idea', 'Prijedlog')], default='bug', max_length=20),
        ),
        migrations.AddField(
            model_name='bugreport',
            name='topic',
            field=models.CharField(choices=[('publishing', 'Objavljivanje postova'), ('design', 'Dizajn bloga'), ('profile', 'Profil i račun'), ('comments', 'Komentari i lajkovi'), ('boxes', 'Boxevi i sidebar'), ('author', 'Upoznaj autora'), ('other', 'Ostalo')], default='other', max_length=30),
        ),
        migrations.AlterModelOptions(
            name='bugreport',
            options={'ordering': ['-created_at']},
        ),
    ]
