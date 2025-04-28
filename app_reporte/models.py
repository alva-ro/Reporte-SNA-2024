# app_reporte/models.py

from django.db import models
from django.contrib import admin
from django.utils.timezone import now
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    Modelo base abstracto que añade campos de auditoría.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,     null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True


class PlanPPDA(models.Model):
    """
    Representa el Plan de Prevención y Descontaminación Atmosférica que corresponde a cada comuna y región.
    Campos:
    - `nombre`: Nombre único del plan en donde se identifican las comunas correspondientes.
    - `mes_reporte`: Mes en el que se debe reportar el avance.
    - `anio`: Año del plan.
    """
    nombre = models.CharField(
        max_length=255,
        help_text="Ingrese el nombre único del Plan, identificando claramente las comunas que corresponden."
    )
    mes_reporte = models.IntegerField(
        help_text="Ingrese un valor",
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    anio = models.IntegerField()
    comunas = models.ManyToManyField('Comuna', related_name='planes')

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'anio', 'mes_reporte'],
                name='unique_plan_nombre_anio_mes'
            )
        ]

    def clean(self):
        super().clean()
        if self.pk:  # Solo validar si el objeto ya existe
            if Medida.objects.filter(plan=self).exists():
                raise ValidationError(
                    "No se puede eliminar este plan porque tiene medidas asociadas. "
                    "Primero debe eliminar o reasignar las medidas."
                )

    def delete(self, *args, **kwargs):
        self.clean()
        super().delete(*args, **kwargs)


class Region(models.Model):
    """
    Representa una región geográfica.

    Atributos:
        nombre (str): Nombre de la región.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.pk:  # Solo validar si el objeto ya exista
            if Ciudad.objects.filter(region=self).exists():
                raise ValidationError(
                    "No se puede eliminar esta región porque tiene ciudades asociadas. "
                    "Primero debe eliminar o reasignar las ciudades."
                )

    def delete(self, *args, **kwargs):
        self.clean()
        super().delete(*args, **kwargs)


class Ciudad(models.Model):
    """
    Representa una ciudad que pertenece a una región.

    Atributos:
        nombre (str): Nombre de la ciudad.
        region (ForeignKey): Región a la que pertenece la ciudad.
    """
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="ciudades")

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.pk:  # Solo validar si el objeto ya existe
            if Comuna.objects.filter(ciudad=self).exists():
                raise ValidationError(
                    "No se puede eliminar esta ciudad porque tiene comunas asociadas. "
                    "Primero debe eliminar o reasignar las comunas."
                )

    def delete(self, *args, **kwargs):
        self.clean()
        super().delete(*args, **kwargs)


class Comuna(models.Model):
    """
    Representa una comuna dentro de una ciudad.

    Atributos:
        nombre (str): Nombre de la comuna.
        ciudad (ForeignKey): Ciudad a la que pertenece la comuna.
    """
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.PROTECT, related_name='comunas')

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.pk:
            planes_asociados = self.planes.all()
            if planes_asociados.exists():
                raise ValidationError(
                    "No se puede eliminar la comuna porque está asociada a uno o más planes PPDA."
                )

    def delete(self, *args, **kwargs):
        planes_asociados = self.planes.all()
        if planes_asociados.exists():
            raise ValidationError(
                "No se puede eliminar la comuna porque está asociada a uno o más planes PPDA."
            )
        super().delete(*args, **kwargs)


class OrganismoResponsable(models.Model):
    """
    Representa un organismo responsable de implementar o verificar medidas del plan.

    Atributos:
        nombre (str): Nombre del organismo.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.pk:  # Solo validar si el objeto ya exista
            if Medida.objects.filter(organismos=self).exists():
                raise ValidationError(
                    "No se puede eliminar este organismo porque tiene medidas asociadas. "
                    "Primero debe eliminar o reasignar las medidas."
                )

    def delete(self, *args, **kwargs):
        self.clean()
        super().delete(*args, **kwargs)


class Medida(models.Model):
    """
    Representa una medida contenida en el plan PPDA.
    """
    FRECUENCIA_CHOICES = [
        ('anual', 'Anual'),
        ('unica', 'Única'),
        ('cada_5_anos', 'Cada 5 años'),
    ]

    TIPO_MEDIDA_CHOICES = [
        ('regulatoria', 'Regulatoria'),
        ('no_regulatoria', 'No Regulatoria'),
    ]

    referencia_pda = models.CharField(max_length=255)
    nombre_corto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    indicador = models.TextField()
    formula_calculo = models.TextField()
    frecuencia_reporte = models.CharField(max_length=50, choices=FRECUENCIA_CHOICES)
    tipo_medida = models.CharField(max_length=50, choices=TIPO_MEDIDA_CHOICES)
    plazo = models.DateField(blank=True, null=True)
    plan = models.ForeignKey('PlanPPDA', on_delete=models.PROTECT, related_name='medidas', null=False, blank=False)
    organismos = models.ManyToManyField('OrganismoResponsable', related_name='medidas')

    def __str__(self):
        return self.nombre_corto


class MedioVerificacion(models.Model):
    """
    Representa el medio por el cual se verifica el cumplimiento de una medida.

    Atributos:
        descripcion (str): Descripción del medio de verificación.
        tipo (str): Tipo del medio (informe, fotografía, oficio, etc.).
        medida (ForeignKey): Medida a la que pertenece este medio.
        entidad_a_cargo (ForeignKey): Entidad responsable de proporcionar el medio de verificación.
    """
    TIPO_MEDIO_CHOICES = [
        ('informe_anual', 'Informe Anual'),
        ('documento_excel', 'Documento Excel'),
        ('fotografia', 'Fotografía'),
        ('reporte', 'Reporte'),
        ('resolucion', 'Resolución'),
        ('registro_interno', 'Registro Interno'),
        ('oficio', 'Oficio'),
    ]

    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_MEDIO_CHOICES)
    medida = models.ForeignKey('Medida', on_delete=models.PROTECT, related_name='medios_verificacion')
    entidad_a_cargo = models.ForeignKey('Entidad', on_delete=models.PROTECT, null=True, blank=True, related_name='medios_verificacion')

    def __str__(self):
        return self.descripcion


class Entidad(models.Model):
    """
    Representa una entidad institucional que puede estar a cargo de medios de verificación.

    Atributos:
        nombre (str): Nombre de la entidad.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Reporte(TimeStampedModel):
    """
    Modelo para representar el reporte que un organismo responsable sube como avance de un plan.

    Consideraciones:
    - Se utiliza FileField para almacenar el archivo real (pdf, imagen, texto, etc).
    - Es necesario configurar MEDIA_URL y MEDIA_ROOT en settings.py para el manejo correcto de los archivos subidos.
    - Para evitar duplicados o validar condiciones específicas se pueden agregar validaciones adicionales en el Serializer o a nivel de modelo.
    """
    ESTADOS_REPORTE = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    medida = models.ForeignKey(
        'Medida',
        on_delete=models.PROTECT,
        related_name='reportes'
    )
    organismo = models.ForeignKey(
        'OrganismoResponsable',
        on_delete=models.PROTECT,
        related_name='reportes'
    )
    fecha_envio = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(
        upload_to='reportes/',
        null=True,
        blank=True,
        help_text="Archivo subido (pdf, imagen, documento, etc)"
    )
    medio_verificacion = models.ForeignKey(
        'MedioVerificacion',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='reportes'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_REPORTE,
        default='pendiente'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['medida', 'organismo', 'fecha_envio'],
                name='unique_reporte_medida_organismo_fecha'
            )
        ]

    def __str__(self):
        return f"Reporte de {self.organismo} sobre {self.medida} - {self.fecha_envio}"


class HistorialEstadoReporte(TimeStampedModel):
    """
    Registra los cambios de estado de los reportes para mantener trazabilidad.
    Guarda el estado anterior, el nuevo, quién lo modificó y cuándo.
    """
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    actualizado_por = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Cambio de Estado"
        verbose_name_plural = "Historiales de Cambios de Estado"

    def __str__(self):
        return f"{self.reporte.id}: {self.estado_anterior} → {self.estado_nuevo} ({self.fecha.date()})"
