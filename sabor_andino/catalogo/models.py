from django.db import models

##-- crea tabla Productos
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    linea = models.CharField(max_length=25)
    presentacion = models.CharField(max_length=50)
    precio_lista_1 = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.PositiveBigIntegerField(default = 0)
    fotografia = models.ImageField('Fotografía', upload_to='productos/', blank=True, null=True)


