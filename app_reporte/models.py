from django.db import models
from django.contrib import admin

class PlanPPDA(models.Model):
    """
    Representa el Plan de Prevención y Descontaminación Atmosférica que corresponde a cada comuna y región.
    Campos:
    - `nombre`: Nombre único del plan en donde se identifican las comunas correspondientes.
    - `mes_reporte`: Mes en el que se debe reportar el avance.
    - `anio`: Año del plan.
    """

    nombre = models.CharField(max_length=255, help_text="Ingrese el nombre único del Plan, identificando claramente las comunas que corresponden.")
    mes_reporte = models.IntegerField()
    anio = models.IntegerField()

    comunas = models.ManyToManyField('Comuna', related_name='planes')

    def __str__(self):
        return self.nombre

class Region(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="ciudades")

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE, related_name='comunas') 

    def __str__(self):
        return self.nombre

class OrganismoResponsable(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Medida(models.Model):
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

    organismos = models.ManyToManyField('OrganismoResponsable', related_name='medidas')

    def __str__(self):
        return self.nombre_corto

class MedioVerificacion(models.Model):
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
    medida = models.ForeignKey('Medida', on_delete=models.CASCADE, related_name='medios_verificacion')
    entidad_a_cargo = models.ForeignKey('Entidad', on_delete=models.SET_NULL, null=True, blank=True, related_name='medios_verificacion')

    def __str__(self):
        return self.descripcion

class Entidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Reporte(models.Model):
    """
    Modelo para representar el reporte que un organismo responsable sube como avance de un plan.

    Consideraciones:
    - Se utiliza FileField para almacenar el archivo real (pdf, imagen, texto, etc).
    - Es necesario configurar MEDIA_URL y MEDIA_ROOT en settings.py para el manejo correcto de los archivos subidos.
    - Para evitar duplicados o validar condiciones específicas se pueden agregar validaciones adicionales en el Serializer o a nivel de modelo.
    """
    medida = models.ForeignKey(
        'Medida',
        on_delete=models.CASCADE,
        related_name='reportes'
    )
    organismo = models.ForeignKey(
        'OrganismoResponsable',
        on_delete=models.CASCADE,
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportes'
    )

    def __str__(self):
        return f"Reporte de {self.organismo} sobre {self.medida} - {self.fecha_envio}"
