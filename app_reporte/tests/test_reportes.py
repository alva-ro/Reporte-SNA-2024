from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from app_reporte.models import PlanPPDA, Medida, OrganismoResponsable

User = get_user_model()

class ReporteAuditAndUniqueTest(APITestCase):
    def setUp(self):
        # -- Preparamos datos mínimos: PlanPPDA, Medida, Organismo y User vinculado --
        self.plan = PlanPPDA.objects.create(
            nombre="Plan Test", mes_reporte=1, anio=2025
        )
        self.medida = Medida.objects.create(
            referencia_pda='R1',
            nombre_corto='NC1',
            indicador='I1',
            formula_calculo='F1',
            frecuencia_reporte='anual',
            tipo_medida='regulatoria',
            plan=self.plan
        )

        self.org = OrganismoResponsable.objects.create(nombre="OrgTest")

        # Creamos un usuario
        self.user = User.objects.create_user(username='u1', password='pw')

        # Creamos los grupos necesarios:
        # 1) Grupo para el organismo (usado en has_object_permission)
        org_group, _ = Group.objects.get_or_create(name=self.org.nombre)
        # 2) Grupo "Representante Organismo Responsable" (usado en has_permission para escrituras)
        rep_group, _ = Group.objects.get_or_create(name='Representante Organismo Responsable')

        # Asociamos el user a ambos grupos
        self.user.groups.add(org_group, rep_group)

        # Obtenemos token JWT
        self.client = APIClient()
        resp = self.client.post('/api/token/', {
            'username': 'u1', 'password': 'pw'
        })
        assert resp.status_code == status.HTTP_200_OK, "No se obtuvo token JWT"
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_created_by_and_updated_by(self):
        """
        Al crear un reporte, los campos created_by y updated_by deben guardarse
        con el id del usuario que hizo la petición.
        """
        url = '/api/reporte/'
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id,
        }
        resp = self.client.post(url, data, format='multipart')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('created_by', resp.data)
        self.assertIn('updated_by', resp.data)
        self.assertEqual(resp.data['created_by'], self.user.id)
        self.assertEqual(resp.data['updated_by'], self.user.id)

    def test_unique_constraint(self):
        """
        La segunda inserción del mismo (medida, organismo, fecha_envio) debe fallar
        con 400 y mensaje de unique.
        """
        url = '/api/reporte/'
        data = {
            'medida': self.medida.id,
            'organismo': self.org.id
        }
        r1 = self.client.post(url, data, format='multipart')
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        r2 = self.client.post(url, data, format='multipart')
        self.assertEqual(r2.status_code, status.HTTP_400_BAD_REQUEST)
        msg = str(r2.data).lower()
        self.assertTrue('unique' in msg or 'único' in msg)

    def test_timestamps_present(self):
        """
        Comprueba que al leer un reporte existen created_at y updated_at.
        """
        r = self.client.post('/api/reporte/', {
            'medida': self.medida.id,
            'organismo': self.org.id
        }, format='multipart')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        rid = r.data['id']
        rget = self.client.get(f'/api/reporte/{rid}')
        self.assertEqual(rget.status_code, status.HTTP_200_OK)
        self.assertIn('created_at', rget.data)
        self.assertIn('updated_at', rget.data)
