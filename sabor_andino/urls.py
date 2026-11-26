"""
URL configuration for sabor_andino project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import include, path


def inicio(request):
    return redirect('login')


def perfil(request):
    return render(request, 'base.html')



urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', perfil, name='perfil'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('acopio/', include('acopio.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
