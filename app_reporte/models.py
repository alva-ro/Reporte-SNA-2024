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

    nombre = models.CharField(
        max_length=255,
        help_text="Ingrese el nombre único del Plan, identificando claramente las comunas que corresponden."
        )
    mes_reporte = models.IntegerField(
        help_text="Ingrese un valor"
    )
    anio = models.IntegerField()

    comunas = models.ManyToManyField('Comuna', related_name='planes')

    def __str__(self):
        return self.nombre

class Region(models.Model):
    """
    Representa una región administrativa del país.

    Atributos:
        nombre (str): Nombre de la región.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    """
    Representa una ciudad que pertenece a una región.

    Atributos:
        nombre (str): Nombre de la ciudad.
        region (ForeignKey): Región a la que pertenece la ciudad.
    """
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="ciudades")

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    """
    Representa una comuna dentro de una ciudad.

    Atributos:
        nombre (str): Nombre de la comuna.
        ciudad (ForeignKey): Ciudad a la que pertenece la comuna.
    """
    nombre = models.CharField(max_length=255)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE, related_name='comunas') 

    def __str__(self):
        return self.nombre

class OrganismoResponsable(models.Model):
    """
    Representa un organismo responsable de implementar o verificar medidas del plan.

    Atributos:
        nombre (str): Nombre del organismo.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Medida(models.Model):
    """
    Representa una medida contenida en el plan PPDA.

    Atributos:
        referencia_pda (str): Código o referencia del plan en el que se enmarca la medida.
        nombre_corto (str): Nombre breve que identifica la medida.
        descripcion (str): Descripción detallada de la medida.
        indicador (str): Indicador que permite evaluar el cumplimiento de la medida.
        formula_calculo (str): Fórmula usada para calcular el indicador.
        frecuencia_reporte (str): Frecuencia con la que se debe reportar la medida.
        tipo_medida (str): Indica si es una medida regulatoria o no regulatoria.
        plazo (date): Fecha límite para la ejecución de la medida.
        organismos (ManyToMany): Organismos responsables de la medida.
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
    medida = models.ForeignKey('Medida', on_delete=models.CASCADE, related_name='medios_verificacion')
    entidad_a_cargo = models.ForeignKey('Entidad', on_delete=models.SET_NULL, null=True, blank=True, related_name='medios_verificacion')

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


class Reporte(models.Model):
    ESTADOS_REPORTE = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    medida = models.ForeignKey('Medida', on_delete=models.CASCADE)
    organismo = models.ForeignKey('OrganismoResponsable', on_delete=models.CASCADE)
    fecha_envio = models.DateField()
    descripcion = models.TextField()
    archivo_url = models.URLField()
    medio_verificacion = models.ForeignKey('MedioVerificacion', null=True, blank=True, on_delete=models.SET_NULL)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_REPORTE,
        default='pendiente'
    )

    def __str__(self):
        return f"Reporte {self.id} - {self.estado}"
