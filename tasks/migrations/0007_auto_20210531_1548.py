# Generated by Django 3.2 on 2021-05-31 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0006_auto_20210531_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='labels',
        ),
        migrations.AddField(
            model_name='tasks',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.Labels'),
        ),
    ]
