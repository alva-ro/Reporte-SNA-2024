from django.test import TestCase, Client
from app_reporte.models import Region, Ciudad, Comuna
from app_reporte.models import OrganismoResponsable, Medida, MedioVerificacion, Reporte
from django.contrib.auth.models import User
import json

class LocalidadTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear superusuario
        self.superadmin = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        # Crear usuario normal
        self.usuario_normal = User.objects.create_user('usuario_normal', 'usuario@example.com', 'password123')
        
        # Obtener tokens
        respuesta_token_admin = self.client.post('/api/token/', {'username': 'admin', 'password': 'admin'})
        self.token_admin = respuesta_token_admin.json()['access']
        
        respuesta_token_usuario = self.client.post('/api/token/', {'username': 'usuario_normal', 'password': 'password123'})
        self.token_usuario = respuesta_token_usuario.json()['access']
        
        # Headers comunes
        self.headers_admin = {
            'HTTP_AUTHORIZATION': f'Bearer {self.token_admin}',
            'content_type': 'application/json'
        }
        self.headers_usuario = {
            'HTTP_AUTHORIZATION': f'Bearer {self.token_usuario}',
            'content_type': 'application/json'
        }
        self.headers_sin_token = {
            'content_type': 'application/json'
        }

        # Crear datos básicos
        self.region = Region.objects.create(
            nombre="Región de Valparaiso"
        )
        self.ciudad = Ciudad.objects.create(
            nombre="ConCon",
            region=self.region
        )
        self.comuna = Comuna.objects.create(
            nombre="ConCon",
            ciudad=self.ciudad
        )

    def test_get_regiones(self):
        respuesta = self.client.get('/api/regiones/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertJSONEqual(respuesta.content, [
            {
                "nombre": "Región de Valparaiso",
                "id": self.region.id
            }
        ])

    def test_get_ciudades(self):
        respuesta = self.client.get('/api/ciudades/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertJSONEqual(respuesta.content, [
            {
                "nombre": "ConCon",
                "region": self.region.id,
                "id": self.ciudad.id
            }
        ])

    def test_get_comunas(self):
        respuesta = self.client.get('/api/comunas/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertJSONEqual(respuesta.content, [
            {
                "nombre": "ConCon",
                "ciudad": self.ciudad.id,
                "id": self.comuna.id
            }
        ])

    def test_create_region(self):
        datos_region = {
            'nombre': 'Región Test 1'
        }
        
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['nombre'], 'Región Test 1')

    def test_create_region_unauthorized(self):
        datos_region = {
            'nombre': 'Región Test No Autorizada'
        }
        
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_usuario)
        self.assertEqual(respuesta.status_code, 403)

    def test_create_region_no_token(self):
        datos_region = {
            'nombre': 'Región Test Sin Token'
        }
        
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_sin_token)
        self.assertEqual(respuesta.status_code, 401)

    def test_update_region_superadmin(self):
        # Crear región para actualizar
        datos_region = {
            'nombre': 'Región Test 1'
        }
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        region_id = respuesta.json()['id']

        # Actualizar región
        datos_actualizacion = {
            'nombre': 'Región Test Actualizada'
        }
        respuesta = self.client.put(f'/api/regiones/{region_id}/', datos_actualizacion, **self.headers_admin)
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['nombre'], 'Región Test Actualizada')

    def test_update_region_unauthorized(self):
        # Crear región con superadmin primero
        datos_region = {'nombre': 'Región Test 1'}
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        region_id = respuesta.json()['id']

        # Intentar actualizar región con usuario normal
        datos_actualizacion = {
            'nombre': 'Región Test No Autorizada'
        }
        
        respuesta = self.client.put(f'/api/regiones/{region_id}/', datos_actualizacion, **self.headers_usuario)
        self.assertEqual(respuesta.status_code, 403)

    def test_update_region_no_token(self):
        # Crear región con superadmin primero
        datos_region = {'nombre': 'Región Test 1'}
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        region_id = respuesta.json()['id']

        # Intentar actualizar región sin token
        datos_actualizacion = {
            'nombre': 'Región Test Sin Token'
        }
        
        respuesta = self.client.put(f'/api/regiones/{region_id}/', datos_actualizacion, **self.headers_sin_token)
        self.assertEqual(respuesta.status_code, 401)

    def test_delete_region_superadmin(self):
        # Crear región para eliminar
        datos_region = {
            'nombre': 'Región Test 1'
        }
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        region_id = respuesta.json()['id']

        # Eliminar región
        respuesta = self.client.delete(f'/api/regiones/{region_id}/', **self.headers_admin)
        self.assertEqual(respuesta.status_code, 204)

    def test_delete_region_unauthorized(self):
        # Crear región con superadmin primero
        datos_region = {'nombre': 'Región Test 1'}
        respuesta = self.client.post('/api/regiones/', datos_region, **self.headers_admin)
        region_id = respuesta.json()['id']

        # Intentar eliminar región con usuario normal
        respuesta = self.client.delete(f'/api/regiones/{region_id}/', **self.headers_usuario)
        self.assertEqual(respuesta.status_code, 403)

    def test_delete_region_no_token(self):
        # Intentar eliminar región sin token
        respuesta = self.client.delete('/api/regiones/1/', **self.headers_sin_token)
        self.assertEqual(respuesta.status_code, 401) 