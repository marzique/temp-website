# Generated by Django 3.1.2 on 2020-10-26 17:22

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201023_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
