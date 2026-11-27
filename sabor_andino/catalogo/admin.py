from django.contrib import admin

from .models import HistorialPrecio, Producto

##--Poder visualizar| editar| eliminar | actualizar la  tabla producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'linea', 'presentacion', 'precio_lista_1', 'stock_actual', 'is_active')
    list_filter = ('linea', 'is_active')
    search_fields = ('nombre', 'linea', 'presentacion')

##-- poder visualizar| editar| eliminar | actualizar la  visualizar tabla de historial de precios
@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ('id_historial', 'id_producto', 'precio_anterior', 'precio_nuevo', 'fecha_cambio', 'id_usuario')
    list_filter = ('fecha_cambio',)
    search_fields = ('id_producto__nombre', 'id_usuario__email')
    list_select_related = ('id_producto', 'id_usuario')
    ordering = ('-fecha_cambio',)
