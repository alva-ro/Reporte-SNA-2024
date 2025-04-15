from django.db import migrations, models
import django.db.models.deletion

def asignar_plan_por_defecto(apps, schema_editor):
    Medida = apps.get_model('app_reporte', 'Medida')
    PlanPPDA = apps.get_model('app_reporte', 'PlanPPDA')
    
    # Obtener el primer plan PPDA
    plan_default = PlanPPDA.objects.first()
    if plan_default:
        # Asignar el plan por defecto a todas las medidas existentes
        Medida.objects.filter(plan__isnull=True).update(plan=plan_default)

class Migration(migrations.Migration):

    dependencies = [
        ('app_reporte', '0008_remove_historialestadoreporte_fecha_cambio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medida',
            name='plan',
            field=models.ForeignKey(
                null=True,  # Permitimos null temporalmente para la migración
                on_delete=django.db.models.deletion.CASCADE,
                related_name='medidas',
                to='app_reporte.planppda'
            ),
        ),
        migrations.RunPython(asignar_plan_por_defecto),
        migrations.AlterField(
            model_name='medida',
            name='plan',
            field=models.ForeignKey(
                null=False,  # Después de la migración, no permitimos null
                on_delete=django.db.models.deletion.CASCADE,
                related_name='medidas',
                to='app_reporte.planppda'
            ),
        ),
    ] 