# Generated by Django 2.2.15 on 2021-03-24 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20210324_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='parent_task',
        ),
    ]
