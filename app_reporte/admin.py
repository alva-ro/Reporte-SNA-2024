from django.contrib import admin


# Register your models here.
from .models import PlanPPDA,Region,Ciudad,Comuna,OrganismoResponsable,Medida,MedioVerificacion,Reporte

# Register your models here.
admin.site.register(PlanPPDA)
admin.site.register(Region)
admin.site.register(Ciudad)
admin.site.register(Comuna)
admin.site.register(OrganismoResponsable)
admin.site.register(Medida)
admin.site.register(MedioVerificacion)
admin.site.register(Reporte)
from django.contrib import admin
from .models import HistorialEstadoReporte

@admin.register(HistorialEstadoReporte)
class HistorialEstadoReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte', 'estado_anterior', 'estado_nuevo', 'actualizado_por', 'fecha')
    list_filter = ('estado_nuevo', 'fecha')
    search_fields = ('reporte__id', 'actualizado_por')
