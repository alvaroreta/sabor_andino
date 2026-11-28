from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/nuevo/', views.crear_lote, name='crear_lote'),
    path('lotes/<int:id_lote>/', views.detalle_lote, name='detalle_lote'),
]