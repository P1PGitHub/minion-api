# Generated by Django 2.2.15 on 2020-09-17 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_report_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerservice',
            name='followup',
            field=models.TextField(blank=True, null=True),
        ),
    ]
