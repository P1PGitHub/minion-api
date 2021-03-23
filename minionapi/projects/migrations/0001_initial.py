# Generated by Django 2.2.15 on 2021-03-23 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0009_team_stale_report_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True)),
                ('index', models.SmallIntegerField(default=-1)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', related_query_name='member', to='projects.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', related_query_name='member', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.PositiveIntegerField(verbose_name='Client ID')),
                ('client_name', models.CharField(max_length=255)),
                ('primary', models.BooleanField(default=False)),
                ('contact_name', models.CharField(blank=True, max_length=255)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=24)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', related_query_name='client', to='projects.Project')),
            ],
        ),
    ]
