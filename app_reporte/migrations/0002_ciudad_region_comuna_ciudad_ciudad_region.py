# Generated by Django 5.1.3 on 2025-01-25 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reporte', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='ciudad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comunas', to='app_reporte.ciudad'),
        ),
        migrations.AddField(
            model_name='ciudad',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ciudades', to='app_reporte.region'),
        ),
    ]
