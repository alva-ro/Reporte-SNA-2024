from django.urls import path
from .views import PlanPPDAView, ComunaView

urlpatterns = [
    path('planes/', PlanPPDAView.as_view(), name='planes'),
    path('comunas/', ComunaView.as_view(), name='comunas'),
]

