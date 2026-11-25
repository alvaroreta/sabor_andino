from django import forms
from .models import PlanillaCalidad


class ControlMateriaPrimaForm(forms.ModelForm):

    class Meta:
        model = PlanillaCalidad
        fields = [
            'id_detalle_acopio',
            'humedad_lab',
            'granulometria',
            'materia_extrana',
            'resultado',
        ]
        widgets = {
            'id_detalle_acopio': forms.Select(attrs={'class': 'form-select'}),
            'humedad_lab': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'granulometria': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'materia_extrana': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'resultado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_detalle_acopio'].empty_label = "Seleccione una opción"
        self.fields['resultado'].choices = [
            ('APROBADO', 'Aprobado'),
            ('RECHAZADO', 'Rechazado'),
            ('EN_OBSERVACION', 'En Observación'),
        ]

class LiberacionLoteForm(forms.ModelForm):
    class Meta:
        model = PlanillaCalidad
        fields = ['id_lote', 'resultado']
        widgets = {
            'id_lote': forms.Select(attrs={'class': 'form-select'}),
            'resultado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_lote'].empty_label = "Seleccione una opción"
        self.fields['resultado'].choices = [
            ('LIBERADO', 'Liberado'),
            ('RECHAZADO', 'Rechazado'),
        ]

