from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Proveedor, MateriaPrima, ComprobanteAcopio, DetalleAcopio
from .forms import ProveedorForm, MateriaPrimaForm, ComprobanteAcopioForm, DetalleAcopioForm


@login_required
def acopio_dashboard(request):
    """
    Dashboard de Acopio. Muestra los comprobantes recientes incluyendo sus detalles de materia prima.
    """
    comprobantes = ComprobanteAcopio.objects.select_related('id_proveedor')\
                                            .prefetch_related('detalles__id_materia_prima')\
                                            .order_by('-fecha_emision', '-hora_emision')[:10]
    materias_primas = MateriaPrima.objects.select_related('id_proveedor').all()

    context = {
        'comprobantes': comprobantes,
        'materias_primas': materias_primas,
    }
    return render(request, 'acopio/acopio_dashboard.html', context)


@login_required
def crear_comprobante(request):
    """
    Registra el pesaje, genera el DetalleAcopio, incrementa stock_kilos 
    y asegura que estado_calidad quede en PENDIENTE.
    """
    if request.method == 'POST':
        form = ComprobanteAcopioForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # 1. Crear cabecera
                comprobante = form.save(commit=False)
                comprobante.kilos_netos = comprobante.kilos_brutos - comprobante.tara
                comprobante.save()

                # 2. Datos extra del formulario
                materia_prima = form.cleaned_data['materia_prima']
                precio_unitario = form.cleaned_data['precio_unitario']

                # 3. Crear DetalleAcopio
                DetalleAcopio.objects.create(
                    id_comprobante_acopio=comprobante,
                    id_materia_prima=materia_prima,
                    kilos_recibidos=comprobante.kilos_netos,
                    precio_unitario=precio_unitario
                )

                # 4. Sumar stock y forzar estado PENDIENTE
                materia_prima.stock_kilos += comprobante.kilos_netos
                materia_prima.estado_calidad = 'PENDIENTE'
                materia_prima.save()

            messages.success(request, f'Comprobante ACO-{comprobante.id_comprobante_acopio:05d} guardado correctamente. MP en estado Pendiente.')
            return redirect('acopio:acopio_dashboard')
        else:
            messages.error(request, 'Error al registrar el comprobante. Verifique los datos.')
    else:
        form = ComprobanteAcopioForm()

    return render(request, 'acopio/carga_acopio.html', {'form': form})


@login_required
def lista_materias_primas(request):
    materias_primas = MateriaPrima.objects.select_related('id_proveedor').all()
    return render(request, 'acopio/materias_primas_lista.html', {'materias_primas': materias_primas})


@login_required
def crear_materia_prima(request):
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST)
        if form.is_valid():
            mp = form.save(commit=False)
            mp.estado_calidad = 'PENDIENTE'
            mp.save()
            messages.success(request, f'Materia prima "{mp.nombre}" registrada en estado Pendiente.')
            return redirect('acopio:lista_materias_primas')
        else:
            messages.error(request, 'Error al registrar la materia prima.')
    else:
        form = MateriaPrimaForm()

    return render(request, 'acopio/materia_prima_form.html', {'form': form})


@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'acopio/proveedores_lista.html', {'proveedores': proveedores})


@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" registrado exitosamente.')
            return redirect('acopio:lista_proveedores')
        else:
            messages.error(request, 'Error al crear el proveedor.')
    else:
        form = ProveedorForm()

    return render(request, 'acopio/proveedor_form.html', {'form': form})