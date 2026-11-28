from django import forms
from .models import Lote, ConsumoInsumoLote
from catalogo.models import Producto
from acopio.models import MateriaPrima

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['id_lote', 'id_producto', 'fecha_elaboracion', 'hora_elaboracion', 'cantidad_producto']
        widgets = {
            'fecha_elaboracion': forms.DateInput(attrs={'type': 'date'}),
            'hora_elaboracion': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_producto'].queryset = Producto.objects.filter(is_active=True)

class ConsumoInsumoLoteForm(forms.ModelForm):
    class Meta:
        model = ConsumoInsumoLote
        fields = ['id_materia_prima', 'cantidad_utilizada_kg']
        widgets = {
            'cantidad_utilizada_kg': forms.NumberInput(attrs={'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_materia_prima'].queryset = MateriaPrima.objects.filter(is_active=True)