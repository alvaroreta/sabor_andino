from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Proveedor, MateriaPrima, ComprobanteAcopio, DetalleAcopio
from .forms import ProveedorForm, MateriaPrimaForm, ComprobanteAcopioForm, DetalleAcopioForm


@login_required
def acopio_dashboard(request):
    comprobantes = ComprobanteAcopio.objects.select_related('id_proveedor').order_by('-fecha_emision', '-hora_emision')[:10]
    materias_primas = MateriaPrima.objects.select_related('id_proveedor').all()

    context = {
        'comprobantes': comprobantes,
        'materias_primas': materias_primas,
    }
    return render(request, 'acopio/acopio_dashboard.html', context)


@login_required
def crear_comprobante(request):
    if request.method == 'POST':
        form = ComprobanteAcopioForm(request.POST)
        if form.is_valid():
            comprobante = form.save(commit=False)
            # Asignación de seguridad para los kilos netos
            comprobante.kilos_netos = comprobante.kilos_brutos - comprobante.tara
            comprobante.save()
            
            messages.success(request, f'Comprobante ACO-{comprobante.id_comprobante_acopio:05d} registrado correctamente.')
            return redirect('acopio:acopio_dashboard')
        else:
            messages.error(request, 'Error al registrar el comprobante. Verifique los datos ingresados.')
    else:
        form = ComprobanteAcopioForm()

    return render(request, 'acopio/carga_acopio.html', {'form': form})


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