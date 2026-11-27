from django.urls import path

from . import views

app_name = 'catalogo'

##--Crea URL de vista de producto mediante ID y de edición de precio
urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('<int:id_producto>/precio/', views.editar_precio, name='editar_precio'),
]
