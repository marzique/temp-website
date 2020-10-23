# Generated by Django 3.1.2 on 2020-10-23 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forecasts', '0004_auto_20201023_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Прийом ставок'), (2, 'Тур розпочався'), (3, 'Очки зараховані')], default=1),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='forecast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixtures', to='forecasts.forecast'),
        ),
    ]
