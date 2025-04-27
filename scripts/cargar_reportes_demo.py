from app_reporte.models import Reporte, Medida, OrganismoResponsable
from random import choice
from datetime import date, timedelta

estados = ['pendiente', 'aprobado', 'rechazado']
organismos = OrganismoResponsable.objects.all()
medidas = Medida.objects.all()

if not organismos.exists() or not medidas.exists():
    print("No hay organismos o medidas en la base de datos.")
else:
    print("Iniciando carga de reportes demo...")
    creados = 0
    for i in range(1, 21):
        try:
            Reporte.objects.create(
                medida=choice(medidas),
                organismo=choice(organismos),
                descripcion=f'Reporte de prueba {i}',
                estado=choice(estados),
                fecha_envio=date(2025, 4, 1) + timedelta(days=i)
            )
            creados += 1
        except Exception as e:
            print(f"⚠️ Error en reporte {i}: {e}")
    print(f"{creados} reportes creados correctamente.")

