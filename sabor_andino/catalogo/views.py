from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from usuarios.decorators import roles_requeridos
from .forms import PrecioProductoForm
from .models import HistorialPrecio, Producto


@roles_requeridos('SOCIO_GERENTE')
def lista_productos(request):
    productos = Producto.objects.filter(is_active=True).order_by('nombre')
    return render(request, 'catalogo/lista.html', {'productos': productos})


@roles_requeridos('SOCIO_GERENTE')
def editar_precio(request, id_producto):
    producto = get_object_or_404(Producto, pk=id_producto, is_active=True)
    precio_anterior = producto.precio_lista_1

    if request.method == 'POST':
        form = PrecioProductoForm(request.POST, instance=producto)
        if form.is_valid():
            with transaction.atomic():
                producto = form.save()
                if producto.precio_lista_1 != precio_anterior:
                    HistorialPrecio.objects.create(
                        id_producto=producto,
                        precio_anterior=precio_anterior,
                        precio_nuevo=producto.precio_lista_1,
                        id_usuario=request.user,
                    )
            messages.success(request, 'Precio actualizado correctamente.')
            return redirect('catalogo:editar_precio', id_producto=producto.id_producto)
    else:
        form = PrecioProductoForm(instance=producto)

    historial = HistorialPrecio.objects.filter(
        id_producto=producto
    ).select_related('id_usuario')

    return render(request, 'catalogo/editar_precio.html', {
        'form': form,
        'producto': producto,
        'historial': historial,
    })
