# Generated by Django 3.1.6 on 2021-02-24 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0008_auto_20210225_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminfo',
            name='league',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='scoreboard.league'),
            preserve_default=False,
        ),
    ]
