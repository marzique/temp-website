# Generated by Django 3.1.2 on 2020-10-23 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='blog.blog'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='posted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
