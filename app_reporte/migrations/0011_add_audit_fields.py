# app_reporte/migrations/0011_add_audit_fields.py
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from django.utils.timezone import now

class Migration(migrations.Migration):
    dependencies = [
        ('app_reporte', '0010_alter_ciudad_region_alter_comuna_ciudad_and_more'),
    ]
    operations = [
        # Campos en Reporte
        migrations.AddField(
            model_name='reporte',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporte',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reporte',
            name='created_by',
            field=models.ForeignKey(
                related_name='reporte_created',
                null=True, blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='reporte',
            name='updated_by',
            field=models.ForeignKey(
                related_name='reporte_updated',
                null=True, blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL
            ),
        ),
        # Campos en HistorialEstadoReporte
        migrations.AddField(
            model_name='historialestadoreporte',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialestadoreporte',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historialestadoreporte',
            name='created_by',
            field=models.ForeignKey(
                related_name='historialestadoreporte_created',
                null=True, blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='historialestadoreporte',
            name='updated_by',
            field=models.ForeignKey(
                related_name='historialestadoreporte_updated',
                null=True, blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
