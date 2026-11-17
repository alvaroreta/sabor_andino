from django.shortcuts import render

def control_materia_prima(request):
    return render(request, 'calidad/control_mp.html')

def liberar_lotes(request):
    return render(request, 'calidad/liberar_lotes.html')
    