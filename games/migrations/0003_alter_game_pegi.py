# Generated by Django 5.1.5 on 2025-01-31 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_pegi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pegi',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Pegi3'), (7, 'Pegi7'), (12, 'Pegi12'), (16, 'Pegi16'), (18, 'Pegi18')]),
        ),
    ]
