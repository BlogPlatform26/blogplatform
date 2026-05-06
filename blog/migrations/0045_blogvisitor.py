from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_post_allow_comments_publish_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_token', models.CharField(max_length=64)),
                ('page_label', models.CharField(blank=True, default='blog', max_length=50)),
                ('path', models.CharField(blank=True, default='', max_length=255)),
                ('device_type', models.CharField(blank=True, default='Nepoznato', max_length=20)),
                ('user_agent', models.CharField(blank=True, default='', max_length=255)),
                ('browser_language', models.CharField(blank=True, default='', max_length=32)),
                ('timezone_name', models.CharField(blank=True, default='', max_length=64)),
                ('latitude', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('hit_count', models.PositiveIntegerField(default=0)),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('blog_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_visitors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='blogvisitor',
            index=models.Index(fields=['blog_owner', 'last_seen'], name='blog_blogvi_blog_ow_6bc38a_idx'),
        ),
        migrations.AddIndex(
            model_name='blogvisitor',
            index=models.Index(fields=['blog_owner', 'page_label'], name='blog_blogvi_blog_ow_2585a8_idx'),
        ),
        migrations.AddConstraint(
            model_name='blogvisitor',
            constraint=models.UniqueConstraint(fields=('blog_owner', 'visitor_token'), name='unique_blog_visitor_token'),
        ),
    ]
