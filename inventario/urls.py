from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.lista_ajustes,
        name='lista_ajustes'
    ),
    path(
        'nuevo/',
        views.crear_ajuste,
        name='crear_ajuste'
    ),
]
