from django.db import migrations, models
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0047_alter_profile_template_simple'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='simple_background_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='design_backgrounds/custom/',
                validators=[blog.models.validate_image_size],
            ),
        ),
    ]
