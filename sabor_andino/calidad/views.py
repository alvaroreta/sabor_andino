from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ControlMateriaPrimaForm


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
            return redirect('control_materia_prima')
    else:
        form = ControlMateriaPrimaForm()

    return render(request, 'calidad/control_mp.html', {'form': form})


def liberar_lotes(request):
    return render(request, 'calidad/liberar_lotes.html')
