from rest_framework import serializers
from .models import (PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable, Medida, MedioVerificacion, Entidad, Reporte, ReporteAnual, ElementoProbatorio,)
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

    def validate(self, data):
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        if data['anio'] == current_year and data['mes_reporte'] > current_month:
            raise serializers.ValidationError(
                "El mes del reporte no puede ser futuro para el año actual"
            )
        
        return data
    
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

# Serializer para API pública de reportes anuales
class ReporteAnualSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteAnual
        fields = '__all__'

# Serializer para API pública de elementos probatorios
class ElementoProbatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoProbatorio
        fields = '__all__'