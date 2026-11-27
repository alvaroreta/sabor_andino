from django.urls import path
from . import views

app_name = 'usuarios'

##-- Creación de URLS de "creación de usuario", "lista de usuarios del ssitema" y "Vista de perfiles de usuarios"
urlpatterns = [
    path('', views.lista_usuarios, name='lista'),
    path('crear/', views.crear_usuario, name='crear'),
    path('<int:user_id>/', views.perfil_usuario, name='detalle'),
]

