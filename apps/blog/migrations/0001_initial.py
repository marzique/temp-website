# Generated by Django 3.1.2 on 2020-10-22 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to='blogs/')),
                ('created', models.DateTimeField(auto_now=True)),
                ('posted', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
