from django.db import models
# Create your models here.

class Lote(models.Model):
    id_lote = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('catalogo.Producto',
        on_delete=models.CASCADE, db_column= 'id_producto')
    fecha_elaboracion = models.DateField()
    hora_elaboracion = models.TimeField()
    cantidad_producto = models.DecimalField(max_digits=10, decimal_places=2)
    

class ConsumoInsumoLote(models.Model):
    id_consumo = models.AutoField(primary_key=True)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE, db_column='id_lote')
    id_materia_prima = models.ForeignKey('acopio.MateriaPrima', on_delete=models.CASCADE, db_column='id_materia_prima')
    cantidad_utilizada_kg = models.DecimalField(max_digits=10, decimal_places=2)