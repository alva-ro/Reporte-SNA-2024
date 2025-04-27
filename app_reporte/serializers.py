from rest_framework import serializers
from .models import (PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable, Medida, MedioVerificacion, Entidad, Reporte,)
from datetime import datetime
from .models import Reporte

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class PlanPPDASerializer(serializers.ModelSerializer):
    mes_reporte = serializers.IntegerField(
        min_value=1,
        max_value=12,
        help_text="Mes del reporte (1-12)"
    )
    
    anio = serializers.IntegerField(
        min_value=2000,
        max_value= datetime.now().year + 1,
        help_text=f"Año del reporte (2000-{datetime.now().year + 1})"
    )
    
    comunas = serializers.PrimaryKeyRelatedField(
        required = False,
        many=True,
        queryset = Comuna.objects.all()
    )

    class Meta:
        model = PlanPPDA
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_comunas(self, value):
        """Valida que las comunas existan"""
        if not value:
            raise serializers.ValidationError("Debe especificar al menos una comuna")
        return value

    def update(self, instance, validated_data):
        """Maneja la actualización de las comunas"""
        comunas_data = validated_data.pop('comunas', None)
        
        instance = super().update(instance, validated_data)
        
        if comunas_data is not None:
            instance.comunas.set(comunas_data)
        
        return instance

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
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate_plan(self, value):
        """Valida que el plan exista"""
        if not value:
            raise serializers.ValidationError("Debe especificar un plan PPDA")
        return value

class MedioVerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioVerificacion
        fields = '__all__'

class EntidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entidad
        fields = '__all__'
class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'
