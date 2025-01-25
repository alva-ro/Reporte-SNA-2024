from django.db import models

class PlanPPDA(models.Model):
    nombre = models.CharField(max_length=255)
    mes_reporte = models.IntegerField()
    anio = models.IntegerField()

    comunas = models.ManyToManyField('Comuna', related_name='planes')

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=255)

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
