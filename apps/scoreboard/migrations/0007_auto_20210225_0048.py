# Generated by Django 3.1.6 on 2021-02-24 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0006_league_teaminfo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='league',
            unique_together={('name', 'years')},
        ),
    ]
