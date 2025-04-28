from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from app_reporte.models import (
    Region, Ciudad, Comuna, PlanPPDA, Medida, 
    OrganismoResponsable, Reporte, MedioVerificacion, Entidad
)
import json

class ViewsTest(APITestCase):
    def setUp(self):
        # Crear superusuario
        self.superadmin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        
        # Crear usuario normal
        self.usuario_normal = User.objects.create_user('usuario_normal', 'usuario@example.com', 'password123')
        
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
        
        # Obtener tokens
        self.client = APIClient()
        
        # Token para admin
        resp_admin = self.client.post('/api/token/', {'username': 'admin', 'password': 'admin'})
        self.token_admin = resp_admin.data['access']
        self.client_admin = APIClient()
        self.client_admin.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        
        # Token para usuario normal
        resp_user = self.client.post('/api/token/', {'username': 'usuario_normal', 'password': 'password123'})
        self.token_user = resp_user.data['access']
        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        
        # Crear grupos necesarios
        self.org_group = Group.objects.create(name=self.org.nombre)
        self.rep_group = Group.objects.create(name='Representante Organismo Responsable')
        self.usuario_normal.groups.add(self.org_group, self.rep_group)

    def test_list_planes_ppda(self):
        """Test para listar planes PPDA"""
        url = '/api/planes/'
        response = self.client_admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Plan Test')

    def test_create_plan_ppda(self):
        """Test para crear un plan PPDA"""
        url = '/api/planes/'
        data = {
            'nombre': 'Nuevo Plan',
            'mes_reporte': 2,
            'anio': 2025
        }
        response = self.client_admin.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Nuevo Plan')

    def test_list_medidas(self):
        """Test para listar medidas"""
        url = '/api/medidas/'
        response = self.client_admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['referencia_pda'], 'R1')

    def test_create_medida(self):
        """Test para crear una medida"""
        data = {
            'referencia_pda': 'R2',
            'nombre_corto': 'NC2',
            'descripcion': 'Descripción de prueba',
            'indicador': 'I2',
            'formula_calculo': 'F2',
            'frecuencia_reporte': 'anual',
            'tipo_medida': 'regulatoria',
            'plan': self.plan.id,
            'organismos': [self.org.id]
        }
        response = self.client_admin.post('/api/medidas/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medida.objects.count(), 2)

    def test_list_medios_verificacion(self):
        """Test para listar medios de verificación"""
        response = self.client_admin.get('/api/medidas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_organismos(self):
        """Test para listar organismos"""
        url = '/api/organismo-responsable/'
        response = self.client_admin.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'OrgTest')

    def test_create_organismo(self):
        """Test para crear un organismo"""
        url = '/api/organismo-responsable/'
        data = {
            'nombre': 'Nuevo Org'
        }
        response = self.client_admin.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Nuevo Org')

    def test_list_reportes(self):
        """Test para listar reportes"""
        # Crear un reporte primero
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id,
            'descripcion': 'Test Reporte'
        }
        response = self.client_user.post('/api/reporte/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Listar reportes
        response = self.client_admin.get('/api/reportes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

    def test_create_reporte(self):
        """Test para crear un reporte"""
        url = '/api/reporte/'
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id
        }
        response = self.client_user.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['medida'], self.medida.id)
        self.assertEqual(response.data['organismo'], self.org.id)

    def test_update_reporte(self):
        """Test para actualizar un reporte"""
        # Crear un reporte primero
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id,
            'descripcion': 'Test Reporte'
        }
        response = self.client_user.post('/api/reporte/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reporte_id = response.data['id']
        
        # Actualizar el reporte
        data_update = {
            'medida': self.medida.id,
            'organismo': self.org.id,
            'descripcion': 'Test Reporte Actualizado'
        }
        response = self.client_user.put(f'/api/reporte/{reporte_id}', data_update, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descripcion'], 'Test Reporte Actualizado')

    def test_delete_reporte(self):
        """Test para eliminar un reporte"""
        # Crear un reporte primero
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id,
            'descripcion': 'Test Reporte'
        }
        response = self.client_user.post('/api/reporte/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reporte_id = response.data['id']
        
        # Eliminar el reporte
        response = self.client_user.delete(f'/api/reporte/{reporte_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 