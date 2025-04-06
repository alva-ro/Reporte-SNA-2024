from django.urls import path
from .views import PlanPPDAView, ComunaView, RegionView, CiudadView, OrganismoResponsableView, OrganismosResponsablesView
from . import views


urlpatterns = [
    path('planes/', PlanPPDAView.as_view(), name='planes'),
    path('comunas/', ComunaView.as_view(), name='comunas'),
    path('regiones/', RegionView.as_view(), name='regiones'),
    path('ciudades/', CiudadView.as_view(), name='ciudades'),
    path('organismo-responsable/<int:id_orgres>', OrganismoResponsableView.as_view(http_method_names=['get', 'put', 'delete']), name='organismo-responsable'),
    path('organismo-responsable/', OrganismoResponsableView.as_view(http_method_names=['post']), name='organismo-responsable'),
    path('organismos-responsables/', OrganismosResponsablesView.as_view(), name='organismos-responsables'),
    path('api/reporteanual/', views.ReporteAnualList.as_view(), name='reporteanual_list'),
    path('api/reporteanual/<int:pk>/', views.ReporteAnualDetail.as_view(), name='reporteanual_detail'),
]

