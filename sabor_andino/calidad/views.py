from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import ControlMateriaPrimaForm, LiberacionLoteForm
from .models import PlanillaCalidad
from produccion.models import Lote
from catalogo.models import Producto

ROLES_CALIDAD = {'SOCIO_GERENTE', 'RESP_CALIDAD', 'AUX_LABORATORIO'}


def rol_calidad_requerido(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.rol not in ROLES_CALIDAD:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


@rol_calidad_requerido
def control_materia_prima(request):
    if request.method == 'POST':
        form = ControlMateriaPrimaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                planilla = form.save(commit=False)
                planilla.id_usuario = request.user
                planilla.tipo_evaluacion = 'INGRESO_MP'
                planilla.save()

                detalle = planilla.id_detalle_acopio
                if detalle and detalle.id_materia_prima:
                    mp = detalle.id_materia_prima
                    if planilla.resultado == 'APROBADO':
                        mp.estado_calidad = 'APTA'
                    elif planilla.resultado == 'RECHAZADO':
                        mp.estado_calidad = 'RECHAZADA'
                    else:
                        mp.estado_calidad = 'PENDIENTE'
                    mp.save(update_fields=['estado_calidad'])

            messages.success(request, 'Análisis de materia prima guardado correctamente.')
            return redirect('calidad:control_mp')
    else:
        form = ControlMateriaPrimaForm()

    return render(request, 'calidad/control_mp.html', {'form': form})


@rol_calidad_requerido
def liberar_lote(request):
    if request.method == 'POST':
        form = LiberacionLoteForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                lote = Lote.objects.select_for_update().get(pk=form.cleaned_data['id_lote'].pk)
                if lote.estado_calidad != Lote.EstadoCalidad.PENDIENTE:
                    form.add_error('id_lote', 'El lote ya fue evaluado.')
                    return render(request, 'calidad/liberar_lotes.html', {'form': form})

                planilla = form.save(commit=False)
                planilla.id_usuario = request.user
                planilla.tipo_evaluacion = PlanillaCalidad.TipoEvaluacion.LOTE_PT
                planilla.save()

                lote.estado_calidad = planilla.resultado
                lote.save(update_fields=['estado_calidad'])

                if planilla.resultado == PlanillaCalidad.Resultado.LIBERADO:
                    producto = Producto.objects.select_for_update().get(pk=lote.id_producto_id)
                    producto.stock_actual += int(lote.cantidad_producto)
                    producto.save(update_fields=['stock_actual'])

            messages.success(request, 'Evaluación de lote registrada correctamente.')
            return redirect('calidad:liberar_lote')
    else:
        form = LiberacionLoteForm()

    return render(request, 'calidad/liberar_lotes.html', {'form': form})


@rol_calidad_requerido
def historial_calidad(request):
    planillas = PlanillaCalidad.objects.filter(is_active=True).select_related(
        'id_usuario', 'id_detalle_acopio', 'id_lote__id_producto'
    )
    return render(request, 'calidad/historial.html', {'planillas': planillas})
