# Generated by Django 3.1.2 on 2020-10-23 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='guest_logo',
            field=models.ImageField(blank=True, upload_to='fixtures/'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='guest_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='home_logo',
            field=models.ImageField(blank=True, upload_to='fixtures/'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='home_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
