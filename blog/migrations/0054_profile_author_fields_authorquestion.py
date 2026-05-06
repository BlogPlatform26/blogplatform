from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0053_profile_blog_tagline'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='allow_author_questions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_bio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_birth_place',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_education',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_favorite_topics',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_hobbies',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_interests',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_motto',
            field=models.CharField(blank=True, default='', max_length=220),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_nationality',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_occupation',
            field=models.CharField(blank=True, default='', max_length=180),
        ),
        migrations.AddField(
            model_name='profile',
            name='author_religion',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.CreateModel(
            name='AuthorQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField(blank=True, default='')),
                ('is_public', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answered_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_author_questions', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_author_questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
