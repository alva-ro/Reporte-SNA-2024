"""
Definiciones de permisos de acceso para vistas
"""
from rest_framework import permissions
from .models import OrganismoResponsable

class EsAdmin(permissions.BasePermission):
    """
    Define un permiso solo para administradores (Grupo)
    """
    def has_permission(self, request, view):
        grupo_esperado = 'Administrador'
        return request.user.groups.filter(name=grupo_esperado).exists()

class EsRepresentanteOrganismoResponsable(permissions.BasePermission):
    """
    Define un permiso solo para organismos responsables
    """
    def has_permission(self, request, view):
        grupo_esperado = 'Representante Organismo Responsable'
        return request.user.groups.filter(name=grupo_esperado).exists()

class EsAdminOSoloLectura(permissions.BasePermission):
    """
    Define un permiso parcial, para operaciones de escritura, 
    solo para miembros del grupo Administrador
    """
    def has_permission(self, request, view):
        grupo_esperado = 'Administrador'
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name=grupo_esperado).exists()

class EsRepOrgResOSoloLectura(permissions.BasePermission):
    """
    Permiso parcial: 
    - Lectura (GET, HEAD, OPTIONS): solo para el organismo al que pertenece el usuario.
    - Escritura: solo para miembros del grupo "Representante Organismo Responsable".
    """
    def has_permission(self, request, view):
        grupo_esperado = 'Representante Organismo Responsable'
        # lecturas permitidas a cualquiera autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # escrituras solo para el grupo
        return request.user and request.user.groups.filter(name=grupo_esperado).exists()

    def has_object_permission(self, request, view, obj):
        # para métodos de solo lectura, verificar que el objeto pertenezca al organismo del usuario
        if request.method in permissions.SAFE_METHODS:
            # obtenemos todos los nombres de grupos del usuario
            grupos_usuario = request.user.groups.values_list('name', flat=True)
            # buscamos el primer OrganismoResponsable cuyo nombre esté en sus grupos
            org = OrganismoResponsable.objects.filter(nombre__in=grupos_usuario).first()
            if not org:
                return False
            # comparamos con el organismo del objeto (Reporte u otro con atributo .organismo_id)
            return getattr(obj, 'organismo_id', None) == org.id
        # para escrituras reutilizamos la lógica de has_permission
        return self.has_permission(request, view)

class EsSuperAdminOSoloLectura(permissions.BasePermission):
    """
    Define un permiso parcial, para operaciones de escritura,
    solo para superadministradores.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser

class EsSuperAdmin(permissions.BasePermission):
    """
    Define un permiso solo para superadministradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
