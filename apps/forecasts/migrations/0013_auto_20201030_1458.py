# Generated by Django 3.1.2 on 2020-10-30 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0012_auto_20201029_0007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forecast',
            options={'ordering': ['-id']},
        ),
    ]