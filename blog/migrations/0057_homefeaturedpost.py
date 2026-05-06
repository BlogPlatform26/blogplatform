from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0056_bugreport_support_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeFeaturedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('algorithm', 'Algoritam'), ('premium', 'Premium')], default='algorithm', max_length=12)),
                ('featured_at', models.DateTimeField()),
                ('slot_date', models.DateField(blank=True, null=True)),
                ('slot_name', models.CharField(blank=True, choices=[('morning', 'Jutro'), ('afternoon', 'Popodne'), ('evening', 'Večer')], max_length=12)),
                ('slot_token', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('raw_score', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home_featured_entries', to='blog.post')),
            ],
            options={
                'ordering': ['-featured_at', '-created_at'],
                'indexes': [models.Index(fields=['source', '-featured_at'], name='blog_homefe_source_a27bd6_idx'), models.Index(fields=['slot_date', 'slot_name'], name='blog_homefe_slot_da_b1aa15_idx')],
            },
        ),
    ]
