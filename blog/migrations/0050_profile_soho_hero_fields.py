from django.db import migrations, models
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0049_alter_profile_template_simple_designs"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="soho_hero_image",
            field=models.ImageField(blank=True, null=True, upload_to="blog_hero_images/", validators=[blog.models.validate_image_size]),
        ),
        migrations.AddField(
            model_name="profile",
            name="soho_hero_preset",
            field=models.CharField(blank=True, choices=[("", "Bez sistemske slike"), ("bookshelf", "Police s knjigama"), ("cute_pets_flower", "Pas i mačka"), ("abstract_earth", "Apstraktni tonovi"), ("blue_tech", "Plava tehnologija"), ("dreamy_sunset", "Zamagljeni zalazak"), ("misty_mountains", "Maglovite planine"), ("night_camp", "Noćno kampiranje"), ("navy_coffee", "Kava i bilježnica"), ("watercolor_workspace", "Kreativni stol")], default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="profile",
            name="template",
            field=models.CharField(choices=[("default", "Default"), ("dark", "Dark"), ("classic", "Classic"), ("default_right", "Default Plus"), ("dark_right", "Dark Plus"), ("classic_right", "Classic Plus"), ("simple_pattern", "Simple Uzorak"), ("simple_image", "Simple Slika"), ("soho", "Soho")], default="default", max_length=50),
        ),
    ]
