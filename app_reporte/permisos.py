"""
Definiciones de permisos de acceso para vistas
"""
from rest_framework import permissions

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
    Define un permiso parcial, para operaciones de escritura, 
    solo para miembros del grupo Representante Organismo Responsable
    """
    def has_permission(self, request, view):
        grupo_esperado = 'Representante Organismo Responsable'
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.groups.filter(name=grupo_esperado).exists()

class EsSuperAdminOSoloLectura(permissions.BasePermission):
    """
    Define un permiso parcial, para operaciones de escritura,
    solo para superadministradores.

    Util para recursos estaticos como regiones y otros, aunque se podría usar el panel de Django
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_superuser
