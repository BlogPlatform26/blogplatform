from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_userblock'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialDayEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('is_active', models.BooleanField(default=True)),
                ('priority', models.PositiveIntegerField(default=100)),
                ('position', models.CharField(choices=[('top', 'Iznad postova'), ('left', 'Lijevo'), ('right', 'Desno')], default='top', max_length=10)),
                ('theme', models.CharField(choices=[('general', 'Općenito'), ('romance', 'Valentinovo / romantika'), ('womens_day', 'Dan žena'), ('spring', 'Proljeće'), ('earth', 'Dan planeta Zemlje'), ('books', 'Dan knjige'), ('summer', 'Ljeto'), ('autumn', 'Jesen'), ('bread', 'Dani kruha'), ('advent', 'Advent'), ('christmas', 'Božić'), ('easter', 'Uskrs'), ('new_year', 'Nova godina')], default='general', max_length=20)),
                ('date_type', models.CharField(choices=[('fixed', 'Fiksni datum'), ('range', 'Raspon datuma'), ('nth_weekday', 'N-ti dan u mjesecu'), ('easter', 'Uskrs'), ('advent', 'Advent')], default='fixed', max_length=20)),
                ('month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('nth_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('nth_week', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Prvi'), (2, 'Drugi'), (3, 'Treći'), (4, 'Četvrti'), (5, 'Zadnji')], null=True)),
                ('nth_weekday', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Ponedjeljak'), (1, 'Utorak'), (2, 'Srijeda'), (3, 'Četvrtak'), (4, 'Petak'), (5, 'Subota'), (6, 'Nedjelja')], null=True)),
                ('accent_label', models.CharField(blank=True, default='', max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['priority', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SpecialDayMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=160)),
                ('body', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='blog.specialdayevent')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SpecialDaySelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to='blog.specialdayevent')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to='blog.specialdaymessage')),
            ],
            options={
                'ordering': ['-selection_date', '-id'],
                'unique_together': {('event', 'selection_date')},
            },
        ),
    ]
