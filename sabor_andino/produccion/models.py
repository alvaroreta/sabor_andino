from django.db import models
# Create your models here.

#Modelo de programacion previa a producir#
class Lote(models.Model):
    class EstadoCalidad(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        LIBERADO = 'LIBERADO', 'Liberado'
        RECHAZADO = 'RECHAZADO', 'Rechazado'

    id_lote = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    id_producto = models.ForeignKey('catalogo.Producto',
        on_delete=models.CASCADE, db_column= 'id_producto')
    fecha_elaboracion = models.DateField()
    hora_elaboracion = models.TimeField()
    cantidad_producto = models.DecimalField(max_digits=10, decimal_places=2)
    estado_calidad = models.CharField(
        'Estado de calidad',
        max_length=10,
        choices=EstadoCalidad.choices,
        default=EstadoCalidad.PENDIENTE
    )

    def __str__(self):
        return f"Lote #{self.id_lote} - {self.id_producto}"
    

#Modelo de consumo de insumos por lote luego de producir#
class ConsumoInsumoLote(models.Model):
    id_consumo = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE, db_column='id_lote')
    id_materia_prima = models.ForeignKey('acopio.MateriaPrima', on_delete=models.CASCADE, db_column='id_materia_prima')
    cantidad_utilizada_kg = models.DecimalField(max_digits=10, decimal_places=2)