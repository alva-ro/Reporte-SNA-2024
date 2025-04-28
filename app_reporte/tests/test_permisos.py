from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from app_reporte.models import (
    Region, Ciudad, Comuna, PlanPPDA, Medida, 
    OrganismoResponsable, Reporte, MedioVerificacion, Entidad
)
from app_reporte.permisos import (
    EsRepresentanteOrganismoResponsable,
    EsAdmin,
    EsSuperAdmin
)
import json

class PermisosTest(APITestCase):
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
        
        # Crear grupos necesarios
        self.org_group = Group.objects.create(name=self.org.nombre)
        self.rep_group = Group.objects.create(name='Representante Organismo Responsable')
        
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

    def test_es_superadmin(self):
        """Test para verificar el permiso de superadmin"""
        permiso = EsSuperAdmin()
        
        # Crear una solicitud simulada
        request = type('Request', (), {'user': self.superadmin})()
        
        # Verificar que el superadmin tiene permiso
        self.assertTrue(permiso.has_permission(request, None))
        
        # Verificar que el usuario normal no tiene permiso
        request.user = self.usuario_normal
        self.assertFalse(permiso.has_permission(request, None))

    def test_es_representante_organismo_responsable(self):
        """Test para verificar el permiso de representante de organismo responsable"""
        permiso = EsRepresentanteOrganismoResponsable()
        
        # Crear una solicitud simulada
        request = type('Request', (), {'user': self.usuario_normal})()
        
        # Verificar que el usuario sin el grupo no tiene permiso
        self.assertFalse(permiso.has_permission(request, None))
        
        # Agregar el usuario al grupo de representante
        self.usuario_normal.groups.add(self.rep_group)
        
        # Verificar que ahora tiene permiso
        self.assertTrue(permiso.has_permission(request, None))

    def test_es_admin(self):
        """Test para verificar el permiso de admin"""
        permiso = EsAdmin()
        
        # Crear una solicitud simulada
        request = type('Request', (), {'user': self.usuario_normal})()
        
        # Verificar que el usuario sin el grupo no tiene permiso
        self.assertFalse(permiso.has_permission(request, None))
        
        # Agregar el usuario al grupo de admin
        admin_group = Group.objects.create(name='Administrador')
        self.usuario_normal.groups.add(admin_group)
        
        # Verificar que ahora tiene permiso
        self.assertTrue(permiso.has_permission(request, None))

    def test_permisos_en_api(self):
        """Test para verificar los permisos en las APIs"""
        # Agregar el usuario al grupo de representante
        self.usuario_normal.groups.add(self.rep_group)
        
        # Intentar crear un plan PPDA con usuario normal (debería fallar)
        url = '/api/planes/'
        data = {
            'nombre': 'Nuevo Plan',
            'mes_reporte': 2,
            'anio': 2025
        }
        response = self.client_user.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Intentar crear un plan PPDA con superadmin (debería funcionar)
        response = self.client_admin.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Agregar el usuario al grupo del organismo
        self.usuario_normal.groups.add(self.org_group)
        
        # Intentar crear un reporte con usuario normal (debería funcionar)
        url = '/api/reporte/'
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id
        }
        response = self.client_user.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 