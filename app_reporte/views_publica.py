# app_reporte/views_publica.py.

from rest_framework import generics
from .models import ReporteAnual, ElementoProbatorio
from .serializers import ReporteAnualSerializer, ElementoProbatorioSerializer

class ReporteAnualList(generics.ListAPIView):
    queryset = ReporteAnual.objects.all()
    serializer_class = ReporteAnualSerializer

class ElementoProbatorioList(generics.ListAPIView):
    queryset = ElementoProbatorio.objects.all()
    serializer_class = ElementoProbatorioSerializer