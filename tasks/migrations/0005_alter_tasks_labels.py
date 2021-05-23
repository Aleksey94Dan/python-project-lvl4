# Generated by Django 3.2 on 2021-05-23 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0004_alter_tasks_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='labels',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='labels', to='labels.labels'),
        ),
    ]
