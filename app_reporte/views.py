from django.core.exceptions import BadRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import PlanPPDA, Comuna, Region, Ciudad, OrganismoResponsable, Medida, MedioVerificacion, Reporte
from .serializers import PlanPPDASerializer, ComunaSerializer, RegionSerializer, \
    CiudadSerializer, OrganismoResponsableSerializer, MedidaSerializer, MedioVerificacionSerializer, EntidadSerializer, ReporteSerializer
from .models import Reporte
from .serializers import ReporteSerializer
from rest_framework.permissions import IsAdminUser


@extend_schema_view(
    get=extend_schema(summary="Listar todas las comunas", tags=["Comunas"]),
    post=extend_schema(summary="Crear una nueva comuna", tags=["Comunas"], request=ComunaSerializer),
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
    get=extend_schema(summary="Obtener una comuna por id", tags=["Comunas"]),
    put= extend_schema(summary="Modificar una comuna existente por su id", tags=["Comunas"]),
    delete=extend_schema(summary="Eliminar una comuna por su id",tags=["Comunas"] )
)
class ComunaDetailView(APIView):
    def put(self, request, pk):
        """Actualizar comuna"""
        try:
            comuna = Comuna.objects.get(pk=pk)
        except Comuna.DoesNotExist:
            return Response(
            {"error": "Comuna no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = ComunaSerializer(comuna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener una Comuna por su id"""
        try:
            comuna = Comuna.objects.get(pk=pk)
            serializer = ComunaSerializer(comuna)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comuna.DoesNotExist:
            raise Http404("Comuna no encontrada")
    
    def delete(self,request, pk):
        """Eliminar comuna"""
        try:
            comuna = Comuna.objects.get(pk=pk)
            comuna.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comuna.DoesNotExist:
            return Response(
            {"error": "Comuna no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
@extend_schema_view(
    get=extend_schema(summary="Listar todos los planes PPDA", tags=["Planes PPDA"]),
    post=extend_schema(summary="Crear un nuevo plan PPDA", tags=["Planes PPDA"], request=PlanPPDASerializer)
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
    get=extend_schema(summary="Obtener un plan PPDA a través de su id", tags=["Planes PPDA"]),
    put= extend_schema(summary="Modificar un plan PPDA existente a través de su id", tags=["Planes PPDA"]),
    delete=extend_schema(summary="Eliminar un plan PPDA a través de su id",tags=["Planes PPDA"] )
)
class PlanPPDADetailView(APIView):    
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
            planPPDA.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PlanPPDA.DoesNotExist:
            return Response(
            {"error": "Plan PPDA no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema_view(
    get=extend_schema(summary="Obtener una región a través de su id", tags=["Regiones"]),
    put= extend_schema(summary="Modificar una región existente a través de su id", tags=["Regiones"]),
    delete=extend_schema(summary="Eliminar una región a través de su id",tags=["Regiones"] )
)
class RegionDetailView(APIView):    
    def put(self, request, pk):
        """Actualizar región"""
        try:
         region = Region.objects.get(pk=pk)
        except Region.DoesNotExist:
            return Response(
            {"error": "Región no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        """Obtener una región por su id"""
        try:
            region = Region.objects.get(pk=pk)
            serializer = RegionSerializer(region)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Region.DoesNotExist:
            raise Http404("Región no encontrada")
    
    def delete(self,request, pk):
        """Eliminar región"""
        try:
            region = Region.objects.get(pk=pk)
            region.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Region.DoesNotExist:
            return Response(
            {"error": "Región no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
@extend_schema_view(
    get=extend_schema(summary="Obtener todas las regiones", tags=["Regiones"]),
    post=extend_schema(summary="Crear una nueva región", tags=["Regiones"], request=RegionSerializer)
)
class RegionView(APIView):
    serializer_class = RegionSerializer
    def get(self, request):
        """Listar todas las regiones"""
        regiones = Region.objects.all()
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
        """
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(summary="Listar todas las ciudades", tags=["Ciudades"]),
    post=extend_schema(summary="Crear una nueva ciudad", tags=["Ciudades"], request=CiudadSerializer)
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
        - Codigo de estado HTTP 201 si la creacion es exitosa.
        - Errores de validación y código de estado HTTP 400 si la creación falla.
        """
        serializer = CiudadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(summary="Obtener una ciudad a través de su id", tags=["Ciudades"]),
    put= extend_schema(summary="Modificar una ciudad existente a través de su id", tags=["Ciudades"]),
    delete=extend_schema(summary="Eliminar una ciudad a través de su id",tags=["Ciudades"] )
)
class CiudadDetailView(APIView):    
    def put(self, request, pk):
        """Actualizar ciudad"""
        try:
         ciudad = Ciudad.objects.get(pk=pk)
        except Ciudad.DoesNotExist:
            return Response(
            {"error": "Ciudad no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = CiudadSerializer(ciudad, data=request.data)
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
        """Eliminar ciudad"""
        try:
            ciudad = Ciudad.objects.get(pk=pk)
            ciudad.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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
    def put(self, request, pk):
        """Actualizar organismo responsable"""
        try:
         org_responsable = OrganismoResponsable.objects.get(pk=pk)
        except OrganismoResponsable.DoesNotExist:
            return Response(
            {"error": "Organismo responsable no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = OrganismoResponsableSerializer(org_responsable, data=request.data)
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
            org_responsable.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrganismoResponsable.DoesNotExist:
            return Response(
            {"error": "Organismo responsable no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema_view(
    get=extend_schema(summary="Listar todos los Organismos Responsables",
        tags=["Organismos Responsables"]),
    post=extend_schema(summary="Crear un nuevo Organismo Responsable",
        tags=["Organismos Responsables"], request=OrganismoResponsableSerializer)
)
class OrganismoResponsableView(APIView):
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
    
    def post(self, request):
        """
        Crear un nuevo Organismo Responsable.

        Parámetros:
        - request.data: Datos del Organismo Responsable a crear.

        Retorna:
        - Datos del Organismo Responsable creado en formato JSON.
        - Codigo de estado HTTP 201 si la creación es exitosa.
        - Errores de validación y codigo de estado HTTP 400 si la creacion falla.
        """
        serializer = OrganismoResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        tags=["Reportes"]
    ),
    put=extend_schema(
        summary="Actualizar un reporte existente",
        tags=["Reportes"]
    ),
    delete=extend_schema(
        summary="Eliminar un reporte existente",
        tags=["Reportes"]
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
    #permitir el manejo de archivos en la petición
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        serializer = ReporteSerializer(reporte, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_reporte=None):
        if not id_reporte:
            raise BadRequest("Se requiere un ID de reporte para esta operacion.")
        reporte = get_object_or_404(Reporte, id=id_reporte)
        reporte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@extend_schema_view(
    get=extend_schema(summary="Listar todas las medidas", tags=["Medidas"]),
    post=extend_schema(summary="Crear una nueva medidas", tags=["Medidas"], request=MedidaSerializer),
)
class MedidaView(APIView):
    serializer_class = MedidaSerializer
    def get(self, request):
        """
        Listar todas las medidas.

        Retorna:
        - Lista de medidas en formato JSON.
        """
        medidas = Medida.objects.all()
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
        """
        serializer = MedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema_view(
    get=extend_schema(summary="Obtener una medidas por id", tags=["Medidas"]),
    put= extend_schema(summary="Modificar una medidas existente por su id", tags=["Medidas"]),
    delete=extend_schema(summary="Eliminar una medidas por su id",tags=["Medidas"] )
)
class MedidaDetailView(APIView):
    def put(self, request, pk):
        """Actualizar medidas"""
        try:
            medida = Medida.objects.get(pk=pk)
        except Medida.DoesNotExist:
            return Response(
            {"error": "Medida no encontrada"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
        serializer = MedidaSerializer(medida, data=request.data)
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