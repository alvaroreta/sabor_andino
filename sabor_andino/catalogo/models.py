from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre del producto', max_length=100)
    linea = models.CharField('Línea', max_length=50)
    presentacion = models.CharField('Presentación', max_length=30)
    precio_lista_1 = models.DecimalField('Precio de lista', max_digits=10, decimal_places=2)
    stock_actual = models.PositiveIntegerField('Stock actual', default=0)
    url_fotografia = models.ImageField('Fotografía', upload_to='productos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"[{self.codigo_sku}] {self.nombre} - {self.presentacion}"

