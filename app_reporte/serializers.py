from rest_framework import serializers
from .models import PlanPPDA, Comuna

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class PlanPPDASerializer(serializers.ModelSerializer):
    comunas = ComunaSerializer(many=True)

    class Meta:
        model = PlanPPDA
        fields = '__all__'
