# app_reporte/migrations/0012_add_reporte_unique_constraint.py

from django.db import migrations, models

def eliminar_reportes_duplicados(apps, schema_editor):
    """
    Elimina los reportes duplicados (mismo medida, organismo y fecha_envio),
    dejando solo el de menor id.
    """
    Reporte = apps.get_model('app_reporte', 'Reporte')
    # agrupamos y obtenemos los ids a conservar
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT MIN(id) AS id_to_keep, medida_id, organismo_id, fecha_envio
            FROM app_reporte_reporte
            GROUP BY medida_id, organismo_id, fecha_envio
            HAVING COUNT(*) > 1
        """)
        grupos = cursor.fetchall()
    # para cada grupo, borramos los que no sean el id_to_keep
    for id_to_keep, medida_id, organismo_id, fecha_envio in grupos:
        Reporte.objects.filter(
            medida_id=medida_id,
            organismo_id=organismo_id,
            fecha_envio=fecha_envio
        ).exclude(id=id_to_keep).delete()

class Migration(migrations.Migration):
    # ejecutar sin transaccion unica
    atomic = False

    dependencies = [
        ('app_reporte', '0011_add_audit_fields'),
    ]

    operations = [
        # 1) eliminamos duplicados para que no falle la creacion del indice unico
        migrations.RunPython(eliminar_reportes_duplicados, reverse_code=migrations.RunPython.noop),
        # 2) forzamos que no queden chequeos deferidos
        migrations.RunSQL("SET CONSTRAINTS ALL IMMEDIATE;"),
        # 3) añadimos la constraint unica
        migrations.AddConstraint(
            model_name='reporte',
            constraint=models.UniqueConstraint(
                fields=['medida', 'organismo', 'fecha_envio'],
                name='unique_reporte_medida_organismo_fecha'
            ),
        ),
    ]
