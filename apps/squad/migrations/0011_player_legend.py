# Generated by Django 3.1.2 on 2020-10-22 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squad', '0010_auto_20201021_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='legend',
            field=models.BooleanField(default=False),
        ),
    ]
