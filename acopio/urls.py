from django.urls import path
from . import views

app_name = 'acopio'

urlpatterns = [
    path('', views.acopio_dashboard, name='acopio_dashboard'),
    path('crear/', views.crear_comprobante, name='carga_acopio'),
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('materias-primas/', views.lista_materias_primas, name='lista_materias_primas'),
    path('materias-primas/crear/', views.crear_materia_prima, name='crear_materia_prima'),
]