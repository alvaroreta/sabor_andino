from django import forms

from .models import Producto


class PrecioProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['precio_lista_1']
        labels = {'precio_lista_1': 'Precio lista 1'}
        widgets = {
            'precio_lista_1': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}
            ),
        }

    def clean_precio_lista_1(self):
        precio = self.cleaned_data['precio_lista_1']
        if precio is None or precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio
