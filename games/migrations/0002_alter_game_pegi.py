# Generated by Django 5.1.5 on 2025-01-31 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pegi',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Pegi 3'), (7, 'Pegi 7'), (12, 'Pegi 12'), (16, 'Pegi 16'), (18, 'Pegi 18')]),
        ),
    ]
