from django import forms
from .models import Lote, ConsumoInsumoLote 

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['id_lote', 'id_producto', 'fecha_elaboracion', 'hora_elaboracion', 'cantidad_producto']
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'type': 'date'}),
            'hora_elaboracion': forms.TimeInput(attrs={'type': 'time'}),
        }
class ConsumoInsumoLoteForm(forms.ModelForm):
    class Meta:
        model = ConsumoInsumoLote
        fields = ['id_materia_prima', 'cantidad_utilizada_kg']
        widgets = {
            'cantidad_utilizada_kg': forms.NumberInput(attrs={'step': '0.01'})
        }