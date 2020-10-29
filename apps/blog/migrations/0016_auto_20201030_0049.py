# Generated by Django 3.1.2 on 2020-10-29 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20201029_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='forecast',
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='blog.blog'),
        ),
    ]
