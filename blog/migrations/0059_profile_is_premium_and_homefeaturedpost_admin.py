from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0058_rename_blog_blogvi_blog_ow_6bc38a_idx_blog_blogvi_blog_ow_8cd797_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='homefeaturedpost',
            name='source',
            field=models.CharField(
                choices=[('algorithm', 'Algoritam'), ('premium', 'Premium'), ('admin', 'Admin')],
                default='algorithm',
                max_length=12,
            ),
        ),
    ]
