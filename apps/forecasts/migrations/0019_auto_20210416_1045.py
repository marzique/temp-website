# Generated by Django 3.2 on 2021-04-16 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0018_auto_20210202_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='season',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]