# Generated by Django 3.1.2 on 2020-10-19 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('squad', '0003_auto_20201018_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='name_slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]
