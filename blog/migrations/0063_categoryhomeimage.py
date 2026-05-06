# Generated manually for BlogPlatform category home images

from django.db import migrations, models
import django.db.models.deletion
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0062_securityevent"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryHomeImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, default="", max_length=120)),
                ("image", models.ImageField(upload_to="category_home_images/", validators=[blog.models.validate_image_size])),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="home_images", to="blog.category")),
            ],
            options={
                "verbose_name": "Slika za kategoriju",
                "verbose_name_plural": "Slike za kategorije",
                "ordering": ["category__group", "category__name", "-created_at"],
            },
        ),
    ]
