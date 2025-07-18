# Generated by Django 5.1.6 on 2025-03-22 11:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_start', models.CharField(max_length=255, verbose_name='route_start')),
                ('route_end', models.CharField(max_length=255, verbose_name='route_end')),
                ('route_url', models.CharField(max_length=255, unique=True, verbose_name='route_url')),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='routes/')),
                ('route_distance', models.FloatField(blank=True, null=True, verbose_name='distance')),
                ('route_duration', models.FloatField(blank=True, null=True, verbose_name='duration')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('owners', models.ManyToManyField(related_name='routes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RouteFares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fare_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='fare_title')),
                ('fare', models.FloatField(blank=True, null=True, verbose_name='fare')),
                ('student_fare', models.FloatField(blank=True, null=True, verbose_name='student_fare')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.routes', verbose_name='route')),
            ],
        ),
        migrations.CreateModel(
            name='RouteSchedules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='start_time')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.routes', verbose_name='route')),
            ],
        ),
    ]
