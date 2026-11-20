from django.urls import path
from . import views

app_name = 'calidad'

urlpatterns = [
    path('materia-prima/', views.control_materia_prima, name='control_mp'),
    path('liberar-lote/', views.liberar_lote, name='liberar_lote'),
    path('historial/', views.historial_calidad, name='historial'),
]
