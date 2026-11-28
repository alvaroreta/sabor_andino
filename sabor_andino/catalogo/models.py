from django.conf import settings
from django.db import models

##-- Creación de tabla productos
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
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
        return f"{self.nombre} - {self.presentacion}"

##--Creación de tabla de precios historicos
class HistorialPrecio(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='historial_precios'
    )
    precio_anterior = models.DecimalField('Precio anterior', max_digits=10, decimal_places=2)
    precio_nuevo = models.DecimalField('Precio nuevo', max_digits=10, decimal_places=2)
    fecha_cambio = models.DateTimeField('Fecha de cambio', auto_now_add=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Historial de precio'
        verbose_name_plural = 'Historial de precios'
        ordering = ['-fecha_cambio']

    def __str__(self):
        return f"{self.id_producto} - {self.precio_anterior} -> {self.precio_nuevo}"

