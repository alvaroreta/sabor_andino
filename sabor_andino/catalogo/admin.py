from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'linea', 'presentacion', 'precio_lista_1', 'stock_actual')
    list_filter = ('linea',)
    search_fields = ('nombre', 'linea', 'presentacion')
