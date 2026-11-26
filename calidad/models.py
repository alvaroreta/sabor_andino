from django.db import models
from django.conf import settings

class PlanillaCalidad(models.Model):
    class TipoEvaluacion(models.TextChoices):
        INGRESO_MP = 'INGRESO_MP', 'Ingreso de Materia Prima'
        LOTE_PT = 'LOTE_PT', 'Lote de Producto Terminado'

    class Resultado(models.TextChoices):
        APROBADO = 'APROBADO', 'Aprobado'
        LIBERADO = 'LIBERADO', 'Liberado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'
        EN_OBSERVACION = 'EN_OBSERVACION', 'En Observación'

    id_planilla_calidad = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Usuario evaluador')
    id_detalle_acopio = models.ForeignKey('acopio.DetalleAcopio', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Detalle de acopio')
    id_lote = models.ForeignKey('produccion.Lote', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Lote de producción')
    fecha_evaluacion = models.DateTimeField('Fecha de evaluación', auto_now_add=True)
    tipo_evaluacion = models.CharField('Tipo de evaluación', max_length=20, choices=TipoEvaluacion.choices)
    humedad_lab = models.DecimalField('Humedad laboratorio (%)', max_digits=5, decimal_places=2, null=True, blank=True)
    granulometria = models.DecimalField('Granulometría', max_digits=5, decimal_places=2, null=True, blank=True)
    materia_extrana = models.DecimalField('Materia extraña (%)', max_digits=5, decimal_places=2, null=True, blank=True)
    resultado = models.CharField('Resultado', max_length=20, choices=Resultado.choices)

    class Meta:
        verbose_name = 'Planilla de Calidad'; verbose_name_plural = 'Planillas de Calidad'
        ordering = ['-fecha_evaluacion']

    def __str__(self):
        return f'Planilla #{self.id_planilla_calidad} - {self.resultado}'
