# Generated by Django 3.2.5 on 2021-11-29 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0012_teaminfo_medal'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='rounds',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AddField(
            model_name='teaminfo',
            name='abandoned',
            field=models.BooleanField(default=False),
        ),
    ]
