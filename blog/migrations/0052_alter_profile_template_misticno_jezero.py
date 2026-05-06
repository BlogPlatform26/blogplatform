from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0051_alter_profile_template_morski_prijelaz"),
        ("blog", "0051_alter_profile_template_nebesko_polje"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="template",
            field=models.CharField(
                max_length=50,
                default="default",
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
                    ("magazin", "Magazin"),
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
                    ("carobna_ljubicasta", "Čarobni sumrak"),
                    ("kraljevska_pozornica", "Kraljevska pozornica"),
                    ("dimni_akordi", "Dimni akordi"),
                    ("nebeska_klasika", "Nebeska klasika"),
                    ("ponocna_elegancija", "Ponoćna elegancija"),
                    ("ruzicasti_vrt", "Ružičasti vrt"),
                    ("stara_aleja", "Stara aleja"),
                    ("staza_prema_vrhovima", "Staza prema vrhovima"),
                    ("jedro_u_suton", "Jedro u suton"),
                    ("sjene_ulice", "Sjene ulice"),
                    ("mjesecev_ples", "Mjesečev ples"),
                    ("misticno_jezero", "Mistično jezero"),
                    ("asfaltni_plamen", "Asfaltni plamen"),
                ],
            ),
        ),
    ]
