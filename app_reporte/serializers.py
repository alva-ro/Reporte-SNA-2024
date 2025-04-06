from rest_framework import serializers
from .models import (PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable, Medida, MedioVerificacion, Entidad,ReporteAnual,)
from .models import PlanPPDA, Region, Ciudad, Comuna, OrganismoResponsable, Medida, MedioVerificacion, Entidad, ReporteAnual


class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class PlanPPDASerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanPPDA
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'

class OrganismoResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganismoResponsable
        fields = '__all__'

class MedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medida
        fields = '__all__'

class MedioVerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioVerificacion
        fields = '__all__'

class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'

class ReporteAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteAnual
        fields = '__all__'
