from django.contrib import admin


# Register your models here.
from .models import PlanPPDA,Region,Ciudad,Comuna,OrganismoResponsable,Medida,MedioVerificacion,ReporteAnual


# Register your models here.
admin.site.register(PlanPPDA)
admin.site.register(Region)
admin.site.register(Ciudad)
admin.site.register(Comuna)
admin.site.register(OrganismoResponsable)
admin.site.register(Medida)
admin.site.register(MedioVerificacion)
admin.site.register(ReporteAnual)
