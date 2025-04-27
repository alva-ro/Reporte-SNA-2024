from django.urls import path
from .views import PlanPPDAView, ComunaView, RegionView, CiudadView, OrganismoResponsableView, RegionDetailView, \
      CiudadDetailView, ComunaDetailView, OrganismoResponsableDetailView, PlanPPDADetailView, ReporteEstadoUpdateView, ReporteListView, \
      ReportesView, ReporteView, MedidaView, MedidaDetailView

urlpatterns = [
    path('planes/', PlanPPDAView.as_view(http_method_names=['post', 'get']), name='planes'),
    path('medidas/<int:pk>/', MedidaDetailView.as_view(http_method_names=['get', 'put', 'delete']), name='medidas'),
    path('medidas/', MedidaView.as_view(http_method_names=['post', 'get']), name='medidas'),
    path('planes/<int:pk>/', PlanPPDADetailView.as_view(http_method_names=['get', 'put', 'delete']), name='planes'),
    path('comunas/', ComunaView.as_view(http_method_names=['post', 'get']), name='comunas'),
    path('comunas/<int:pk>/', ComunaDetailView.as_view(http_method_names=['get', 'put', 'delete']), name='comunas'),
    path('regiones/', RegionView.as_view(http_method_names=['post', 'get']), name='regiones'),
    path('regiones/<int:pk>/', RegionDetailView.as_view(http_method_names=['get', 'put', 'delete']), name='regiones-detail'),
    path('ciudades/', CiudadView.as_view(http_method_names=['post', 'get']), name='ciudades'),
    path('ciudades/<int:pk>/', CiudadDetailView.as_view(http_method_names=['get', 'put', 'delete']), name='ciudades'),
    path('organismo-responsable/<int:pk>/', OrganismoResponsableDetailView.as_view(http_method_names=['get', 'put', 'delete']), name='organismo-responsable'),
    path('organismo-responsable/', OrganismoResponsableView.as_view(http_method_names=['post', 'get']), name='organismo-responsable'),
    path('reportes/', ReporteListView.as_view(), name='reportes'),  # ← Usamos este
    path('reportes/<int:id_reporte>/estado/', ReporteEstadoUpdateView.as_view(), name='actualizar-estado-reporte'),    
    path('reporte/', ReporteView.as_view(http_method_names=['post']), name='reporte_create'),
    path('reporte/<int:id_reporte>', ReporteView.as_view(http_method_names=['get', 'put', 'delete']), name='reporte_detail'),
]
