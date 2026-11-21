from django.shortcuts import render, redirect
from .forms import UsuarioForm
from django.contrib.auth.decorators import login_required


@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UsuarioForm()

    return render(request, 'usuarios/usuario_form.html', {'form': form})
