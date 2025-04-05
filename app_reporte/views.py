from django.core.exceptions import BadRequest
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable
from .serializers import PlanPPDASerializer, ComunaSerializer, RegionSerializer, \
    CiudadSerializer, OrganismoResponsableSerializer

from .models import Reporte
from .serializers import ReporteSerializer
from rest_framework import filters
from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.permissions import IsAdminUser


@extend_schema_view(
    get=extend_schema(summary="Listar todas las comunas", tags=["Comunas"]),
    post=extend_schema(summary="Crear una nueva comuna", tags=["Comunas"])
)
class ComunaView(APIView):
    serializer_class = ComunaSerializer
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

@extend_schema_view(
    get=extend_schema(summary="Listar todos los planes PPDA", tags=["Planes PPDA"]),
    post=extend_schema(summary="Crear un nuevo plan PPDA", tags=["Planes PPDA"])
)
class PlanPPDAView(APIView):
    serializer_class = PlanPPDASerializer
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
    

@extend_schema_view(
    get=extend_schema(summary="Listar todas las regiones", tags=["Regiones"]),
    post=extend_schema(summary="Crear una nueva región", tags=["Regiones"])
)
class RegionView(APIView):
    serializer_class = RegionSerializer
    def get(self, request):
        """
        Listar todas las regiones.

        Retorna:
        - Lista de comunas en formato JSON.
        """
        ciudades = Region.objects.all()
        serializer = RegionSerializer(ciudades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear una nueva región.

        Parámetros:
        - request.data: Datos de la región a crear.

        Retorna:
        - Datos de la Región creada en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(summary="Listar todas las ciudades", tags=["Ciudades"]),
    post=extend_schema(summary="Crear una nueva ciudad", tags=["Ciudades"])
)
class CiudadView(APIView):
    serializer_class = CiudadSerializer
    def get(self, request):
        """
        Listar todas las ciudades.

        Retorna:
        - Lista de ciudades en formato JSON.
        """
        ciudades = Ciudad.objects.all()
        serializer = CiudadSerializer(ciudades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Crear una nueva ciudad.

        Parámetros:
        - request.data: Datos de la ciudad a crear.

        Retorna:
        - Datos de la ciudad creada en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = CiudadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(summary="Listar detalles de un Organismo Responsable",
                      tags=["Organismos Responsables"]),
    post=extend_schema(summary="Crear un nuevo Organismo Responsable",
                       tags=["Organismos Responsables"]),
    put=extend_schema(summary="Actualizar un Organismo Responsable existente",
                      tags=["Organismos Responsables"]),
    delete=extend_schema(summary="Eliminar un Organismo Responsable existente",
                         tags=["Organismos Responsables"])
)
class OrganismoResponsableView(APIView):
    serializer_class = OrganismoResponsableSerializer
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
        - Errores de validación y có digo de estado HTTP 400 si la creación falla.
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
        if not org_res:
            raise BadRequest("Recurso solicitado no existe")
        serializer = OrganismoResponsableSerializer(org_res, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_orgres):
        org_res = OrganismoResponsable.objects.filter(id=id_orgres).delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    get=extend_schema(summary="Listar todos los Organismos Responsables",
        tags=["Organismos Responsables"]),
)
class OrganismosResponsablesView(APIView):
    """
    API para listar los Organismos Responsables.

    Endpoints:
    - GET /organismos-responsables/: Listar Organismos Responsables.
    """
    serializer_class = OrganismoResponsableSerializer
    def get(self, request):
        """
        Listar Organismos Responsables.

        Retorna:
        - Lista de Organismos Responsables en formato JSON.
        """
        planes = OrganismoResponsable.objects.all()
        serializer = OrganismoResponsableSerializer(planes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
    Lista reportes
"""
@extend_schema_view(
    get=extend_schema(
        summary="Listar reportes",
        description="Permite listar reportes con filtros por organismo, estado y fecha de envío",
        tags=["Reportes"]
    )
)
class ReporteListView(APIView):
    serializer_class = ReporteSerializer
    permission_classes = [IsAdminUser]
    def get(self, request):
        queryset = Reporte.objects.all()

        organismo_id = request.GET.get('organismo')
        estado = request.GET.get('estado')
        fecha_envio = request.GET.get('fecha_envio')

        if organismo_id:
            queryset = queryset.filter(organismo_id=organismo_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if fecha_envio:
            queryset = queryset.filter(fecha_envio=fecha_envio)

        serializer = ReporteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
    Actualizar el estado de un reporte a "aprobado", "rechazado" o "pendiente".
"""
@extend_schema_view(
    put=extend_schema(
        summary="Modificar estado de un reporte",
        description="Permite cambiar el estado de un reporte a aprobado, rechazado o pendiente",
        tags=["Reportes"]
    )
)

class ReporteEstadoUpdateView(APIView):
    serializer_class = ReporteSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, id_reporte):
        try:
            reporte = Reporte.objects.get(id=id_reporte)
        except Reporte.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nuevo_estado = request.data.get("estado")
        if nuevo_estado not in ["pendiente", "aprobado", "rechazado"]:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if nuevo_estado == reporte.estado:
            return Response(
                {"detail": "El reporte ya tiene ese estado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reporte.estado = nuevo_estado
        reporte.save()

        serializer = ReporteSerializer(reporte)
        return Response(serializer.data, status=status.HTTP_200_OK)
