from django.test import TestCase, Client
from app_reporte.models import Region, Ciudad, Comuna
from app_reporte.models import OrganismoResponsable, Medida, MedioVerificacion, Reporte
import json
# Create your tests here.

class LocalidadTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        # Crear superusuario
        from django.contrib.auth.models import User
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Superusuario creado")
        
        # Obtener token
        credenciales = {
            'username': 'admin',
            'password': 'admin'
        }
        
        respuesta_token = self.client.post('/api/token/', credenciales)
        self.assertEqual(respuesta_token.status_code, 200)
        token = respuesta_token.json()['access']

        # Crear región usando el token
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {token}',
            'content_type': 'application/json'
        }
        datos_region = {
                'nombre': 'Región Test 1'
        }
        
        respuesta = self.client.post('/api/regiones/', datos_region, **headers)
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['nombre'], 'Región Test 1')