from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .decorators import roles_requeridos


@roles_requeridos('SOCIO_GERENTE')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/usuario_form.html', {'form': form})
