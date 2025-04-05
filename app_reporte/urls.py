from django.urls import path
from .views import PlanPPDAView, ComunaView, RegionView, CiudadView, OrganismoResponsableView, OrganismosResponsablesView, ReportesView, ReporteView

urlpatterns = [
    path('planes/', PlanPPDAView.as_view(), name='planes'),
    path('comunas/', ComunaView.as_view(), name='comunas'),
    path('regiones/', RegionView.as_view(), name='regiones'),
    path('ciudades/', CiudadView.as_view(), name='ciudades'),
    path('organismo-responsable/<int:id_orgres>', OrganismoResponsableView.as_view(http_method_names=['get', 'put', 'delete']), name='organismo-responsable'),
    path('organismo-responsable/', OrganismoResponsableView.as_view(http_method_names=['post']), name='organismo-responsable'),
    path('organismos-responsables/', OrganismosResponsablesView.as_view(), name='organismos-responsables'),
    path('reportes/', ReportesView.as_view(), name='reportes'),
    path('reporte/', ReporteView.as_view(http_method_names=['post']), name='reporte_create'),
    path('reporte/<int:id_reporte>', ReporteView.as_view(http_method_names=['get', 'put', 'delete']), name='reporte_detail'),
]

