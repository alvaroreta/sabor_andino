from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UsuarioForm
from .decorators import roles_requeridos
from .models import Usuario

##-- Crea función de vista de perfil del usuario, solo restringida a usuarios logueados
@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html', {
        'perfil_usuario': request.user,
        'es_propio': True,
    })


##-- Crea vista de perfil de usuarios del sistema, restringido a SOCIO_GERENTE
@roles_requeridos('SOCIO_GERENTE')
def perfil_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    return render(request, 'usuarios/perfil.html', {
        'perfil_usuario': usuario,
        'es_propio': False,
    })


##-- Crea consulta a todos los usuarios activos del sistema (IS_ACTIVE == True)- Restringido a SOCIO_GERENTE
@roles_requeridos('SOCIO_GERENTE')
def lista_usuarios(request):
    usuarios = Usuario.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'usuarios/usuarios_lista.html', {'usuarios': usuarios})

##-- Creación de función de creación de usuario - Restringido a SOCIO_GERENTE
@roles_requeridos('SOCIO_GERENTE')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/usuario_form.html', {'form': form})
