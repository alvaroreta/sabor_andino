from django.shortcuts import render, redirect, get_object_or_404
from usuarios.decorators import roles_requeridos
from .models import Lote, ConsumoInsumoLote
from .forms import ProduccionForm, ConsumoInsumoLoteForm

@roles_requeridos('JEFA_PLANTA', 'SOCIO_GERENTE')
def crear_lote(request):
    if request.method == 'POST':
        form = ProduccionForm(request.POST, request.FILES)
        if form.is_valid():
            lote = form.save()
            return redirect('produccion:detalle_lote', id_lote=lote.pk)
    else:
        form = ProduccionForm()
    return render(request, 'Produccion/crear_lote.html', {'form': form})

@roles_requeridos('JEFA_PLANTA', 'SOCIO_GERENTE')
def lista_lotes(request):
    lotes = Lote.objects.filter(is_active=True).select_related('id_producto').order_by('-fecha_elaboracion', '-hora_elaboracion')
    return render(request, 'Produccion/lista_lotes.html', {'lotes': lotes})

@roles_requeridos('JEFA_PLANTA', 'SOCIO_GERENTE')
def detalle_lote(request, id_lote):
    lote=get_object_or_404(Lote, pk=id_lote, is_active=True)

    if request.method == 'POST':
        form = ConsumoInsumoLoteForm(request.POST)
        if form.is_valid():
            consumo = form.save(commit=False)
            consumo.id_lote = lote
            consumo.save()
            return redirect('produccion:detalle_lote', id_lote=lote.pk)
    else:
        form = ConsumoInsumoLoteForm()
    consumos = lote.consumoinsumolote_set.select_related('id_materia_prima')
    return render(request, 'Produccion/detalle_lote.html',
    {'lote': lote,
    'form': form, 
    'consumos': consumos})