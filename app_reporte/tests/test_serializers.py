from django.test import TestCase
from django.contrib.auth.models import User
from app_reporte.models import (
    Region, Ciudad, Comuna, PlanPPDA, Medida, 
    OrganismoResponsable, Reporte, MedioVerificacion, Entidad
)
from app_reporte.serializers import (
    RegionSerializer, CiudadSerializer, ComunaSerializer,
    PlanPPDASerializer, MedidaSerializer, OrganismoResponsableSerializer,
    ReporteSerializer, MedioVerificacionSerializer
)

class SerializersTest(TestCase):
    def setUp(self):
        # Crear datos básicos
        self.region = Region.objects.create(nombre="Región de Valparaiso")
        self.ciudad = Ciudad.objects.create(nombre="ConCon", region=self.region)
        self.comuna = Comuna.objects.create(nombre="ConCon", ciudad=self.ciudad)
        
        # Crear plan PPDA
        self.plan = PlanPPDA.objects.create(
            nombre="Plan Test", 
            mes_reporte=1, 
            anio=2025
        )
        
        # Crear medida
        self.medida = Medida.objects.create(
            referencia_pda='R1',
            nombre_corto='NC1',
            indicador='I1',
            formula_calculo='F1',
            frecuencia_reporte='anual',
            tipo_medida='regulatoria',
            plan=self.plan
        )
        
        # Crear organismo
        self.org = OrganismoResponsable.objects.create(nombre="OrgTest")
        
        # Crear entidad
        self.entidad = Entidad.objects.create(nombre="Entidad Test")
        
        # Crear medio de verificación
        self.medio_verificacion = MedioVerificacion.objects.create(
            descripcion="Descripción Test",
            tipo='informe_anual',
            medida=self.medida,
            entidad_a_cargo=self.entidad
        )
        
        # Crear usuario
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        
        # Crear reporte
        self.reporte = Reporte.objects.create(
            medida=self.medida,
            organismo=self.org,
            created_by=self.user,
            updated_by=self.user
        )

    def test_region_serializer(self):
        """Test para el serializer de Region"""
        serializer = RegionSerializer(self.region)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'Región de Valparaiso')
        self.assertEqual(data['id'], self.region.id)

    def test_ciudad_serializer(self):
        """Test para el serializer de Ciudad"""
        serializer = CiudadSerializer(self.ciudad)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'ConCon')
        self.assertEqual(data['region'], self.region.id)
        self.assertEqual(data['id'], self.ciudad.id)

    def test_comuna_serializer(self):
        """Test para el serializer de Comuna"""
        serializer = ComunaSerializer(self.comuna)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'ConCon')
        self.assertEqual(data['ciudad'], self.ciudad.id)
        self.assertEqual(data['id'], self.comuna.id)

    def test_plan_ppda_serializer(self):
        """Test para el serializer de PlanPPDA"""
        serializer = PlanPPDASerializer(self.plan)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'Plan Test')
        self.assertEqual(data['mes_reporte'], 1)
        self.assertEqual(data['anio'], 2025)
        self.assertEqual(data['id'], self.plan.id)

    def test_medida_serializer(self):
        """Test para el serializer de Medida"""
        serializer = MedidaSerializer(self.medida)
        data = serializer.data
        
        self.assertEqual(data['referencia_pda'], 'R1')
        self.assertEqual(data['nombre_corto'], 'NC1')
        self.assertEqual(data['indicador'], 'I1')
        self.assertEqual(data['formula_calculo'], 'F1')
        self.assertEqual(data['frecuencia_reporte'], 'anual')
        self.assertEqual(data['tipo_medida'], 'regulatoria')
        self.assertEqual(data['plan'], self.plan.id)
        self.assertEqual(data['id'], self.medida.id)

    def test_organismo_responsable_serializer(self):
        """Test para el serializer de OrganismoResponsable"""
        serializer = OrganismoResponsableSerializer(self.org)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'OrgTest')
        self.assertEqual(data['id'], self.org.id)

    def test_medio_verificacion_serializer(self):
        """Test para el serializer de MedioVerificacion"""
        serializer = MedioVerificacionSerializer(self.medio_verificacion)
        data = serializer.data
        
        self.assertEqual(data['descripcion'], 'Descripción Test')
        self.assertEqual(data['tipo'], 'informe_anual')
        self.assertEqual(data['medida'], self.medida.id)
        self.assertEqual(data['entidad_a_cargo'], self.entidad.id)
        self.assertEqual(data['id'], self.medio_verificacion.id)

    def test_reporte_serializer(self):
        """Test para el serializer de Reporte"""
        serializer = ReporteSerializer(self.reporte)
        data = serializer.data
        
        self.assertEqual(data['medida'], self.medida.id)
        self.assertEqual(data['organismo'], self.org.id)
        self.assertEqual(data['created_by'], self.user.id)
        self.assertEqual(data['updated_by'], self.user.id)
        self.assertEqual(data['id'], self.reporte.id)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data) 