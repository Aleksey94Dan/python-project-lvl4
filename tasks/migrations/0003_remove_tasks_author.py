# Generated by Django 3.2 on 2021-05-23 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210523_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='author',
        ),
    ]