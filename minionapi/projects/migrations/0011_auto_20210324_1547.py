# Generated by Django 2.2.15 on 2021-03-24 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20210324_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['active', '-created_at']},
        ),
    ]
