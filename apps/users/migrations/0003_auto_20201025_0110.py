# Generated by Django 3.1.2 on 2020-10-24 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201024_2147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='week_points',
            new_name='forecasts_points',
        ),
    ]
