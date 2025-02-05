from django.urls import path
from .views import PlanPPDAView, ComunaView, CiudadView, RegionView

urlpatterns = [
    path('planes/', PlanPPDAView.as_view(), name='planes'),
    path('comunas/', ComunaView.as_view(), name='comunas'),
    path('ciudades/', CiudadView.as_view(), name='ciudades'),
    path('regiones/', RegionView.as_view(), name='ciudades'),

]

