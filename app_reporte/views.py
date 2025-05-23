from django.core.exceptions import BadRequest, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable, Medida, MedioVerificacion, Reporte
from .serializers import PlanPPDASerializer, ComunaSerializer, RegionSerializer, \
    CiudadSerializer, OrganismoResponsableSerializer, MedidaSerializer, MedioVerificacionSerializer, EntidadSerializer, ReporteSerializer
from .models import Reporte
from .serializers import ReporteSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from app_reporte.permisos import EsRepOrgResOSoloLectura, EsSuperAdminOSoloLectura, EsAdminOSoloLectura, EsSuperAdmin
from datetime import datetime
from .models import Reporte, HistorialEstadoReporte
from django.utils.timezone import now
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from app_reporte.models import Reporte
from app_reporte.serializers import ReporteSerializer
from django.contrib.auth import get_user_model
import unicodedata


User = get_user_model()


def normalizar_texto(texto):
    """
    Normaliza el texto eliminando acentos y convirtiendo a minúsculas.
    """
    if not texto:
        return ""
    texto_normalizado = ''.join(c for c in unicodedata.normalize('NFD', texto)
                              if unicodedata.category(c) != 'Mn')
    return texto_normalizado.lower()

@extend_schema_view(
    get=extend_schema(
        summary="Listar todas las comunas", 
        tags=["Comunas"],
        parameters=[
            OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar comunas por nombre (búsqueda parcial, case-insensitive, ignora tildes)'),
            OpenApiParameter(name='ciudad_id', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar comunas por ID de ciudad'),
            OpenApiParameter(name='ciudad_nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar comunas por nombre de ciudad (búsqueda parcial, case-insensitive, ignora tildes)'),
        ],
    ),
    post=extend_schema(summary="Crear una nueva comuna", tags=["Comunas"], request=ComunaSerializer),
)
class ComunaView(APIView):
    serializer_class = ComunaSerializer
    permission_classes=[EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar todas las comunas.
        
        Parámetros de búsqueda:
        - nombre: Filtrar comunas por nombre (búsqueda parcial, case-insensitive, ignora tildes)
        - ciudad_id: Filtrar comunas por ID de ciudad
        - ciudad_nombre: Filtrar comunas por nombre de ciudad (búsqueda parcial, case-insensitive, ignora tildes)

        Retorna:
        - Lista de comunas en formato JSON.
        """
        comunas = Comuna.objects.all()
        
        nombre = request.GET.get('nombre')
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            comunas = [comuna for comuna in comunas 
                      if nombre_normalizado in normalizar_texto(comuna.nombre)]
        
        ciudad_id = request.GET.get('ciudad_id')
        ciudad_nombre = request.GET.get('ciudad_nombre')
        
        if ciudad_id:
            comunas = [comuna for comuna in comunas 
                      if str(comuna.ciudad.id) == ciudad_id]
        elif ciudad_nombre:
            ciudad_nombre_normalizado = normalizar_texto(ciudad_nombre)
            comunas = [comuna for comuna in comunas 
                      if ciudad_nombre_normalizado in normalizar_texto(comuna.ciudad.nombre)]
            
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
        - Código de estado HTTP 409 si ya existe una comuna con el mismo nombre en la misma ciudad.
        """

        nombre_comuna = request.data.get('nombre')
        ciudad_id = request.data.get('ciudad')
        
        if nombre_comuna and ciudad_id:
            nombre_normalizado = normalizar_texto(nombre_comuna)
            
            comunas_existentes = Comuna.objects.filter(ciudad_id=ciudad_id)
            for comuna in comunas_existentes:
                if normalizar_texto(comuna.nombre) == nombre_normalizado:
                    return Response(
                        {"error": f"Ya existe una comuna con el nombre '{nombre_comuna}' en la ciudad seleccionada"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = ComunaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(
        summary="Obtener una comuna a través de su id", 
        tags=["Comunas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la comuna a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Modificar una comuna existente a través de su id", 
        tags=["Comunas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la comuna a modificar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar una comuna a través de su id", 
        tags=["Comunas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la comuna a eliminar'),
        ],
    )
)
class ComunaDetailView(APIView):
    serializer_class = ComunaSerializer
    permission_classes=[EsSuperAdminOSoloLectura]
    
    def get(self, request, pk=None):
        if not pk:
            raise BadRequest("Se requiere un ID de comuna para esta operacion.")
        comuna = get_object_or_404(Comuna, id=pk)
        serializer = ComunaSerializer(comuna)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        if not pk:
            raise BadRequest("Se requiere un ID de comuna para esta operacion.")
        comuna = get_object_or_404(Comuna, id=pk)
        serializer = ComunaSerializer(comuna, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            raise BadRequest("Se requiere un ID de comuna para esta operacion.")
        comuna = get_object_or_404(Comuna, id=pk)
        
        try:
            comuna.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@extend_schema_view(
    get=extend_schema(
        summary="Listar todos los planes PPDA", 
        tags=["Planes PPDA"],
        parameters=[
            OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar planes por nombre (búsqueda parcial, case-insensitive, ignora tildes)'),
            OpenApiParameter(name='mes_reporte', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar planes por mes de reporte (1-12)'),
            OpenApiParameter(name='anio', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar planes por año'),
            OpenApiParameter(name='comuna_id', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar planes por ID de comuna'),
        ],
    ),
    post=extend_schema(summary="Crear un nuevo plan PPDA", tags=["Planes PPDA"], request=PlanPPDASerializer)
)
class PlanPPDAView(APIView):
    serializer_class = PlanPPDASerializer
    permission_classes=[EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar todos los planes PPDA.
        
        Parámetros de búsqueda:
        - nombre: Filtrar planes por nombre (búsqueda parcial, case-insensitive, ignora tildes)
        - mes_reporte: Filtrar planes por mes de reporte (1-12)
        - anio: Filtrar planes por año
        - comuna_id: Filtrar planes por ID de comuna

        Retorna:
        - Lista de planes PPDA en formato JSON.
        """
        planes = PlanPPDA.objects.all()
        
        nombre = request.GET.get('nombre')
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            planes = [plan for plan in planes 
                     if nombre_normalizado in normalizar_texto(plan.nombre)]
        
        mes_reporte = request.GET.get('mes_reporte')
        if mes_reporte:
            try:
                mes_reporte = int(mes_reporte)
                planes = [plan for plan in planes 
                         if plan.mes_reporte == mes_reporte]
            except ValueError:
                pass
        
        anio = request.GET.get('anio')
        if anio:
            try:
                anio = int(anio)
                planes = [plan for plan in planes 
                         if plan.anio == anio]
            except ValueError:
                pass
        
        comuna_id = request.GET.get('comuna_id')
        if comuna_id:
            planes = [plan for plan in planes 
                     if any(str(comuna.id) == comuna_id for comuna in plan.comunas.all())]
            
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
        - Código de estado HTTP 409 si ya existe un plan con los mismos valores en los campos nombre, anio, mes_reporte y comunas.
        """
        nombre_plan = request.data.get('nombre')
        anio_plan = request.data.get('anio')
        mes_reporte_plan = request.data.get('mes_reporte')
        comunas_ids = request.data.get('comunas', [])
        
        if nombre_plan and anio_plan and mes_reporte_plan and comunas_ids:
            planes_existentes = PlanPPDA.objects.filter(
                nombre=nombre_plan,
                anio=anio_plan,
                mes_reporte=mes_reporte_plan
            )
            
            for plan in planes_existentes:
                plan_comunas_ids = set(plan.comunas.values_list('id', flat=True))
                if set(comunas_ids) == plan_comunas_ids:
                    return Response(
                        {"error": "Ya existe un plan con los mismos valores en los campos nombre, anio, mes_reporte y comunas"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = PlanPPDASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        summary="Obtener un plan PPDA a través de su id", 
        tags=["Planes PPDA"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID del plan PPDA a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Modificar un plan PPDA existente a través de su id", 
        tags=["Planes PPDA"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID del plan PPDA a modificar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar un plan PPDA a través de su id",
        tags=["Planes PPDA"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID del plan PPDA a eliminar'),
        ],
    )
)
class PlanPPDADetailView(APIView):    
    permission_classes=[EsSuperAdminOSoloLectura]
    def put(self, request, pk):
        """Actualizar un plan PPDA"""
        try:
         planPPDA = PlanPPDA.objects.get(pk=pk)
        except PlanPPDA.DoesNotExist:
            return Response(
            {"error": "Plan PPDA no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = PlanPPDASerializer(planPPDA, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener un plan PPDA por su id"""
        try:
            planPPDA = PlanPPDA.objects.get(pk=pk)
            serializer = PlanPPDASerializer(planPPDA)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PlanPPDA.DoesNotExist:
            raise Http404("Plan PPDA no encontrada")
    
    def delete(self,request, pk):
        """Eliminar un plan PPDA"""
        try:
            planPPDA = PlanPPDA.objects.get(pk=pk)
            try:
                planPPDA.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return Response(
                    {"error": "No se puede eliminar este plan porque tiene medidas asociadas. Primero debe eliminar o reasignar las medidas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except PlanPPDA.DoesNotExist:
            return Response(
            {"error": "Plan PPDA no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema_view(
    get=extend_schema(
        summary="Listar todas las regiones", 
        tags=["Regiones"],
        parameters=[
            OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar regiones por nombre (búsqueda parcial, case-insensitive, ignora tildes)'),
        ],
    ),
    post=extend_schema(summary="Crear una nueva región", tags=["Regiones"], request=RegionSerializer)
)
class RegionView(APIView):
    serializer_class = RegionSerializer
    permission_classes=[EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar todas las regiones.
        
        Parámetros de búsqueda:
        - nombre: Filtrar regiones por nombre (búsqueda parcial, case-insensitive, ignora tildes)

        Retorna:
        - Lista de regiones en formato JSON.
        """
        regiones = Region.objects.all()

        nombre = request.GET.get('nombre')
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            regiones = [region for region in regiones 
                       if nombre_normalizado in normalizar_texto(region.nombre)]
            
        serializer = RegionSerializer(regiones, many=True)
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
        - Código de estado HTTP 409 si ya existe una región con el mismo nombre.
        """
        nombre_region = request.data.get('nombre')
        
        if nombre_region:
            nombre_normalizado = normalizar_texto(nombre_region)
            
            regiones_existentes = Region.objects.all()
            for region in regiones_existentes:
                if normalizar_texto(region.nombre) == nombre_normalizado:
                    return Response(
                        {"error": f"Ya existe una región con el nombre '{nombre_region}'"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        summary="Obtener una región por id", 
        tags=["Regiones"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la región a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Modificar una región existente por su id", 
        tags=["Regiones"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la región a modificar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar una región por su id",
        tags=["Regiones"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la región a eliminar'),
        ],
    )
)
class RegionDetailView(APIView):
    serializer_class = RegionSerializer
    permission_classes = [EsSuperAdminOSoloLectura]

    def get(self, request, pk):
        if not pk:
            raise BadRequest("Se requiere un ID de región para esta operación.")
        region = get_object_or_404(Region, id=pk)
        serializer = RegionSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if not pk:
            raise BadRequest("Se requiere un ID de región para esta operación.")
        region = get_object_or_404(Region, id=pk)
        serializer = RegionSerializer(region, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not pk:
            raise BadRequest("Se requiere un ID de región para esta operación.")
        region = get_object_or_404(Region, id=pk)
        try:
            region.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response(
                {"error": "No se puede eliminar esta región porque tiene ciudades asociadas. Primero debe eliminar o reasignar las ciudades."},
                status=status.HTTP_400_BAD_REQUEST
            )

@extend_schema_view(
    get=extend_schema(
        summary="Listar todas las ciudades", 
        tags=["Ciudades"],
        parameters=[
            OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar ciudades por nombre (búsqueda parcial, case-insensitive, ignora tildes)'),
            OpenApiParameter(name='region_id', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar ciudades por ID de región'),
            OpenApiParameter(name='region_nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar ciudades por nombre de región (búsqueda parcial, case-insensitive, ignora tildes)'),
        ],
    ),
    post=extend_schema(summary="Crear una nueva ciudad", tags=["Ciudades"], request=CiudadSerializer)
)
class CiudadView(APIView):
    serializer_class = CiudadSerializer
    permission_classes=[EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar todas las ciudades.
        
        Parámetros de búsqueda:
        - nombre: Filtrar ciudades por nombre (búsqueda parcial, case-insensitive, ignora tildes)
        - region_id: Filtrar ciudades por ID de región
        - region_nombre: Filtrar ciudades por nombre de región (búsqueda parcial, case-insensitive, ignora tildes)

        Retorna:
        - Lista de ciudades en formato JSON.
        """
        ciudades = Ciudad.objects.all()
        
        nombre = request.GET.get('nombre')
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            ciudades = [ciudad for ciudad in ciudades 
                       if nombre_normalizado in normalizar_texto(ciudad.nombre)]
    
        region_id = request.GET.get('region_id')
        region_nombre = request.GET.get('region_nombre')
        
        if region_id:
            ciudades = [ciudad for ciudad in ciudades 
                       if str(ciudad.region.id) == region_id]
        elif region_nombre:
            region_nombre_normalizado = normalizar_texto(region_nombre)
            ciudades = [ciudad for ciudad in ciudades 
                       if region_nombre_normalizado in normalizar_texto(ciudad.region.nombre)]
            
        serializer = CiudadSerializer(ciudades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Crear una nueva ciudad.

        Parámetros:
        - request.data: Datos de la ciudad a crear.

        Retorna:
        - Datos de la ciudad creada en formato JSON.
        - Codigo de estado HTTP 201 si la creacion es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        - Código de estado HTTP 409 si ya existe una ciudad con el mismo nombre en la misma región.
        """
        nombre_ciudad = request.data.get('nombre')
        region_id = request.data.get('region')
        
        if nombre_ciudad and region_id:
            nombre_normalizado = normalizar_texto(nombre_ciudad)
            
            ciudades_existentes = Ciudad.objects.filter(region_id=region_id)
            for ciudad in ciudades_existentes:
                if normalizar_texto(ciudad.nombre) == nombre_normalizado:
                    return Response(
                        {"error": f"Ya existe una ciudad con el nombre '{nombre_ciudad}' en la región seleccionada"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = CiudadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(
        summary="Obtener una ciudad a través de su id", 
        tags=["Ciudades"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la ciudad a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Modificar una ciudad existente a través de su id", 
        tags=["Ciudades"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la ciudad a modificar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar una ciudad a través de su id",
        tags=["Ciudades"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la ciudad a eliminar'),
        ],
    )
)
class CiudadDetailView(APIView):  
    permission_classes=[EsSuperAdminOSoloLectura]  
    def put(self, request, pk):
        """Actualizar ciudad"""
        try:
         ciudad = Ciudad.objects.get(pk=pk)
        except Ciudad.DoesNotExist:
            return Response(
            {"error": "Ciudad no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = CiudadSerializer(ciudad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener una ciudad por su id"""
        try:
            ciudad = Ciudad.objects.get(pk=pk)
            serializer = CiudadSerializer(ciudad)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ciudad.DoesNotExist:
            raise Http404("Ciudad no encontrada")
    
    def delete(self,request, pk):
        """Eliminar una ciudad"""
        try:
            ciudad = Ciudad.objects.get(pk=pk)
            try:
                ciudad.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return Response(
                    {"error": "No se puede eliminar esta ciudad porque tiene comunas asociadas. Primero debe eliminar o reasignar las comunas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Ciudad.DoesNotExist:
            return Response(
            {"error": "Ciudad no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema_view(
    get=extend_schema(summary="Obtener un organismo responsable a través de su Id",
                      tags=["Organismos Responsables"]),
  
    put=extend_schema(summary="Actualizar un Organismo Responsable existente",
                      tags=["Organismos Responsables"], request=OrganismoResponsableSerializer),
    delete=extend_schema(summary="Eliminar un Organismo Responsable existente",
                         tags=["Organismos Responsables"])
)
class OrganismoResponsableDetailView(APIView):
    permission_classes=[EsSuperAdminOSoloLectura]
    def put(self, request, pk):
        """Actualizar organismo responsable"""
        try:
         org_responsable = OrganismoResponsable.objects.get(pk=pk)
        except OrganismoResponsable.DoesNotExist:
            return Response(
            {"error": "Organismo responsable no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = OrganismoResponsableSerializer(org_responsable, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener un organismo responsable por su id"""
        try:
            org_responsable = OrganismoResponsable.objects.get(pk=pk)
            serializer = OrganismoResponsableSerializer(org_responsable)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrganismoResponsable.DoesNotExist:
            raise Http404("Organismo responsable no encontrado")
    
    def delete(self,request, pk):
        """Eliminar un organismo responsable"""
        try:
            org_responsable = OrganismoResponsable.objects.get(pk=pk)
            try:
                org_responsable.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValidationError as e:
                return Response(
                    {"error": "No se puede eliminar este organismo porque tiene medidas asociadas. Primero debe eliminar o reasignar las medidas."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except OrganismoResponsable.DoesNotExist:
            return Response(
            {"error": "Organismo responsable no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema_view(
    get=extend_schema(
        summary="Listar todos los Organismos Responsables",
        tags=["Organismos Responsables"],
        parameters=[
            OpenApiParameter(name='nombre', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar organismos por nombre (búsqueda parcial, case-insensitive, ignora tildes)'),
        ],
    ),
    post=extend_schema(
        summary="Crear un nuevo Organismo Responsable",
        tags=["Organismos Responsables"], 
        request=OrganismoResponsableSerializer
    )
)
class OrganismoResponsableView(APIView):
    """
    API para listar los Organismos Responsables.

    Endpoints:
    - GET /organismos-responsables/: Listar Organismos Responsables.
    """
    permission_classes = [EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar Organismos Responsables.
        
        Parámetros de búsqueda:
        - nombre: Filtrar organismos por nombre (búsqueda parcial, case-insensitive, ignora tildes)

        Retorna:
        - Lista de Organismos Responsables en formato JSON.
        """
        organismos = OrganismoResponsable.objects.all()
        
        nombre = request.GET.get('nombre')
        if nombre:
            nombre_normalizado = normalizar_texto(nombre)
            organismos = [org for org in organismos 
                         if nombre_normalizado in normalizar_texto(org.nombre)]
            
        serializer = OrganismoResponsableSerializer(organismos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Crear un nuevo Organismo Responsable.

        Parámetros:
        - request.data: Datos del Organismo Responsable a crear.

        Retorna:
        - Datos del Organismo Responsable creado en formato JSON.
        - Codigo de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y codigo de estado HTTP 400 si la creacion falla.
        - Código de estado HTTP 409 si ya existe un organismo responsable con el mismo nombre.
        """
        nombre_organismo = request.data.get('nombre')
        
        if nombre_organismo:
            nombre_normalizado = normalizar_texto(nombre_organismo)
            
            organismos_existentes = OrganismoResponsable.objects.all()
            for organismo in organismos_existentes:
                if normalizar_texto(organismo.nombre) == nombre_normalizado:
                    return Response(
                        {"error": f"Ya existe un organismo responsable con el nombre '{nombre_organismo}'"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = OrganismoResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    Lista reportes
"""
class ReportePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    summary="Listar reportes con filtros",
    description="Permite listar reportes filtrando por organismo, estado y fecha de envío, y ordenarlos por estado o fecha.",
    tags=["Reportes"],  
    parameters=[
        OpenApiParameter(name='organismo', type=int, location=OpenApiParameter.QUERY, description='ID del organismo responsable'),
        OpenApiParameter(name='estado', type=str, location=OpenApiParameter.QUERY, description='Estado del reporte (pendiente, aprobado, rechazado)'),
        OpenApiParameter(name='fecha_envio', type=str, location=OpenApiParameter.QUERY, description='Fecha exacta de envío (YYYY-MM-DD)'),
        OpenApiParameter(name='ordering', type=str, location=OpenApiParameter.QUERY, description='Campo de ordenamiento, por ejemplo "-fecha_envio"'),
        OpenApiParameter(name='page', type=int, location=OpenApiParameter.QUERY, description='Número de página'),
        OpenApiParameter(name='page_size', type=int, location=OpenApiParameter.QUERY, description='Cantidad de elementos por página'),
    ]
)
class ReporteListView(generics.ListAPIView):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [EsRepOrgResOSoloLectura]

    def get(self, request):
        queryset = Reporte.objects.all()
        #si no es superusuario, solo sus reportes
        if not request.user.is_superuser:
            mis_orgs = request.user.groups.first().organismoresponsable_set.all()
            queryset = queryset.filter(organismo__in=mis_orgs)
        organismo_id = request.GET.get('organismo')
        estado = request.GET.get('estado')
        fecha_envio = request.GET.get('fecha_envio')
        ordering = request.GET.get('ordering')

        # Filtros con validación
        if organismo_id:
            if not organismo_id.isdigit():
                return Response({"error": "El ID de organismo debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(organismo_id=organismo_id)

        ESTADOS_VALIDOS = ["pendiente", "aprobado", "rechazado"]
        if estado:
            if estado not in ESTADOS_VALIDOS:
                return Response({"error": f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(estado=estado)

        if fecha_envio:
            try:
                fecha_obj = datetime.strptime(fecha_envio, "%Y-%m-%d").date()
                queryset = queryset.filter(fecha_envio=fecha_obj)
            except ValueError:
                return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Ordenamiento
        if ordering in ['fecha_envio', '-fecha_envio', 'estado', '-estado']:
            queryset = queryset.order_by(ordering)

        paginator = ReportePagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ReporteSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


@extend_schema_view(
    put=extend_schema(
        summary="Modificar estado de un reporte",
        description="Permite cambiar el estado de un reporte a aprobado, rechazado o pendiente. Se registra el cambio en historial.",
        tags=["Reportes"]
    )
)
class ReporteEstadoUpdateView(APIView):
    """
    Permite actualizar el estado de un reporte a "aprobado", "rechazado" o "pendiente".
    También registra la modificación en un historial para trazabilidad.
    """
    serializer_class = ReporteSerializer
    permission_classes = [EsAdminOSoloLectura]

    def put(self, request, id_reporte):
        try:
            reporte = Reporte.objects.get(id=id_reporte)
        except Reporte.DoesNotExist:
            return Response({"error": "Reporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        nuevo_estado = request.data.get("estado")
        ESTADOS_VALIDOS = ["pendiente", "aprobado", "rechazado"]

        if nuevo_estado not in ESTADOS_VALIDOS:
            return Response({"error": f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}"}, status=status.HTTP_400_BAD_REQUEST)

        if nuevo_estado == reporte.estado:
            return Response({
                "detail": "El reporte ya tiene ese estado.",
                "estado_actual": reporte.estado
            }, status=status.HTTP_400_BAD_REQUEST)

        if reporte.estado == "rechazado" and nuevo_estado == "aprobado":
            return Response({"error": "No se puede aprobar un reporte que fue rechazado previamente."}, status=status.HTTP_400_BAD_REQUEST)

        if reporte.estado == "aprobado" and nuevo_estado != "aprobado":
            return Response({"error": "No se puede modificar un reporte que ya fue aprobado."}, status=status.HTTP_400_BAD_REQUEST)

        estado_anterior = reporte.estado
        reporte.estado = nuevo_estado
        reporte.updated_by = request.user
        reporte.save()

        # Registro de trazabilidad
        HistorialEstadoReporte.objects.create(
            reporte=reporte,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            actualizado_por=request.user.username if request.user.is_authenticated else "Desconocido"
        )

        serializer = ReporteSerializer(reporte)
        return Response({
            "mensaje": "Estado actualizado correctamente",
            "estado_anterior": estado_anterior,
            "estado_nuevo": nuevo_estado,
            "reporte": serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="Listar todos los reportes",
        tags=["Reportes"]
    ),
)
class ReportesView(APIView):
    """
    Endpoint para listar todos los reportes.
    GET /api/reportes/
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        reportes = Reporte.objects.all()
        serializer = ReporteSerializer(reportes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        summary="Crear un nuevo reporte",
        tags=["Reportes"]
    ),
    get=extend_schema(
        summary="Obtener detalle de un reporte",
        tags=["Reportes"],
        parameters=[
            OpenApiParameter(name='id_reporte', type=int, location=OpenApiParameter.PATH, 
                           description='ID del reporte a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Actualizar un reporte existente",
        tags=["Reportes"],
        parameters=[
            OpenApiParameter(name='id_reporte', type=int, location=OpenApiParameter.PATH, 
                           description='ID del reporte a actualizar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar un reporte existente",
        tags=["Reportes"],
        parameters=[
            OpenApiParameter(name='id_reporte', type=int, location=OpenApiParameter.PATH, 
                           description='ID del reporte a eliminar'),
        ],
    )
)
class ReporteView(APIView):
    """
    Endpoint para gestionar operaciones CRUD sobre un reporte especifico.
    - POST /api/reporte/           -> Crear reporte.
    - GET /api/reporte/<id>        -> Obtener detalle.
    - PUT /api/reporte/<id>        -> Actualizar reporte.
    - DELETE /api/reporte/<id>     -> Eliminar reporte.
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [EsRepOrgResOSoloLectura]

    def post(self, request):
        serializer = ReporteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id_reporte=None):
        if not id_reporte:
            raise BadRequest("Se requiere un ID de reporte para esta operacion.")
        reporte = get_object_or_404(Reporte, id=id_reporte)
        serializer = ReporteSerializer(reporte)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id_reporte=None):
        if not id_reporte:
            raise BadRequest("Se requiere un ID de reporte para esta operacion.")
        reporte = get_object_or_404(Reporte, id=id_reporte)
        serializer = ReporteSerializer(reporte, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_reporte=None):
        if not id_reporte:
            raise BadRequest("Se requiere un ID de reporte para esta operacion.")
        reporte = get_object_or_404(Reporte, id=id_reporte)
        reporte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    get=extend_schema(
        summary="Listar todas las medidas", 
        tags=["Medidas"],
        parameters=[
            OpenApiParameter(name='nombre_corto', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar medidas por nombre corto (búsqueda parcial, case-insensitive, ignora tildes)'),
            OpenApiParameter(name='referencia_pda', type=str, location=OpenApiParameter.QUERY, 
                           description='Filtrar medidas por referencia PDA (búsqueda parcial, case-insensitive, ignora tildes)'),
            OpenApiParameter(name='plan_id', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar medidas por ID de plan PPDA'),
            OpenApiParameter(name='organismo_id', type=int, location=OpenApiParameter.QUERY, 
                           description='Filtrar medidas por ID de organismo responsable'),
        ],
    ),
    post=extend_schema(summary="Crear una nueva medidas", tags=["Medidas"], request=MedidaSerializer),
)
class MedidaView(APIView):
    serializer_class = MedidaSerializer
    permission_classes = [EsSuperAdminOSoloLectura]
    def get(self, request):
        """
        Listar todas las medidas.
        
        Parámetros de búsqueda:
        - nombre_corto: Filtrar medidas por nombre corto (búsqueda parcial, case-insensitive, ignora tildes)
        - referencia_pda: Filtrar medidas por referencia PDA (búsqueda parcial, case-insensitive, ignora tildes)
        - plan_id: Filtrar medidas por ID de plan PPDA
        - organismo_id: Filtrar medidas por ID de organismo responsable

        Retorna:
        - Lista de medidas en formato JSON.
        """
        medidas = Medida.objects.all()
        
        nombre_corto = request.GET.get('nombre_corto')
        if nombre_corto:
            nombre_normalizado = normalizar_texto(nombre_corto)
            medidas = [medida for medida in medidas 
                      if nombre_normalizado in normalizar_texto(medida.nombre_corto)]
        
        referencia_pda = request.GET.get('referencia_pda')
        if referencia_pda:
            referencia_normalizada = normalizar_texto(referencia_pda)
            medidas = [medida for medida in medidas 
                      if referencia_normalizada in normalizar_texto(medida.referencia_pda)]
        
        plan_id = request.GET.get('plan_id')
        if plan_id:
            medidas = [medida for medida in medidas 
                      if str(medida.plan.id) == plan_id]
        
        organismo_id = request.GET.get('organismo_id')
        if organismo_id:
            medidas = [medida for medida in medidas 
                      if any(str(org.id) == organismo_id for org in medida.organismos.all())]
            
        serializer = MedidaSerializer(medidas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crear una nueva medidas.

        Parámetros:
        - request.data: Datos de la medidas a crear.

        Retorna:
        - Datos de la medidas creada en formato JSON.
        - Código de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        - Código de estado HTTP 409 si ya existe una medida con los mismos valores en los campos referencia_pda, frecuencia_reporte, tipo_medida, plazo, plan y organismos.
        """
        referencia_pda = request.data.get('referencia_pda')
        frecuencia_reporte = request.data.get('frecuencia_reporte')
        tipo_medida = request.data.get('tipo_medida')
        plazo = request.data.get('plazo')
        plan_id = request.data.get('plan')
        organismos_ids = request.data.get('organismos', [])
        
        if referencia_pda and frecuencia_reporte and tipo_medida and plan_id and organismos_ids:
            medidas_existentes = Medida.objects.filter(
                referencia_pda=referencia_pda,
                frecuencia_reporte=frecuencia_reporte,
                tipo_medida=tipo_medida,
                plan_id=plan_id
            )
            
            if plazo:
                medidas_existentes = medidas_existentes.filter(plazo=plazo)
            
            for medida in medidas_existentes:
                medida_organismos_ids = set(medida.organismos.values_list('id', flat=True))
                if set(organismos_ids) == medida_organismos_ids:
                    return Response(
                        {"error": "Ya existe una medida con los mismos valores en los campos referencia_pda, frecuencia_reporte, tipo_medida, plazo, plan y organismos"},
                        status=status.HTTP_409_CONFLICT
                    )
        
        serializer = MedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(
        summary="Obtener una medidas por id", 
        tags=["Medidas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la medida a obtener'),
        ],
    ),
    put=extend_schema(
        summary="Modificar una medidas existente por su id", 
        tags=["Medidas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la medida a modificar'),
        ],
    ),
    delete=extend_schema(
        summary="Eliminar una medidas por su id",
        tags=["Medidas"],
        parameters=[
            OpenApiParameter(name='pk', type=int, location=OpenApiParameter.PATH, 
                           description='ID de la medida a eliminar'),
        ],
    )
)
class MedidaDetailView(APIView):
    permission_classes = [EsSuperAdminOSoloLectura]
    def put(self, request, pk):
        """Actualizar medidas"""
        try:
            medida = Medida.objects.get(pk=pk)
        except Medida.DoesNotExist:
            return Response(
            {"error": "Medida no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = MedidaSerializer(medida, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener una medidas por su id"""
        try:
            medida = Medida.objects.get(pk=pk)
            serializer = MedidaSerializer(medida)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Medida.DoesNotExist:
            raise Http404("Medida no encontrada")
    
    def delete(self,request, pk):
        """Eliminar medidas"""
        try:
            medida = Medida.objects.get(pk=pk)
            medida.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Medida.DoesNotExist:
            return Response(
            {"error": "Medida no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
