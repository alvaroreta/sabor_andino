from django.urls import path
from . import views

app_name = 'acopio'

urlpatterns = [
    # Dashboard principal de acopio
    path('', views.acopio_dashboard, name='acopio_dashboard'),

    # Comprobantes de pesaje en Cachi (HU-01)
    path('crear/', views.crear_comprobante, name='carga_acopio'),

    # Proveedores
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
]