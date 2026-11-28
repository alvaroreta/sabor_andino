
from django.shortcuts import render, redirect
from django.contrib import messages
from usuarios.decorators import roles_requeridos
from django.db import transaction

from .models import AjusteStock
from .forms import AjusteStockForm
from acopio.models import MateriaPrima
from catalogo.models import Producto


@roles_requeridos('ENC_DEPOSITO', 'SOCIO_GERENTE')
def lista_ajustes(request):
    ajustes = AjusteStock.objects.filter(is_active=True).select_related(
        'id_usuario',
        'id_materia_prima',
        'id_producto'
    ).order_by('-fecha')

    return render(
        request,
        'inventario/lista_ajustes.html',
        {'ajustes': ajustes}
    )


@roles_requeridos('ENC_DEPOSITO', 'SOCIO_GERENTE')
def crear_ajuste(request):
    if request.method == 'POST':
        form = AjusteStockForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                ajuste = form.save(commit=False)
                ajuste.id_usuario = request.user

                cantidad = ajuste.cantidad

                if ajuste.id_materia_prima:
                    materia_prima = MateriaPrima.objects.select_for_update().get(
                        pk=ajuste.id_materia_prima.pk
                    )

                    if ajuste.tipo_ajuste == AjusteStock.TipoAjuste.ALTA:
                        materia_prima.stock_kilos += cantidad

                    else:
                        if materia_prima.stock_kilos < cantidad:
                            form.add_error(
                                'cantidad',
                                'No hay suficiente stock de materia prima.'
                            )
                            return render(
                                request,
                                'inventario/crear_ajuste.html',
                                {'form': form}
                            )

                        materia_prima.stock_kilos -= cantidad

                    materia_prima.save(update_fields=['stock_kilos'])

                elif ajuste.id_producto:
                    producto = Producto.objects.select_for_update().get(
                        pk=ajuste.id_producto.pk
                    )

                    cantidad_entera = int(cantidad)

                    if ajuste.tipo_ajuste == AjusteStock.TipoAjuste.ALTA:
                        producto.stock_actual += cantidad_entera

                    else:
                        if producto.stock_actual < cantidad_entera:
                            form.add_error(
                                'cantidad',
                                'No hay suficiente stock del producto.'
                            )
                            return render(
                                request,
                                'inventario/crear_ajuste.html',
                                {'form': form}
                            )

                        producto.stock_actual -= cantidad_entera

                    producto.save(update_fields=['stock_actual'])

                ajuste.save()

            messages.success(request, 'El ajuste de stock se registró correctamente.')
            return redirect('lista_ajustes')

    else:
        form = AjusteStockForm()

    return render(
        request,
        'inventario/crear_ajuste.html',
        {'form': form}
    )

