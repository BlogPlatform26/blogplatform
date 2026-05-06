from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0050_profile_soho_hero_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="template",
            field=models.CharField(
                choices=[
                    ("default", "Default"),
                    ("dark", "Dark"),
                    ("classic", "Classic"),
                    ("default_right", "Default Plus"),
                    ("dark_right", "Dark Plus"),
                    ("classic_right", "Classic Plus"),
                    ("simple_pattern", "Simple Uzorak"),
                    ("simple_image", "Simple Slika"),
                    ("soho", "Studio"),
                    ("litica_noci", "Litica u noći"),
                    ("podvodna_tisina", "Podvodna tišina"),
                    ("vodopad_u_magli", "Vodopad u magli"),
                    ("planine_u_magli", "Planine u magli"),
                    ("nebeski_mir", "Nebeski mir"),
                    ("svemirski_horizont", "Svemirski horizont"),
                    ("zlatni_horizont", "Zlatni horizont"),
                    ("iznad_oblaka", "Iznad oblaka"),
                    ("sumska_svjetlost", "Šumska svjetlost"),
                    ("polarna_svjetlost", "Polarna svjetlost"),
                    ("zlatno_polje", "Zlatno polje"),
                    ("neonski_grad", "Neonski grad"),
                    ("polje_lavande", "Polje lavande"),
                    ("nebesko_polje", "Nebesko polje"),
                ],
                default="default",
                max_length=50,
            ),
        ),
    ]
