from django import forms
from .models import PlanillaCalidad
from acopio.models import DetalleAcopio
from produccion.models import Lote


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
        self.fields['id_detalle_acopio'].queryset = DetalleAcopio.objects.filter(is_active=True)
        self.fields['resultado'].choices = [
            ('APROBADO', 'Aprobado'),
            ('RECHAZADO', 'Rechazado'),
            ('PENDIENTE', 'Pendiente'),
        ]

class LiberacionLoteForm(forms.ModelForm):
    class Meta:
        model = PlanillaCalidad
        fields = ['id_lote', 'humedad_lab', 'granulometria', 'materia_extrana', 'resultado']
        widgets = {
            'id_lote': forms.Select(attrs={'class': 'form-select'}),
            'humedad_lab': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'granulometria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'materia_extrana': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'resultado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_lote'].empty_label = "Seleccione una opción"
        self.fields['id_lote'].queryset = Lote.objects.filter(
            is_active=True,
            estado_calidad=Lote.EstadoCalidad.PENDIENTE,
        )
        self.fields['resultado'].choices = [
            ('LIBERADO', 'Liberado'),
            ('RECHAZADO', 'Rechazado'),
        ]

