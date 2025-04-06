# Generated by Django 5.1.5 on 2025-04-06 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reporte', '0004_alter_planppda_mes_reporte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporte',
            name='archivo_url',
        ),
        migrations.RemoveField(
            model_name='reporte',
            name='estado',
        ),
        migrations.AddField(
            model_name='reporte',
            name='archivo',
            field=models.FileField(blank=True, help_text='Archivo subido (pdf, imagen, documento, etc)', null=True, upload_to='reportes/'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='fecha_envio',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='app_reporte.medida'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='medio_verificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportes', to='app_reporte.medioverificacion'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='organismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportes', to='app_reporte.organismoresponsable'),
        ),
    ]
