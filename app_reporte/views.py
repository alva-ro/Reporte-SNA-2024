from django.core.exceptions import BadRequest
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable
from .serializers import PlanPPDASerializer, ComunaSerializer, RegionSerializer, \
    CiudadSerializer, OrganismoResponsableSerializer


class ComunaView(APIView):
    """
    API para gestionar las comunas.

    Endpoints:
    - GET /comuna/: Listar todas las comunas.
    - POST /comuna/: Crear una nueva comuna.
    """
    def get(self, request):
        """
        Listar todas las comunas.

        Retorna:
        - Lista de comunas en formato JSON.
        """
        comunas = Comuna.objects.all()
        serializer = ComunaSerializer(comunas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear una nueva comuna.

        Parámetros:
        - request.data: Datos de la comuna a crear.

        Retorna:
        - Datos de la comuna creada en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = ComunaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanPPDAView(APIView):
    """
    API para gestionar los planes PPDA.

    Endpoints:
    - GET /plan-ppda/: Listar todos los planes PPDA.
    - POST /plan-ppda/: Crear un nuevo plan PPDA.
    """
    def get(self, request):
        """
        Listar todos los planes PPDA.

        Retorna:
        - Lista de planes PPDA en formato JSON.
        """
        planes = PlanPPDA.objects.all()
        serializer = PlanPPDASerializer(planes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear un nuevo plan PPDA.

        Parámetros:
        - request.data: Datos del plan PPDA a crear.

        Retorna:
        - Datos del plan PPDA creado en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = PlanPPDASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegionView(APIView):
    """
    API para presentar las Regiones, utilizable en filtros o selectores para la definición de PlanesPPDA, por ejemplo.

    Endpoints:
    - GET /regiones/: Listar todas las Regiones.
    """
    def get(self, request):
        """
        Listar todas las Regiones.

        Retorna:
        - Lista de Regiones en formato JSON.
        """
        comunas = Region.objects.all()
        serializer = RegionSerializer(comunas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CiudadView(APIView):
    """
    API para presentar las Ciudades, utilizable en filtros o selectores para la definición de PlanesPPDA, por ejemplo.

    Endpoints:
    - GET /ciudad/: Listar todas las Ciudades.
    """
    def get(self, request):
        """
        Listar todas las Ciudades.

        Retorna:
        - Lista de Ciudades en formato JSON.
        """
        planes = Ciudad.objects.all()
        serializer = CiudadSerializer(planes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganismoResponsableView(APIView):
    """
    API para operaciones CRUD sobre los Organismos Responsables.

    Endpoints:
    - GET /organismo-responsable/id: Lista detalles de un Organismo Responsable.
    - POST /organismo-responsable/: Crear un nuevo Organismo Responsable.
    - PUT /organismo-responsable/id: Actualiza campos de un Organismo Responsable
    - DELETE /organismo-responsable/id: Elimina un Organismo Responsable, si no tiene dependencias
    """
    def get(self, request, id_orgres):
        """
        Listar un Organismo Responsable y sus .

        Retorna:
        - Lista de planes PPDA en formato JSON.
        """
        org_res = OrganismoResponsable.objects.filter(id=id_orgres)
        if not org_res:
            raise Http404
        serializer = OrganismoResponsableSerializer(org_res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear un nuevo Organismo Responsable.

        Parámetros:
        - request.data: Datos del Organismo Responsable a crear.

        Retorna:
        - Datos del Organismo Responsable creado en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = OrganismoResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_orgres):
        """
        Crear un nuevo Organismo Responsable.

        Parámetros:
        - request.data: Datos del Organismo Responsable a crear.

        Retorna:
        - Datos del Organismo Responsable creado en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        org_res = OrganismoResponsable.objects.filter(id=id_orgres).first()
        if org_res == None:
            raise BadRequest("Recurso solicitado no existe")
        serializer = OrganismoResponsableSerializer(org_res, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id_orgres):
        org_res = OrganismoResponsable.objects.filter(id=id_orgres).delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)

class OrganismosResponsablesView(APIView):
    """
    API para listar los Organismos Responsables.

    Endpoints:
    - GET /organismos-responsables/: Listar Organismos Responsables.
    """
    def get(self, request):
        """
        Listar Organismos Responsables.

        Retorna:
        - Lista de Organismos Responsables en formato JSON.
        """
        planes = OrganismoResponsable.objects.all()
        serializer = OrganismoResponsableSerializer(planes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
