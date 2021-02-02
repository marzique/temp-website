# Generated by Django 3.1.6 on 2021-02-02 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0016_season_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecasts', to='forecasts.season'),
        ),
        migrations.AlterField(
            model_name='season',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]