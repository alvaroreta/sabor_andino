
from django import forms
from django.core.exceptions import ValidationError

from .models import AjusteStock
from acopio.models import MateriaPrima
from catalogo.models import Producto


class AjusteStockForm(forms.ModelForm):

    class Meta:
        model = AjusteStock

        fields = [
            'id_materia_prima',
            'id_producto',
            'tipo_ajuste',
            'cantidad',
            'motivo',
        ]

        labels = {
            'id_materia_prima': 'Materia prima',
            'id_producto': 'Producto',
            'tipo_ajuste': 'Tipo de ajuste',
            'cantidad': 'Cantidad',
            'motivo': 'Motivo del ajuste',
        }

        widgets = {
            'id_materia_prima': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'id_producto': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'tipo_ajuste': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'cantidad': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.01',
                    'step': '0.01',
                }
            ),
            'motivo': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_materia_prima'].queryset = MateriaPrima.objects.filter(is_active=True)
        self.fields['id_producto'].queryset = Producto.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()

        materia_prima = cleaned_data.get('id_materia_prima')
        producto = cleaned_data.get('id_producto')
        cantidad = cleaned_data.get('cantidad')

        if bool(materia_prima) == bool(producto):
            raise ValidationError(
                'Debe seleccionar una materia prima o un producto, '
                'pero no ambos.'
            )

        if cantidad is not None and cantidad <= 0:
            self.add_error(
                'cantidad',
                'La cantidad debe ser mayor que cero.'
            )

        if producto and cantidad is not None:
            if cantidad != cantidad.to_integral_value():
                self.add_error(
                    'cantidad',
                    'La cantidad de productos debe ser un número entero.'
                )

        return cleaned_data
