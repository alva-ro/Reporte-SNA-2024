# Generated by Django 5.1.5 on 2025-04-15 00:38

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reporte', '0009_add_plan_to_medida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ciudades', to='app_reporte.region'),
        ),
        migrations.AlterField(
            model_name='comuna',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comunas', to='app_reporte.ciudad'),
        ),
        migrations.AlterField(
            model_name='medida',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medidas', to='app_reporte.planppda'),
        ),
        migrations.AlterField(
            model_name='medioverificacion',
            name='entidad_a_cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='medios_verificacion', to='app_reporte.entidad'),
        ),
        migrations.AlterField(
            model_name='medioverificacion',
            name='medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medios_verificacion', to='app_reporte.medida'),
        ),
        migrations.AlterField(
            model_name='planppda',
            name='mes_reporte',
            field=models.IntegerField(help_text='Ingrese un valor', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='medida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reportes', to='app_reporte.medida'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='medio_verificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reportes', to='app_reporte.medioverificacion'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='organismo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reportes', to='app_reporte.organismoresponsable'),
        ),
        migrations.AddConstraint(
            model_name='planppda',
            constraint=models.UniqueConstraint(fields=('nombre', 'anio', 'mes_reporte'), name='unique_plan_nombre_anio_mes'),
        ),
    ]
