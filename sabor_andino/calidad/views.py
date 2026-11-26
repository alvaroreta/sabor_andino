from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ControlMateriaPrimaForm, LiberacionLoteForm
from .models import PlanillaCalidad

@login_required # comentario: Se requiere que el usuario esté autenticado para acceder a esta vista
def control_materia_prima(request):
    if request.method == 'POST':
        form = ControlMateriaPrimaForm(request.POST)
        if form.is_valid():
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
                mp.save()

            messages.success( #comentario: Se muestra un mensaje de éxito al usuario después de guardar el análisis de materia prima
                request, 'Análisis de materia prima guardado correctamente.'
            )
            return redirect('calidad:control_mp')
    else:
        form = ControlMateriaPrimaForm()

    return render(request, 'calidad/control_mp.html', {'form': form})


@login_required
def liberar_lote(request):
    if request.method == 'POST':
        form = LiberacionLoteForm(request.POST)
        if form.is_valid():
            planilla = form.save(commit=False)
            planilla.id_usuario = request.user
            planilla.tipo_evaluacion = PlanillaCalidad.TipoEvaluacion.LOTE_PT
            planilla.save()

            messages.success(request, 'Evaluación de lote registrada correctamente.')
            return redirect('calidad:liberar_lote')
    else:
        form = LiberacionLoteForm()

    return render(request, 'calidad/liberar_lotes.html', {'form': form})


@login_required
def historial_calidad(request):
    planillas = PlanillaCalidad.objects.filter(is_active=True).select_related(
        'id_usuario', 'id_detalle_acopio', 'id_lote'
    )
    return render(request, 'calidad/historial.html', {'planillas': planillas})

