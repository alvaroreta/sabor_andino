from django import forms
from .models import Proveedor, MateriaPrima, ComprobanteAcopio, DetalleAcopio


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'direccion', 'rubro']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre / Razón Social'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'rubro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rubro'}),
        }


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['id_proveedor', 'nombre', 'stock_kilos', 'descripcion', 'precio_compra', 'peso_grs']
        widgets = {
            'id_proveedor': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pimentón Dulce'}),
            'stock_kilos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_grs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ComprobanteAcopioForm(forms.ModelForm):
    materia_prima = forms.ModelChoiceField(
        queryset=MateriaPrima.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Materia Prima Recibida'
    )
    precio_unitario = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        initial=0.00,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Precio Unitario ($)'
    )

    class Meta:
        model = ComprobanteAcopio
        fields = ['id_proveedor', 'materia_prima', 'kilos_brutos', 'tara', 'porcentaje_humedad', 'precio_unitario']
        widgets = {
            'id_proveedor': forms.Select(attrs={'class': 'form-select'}),
            'kilos_brutos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tara': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'porcentaje_humedad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class DetalleAcopioForm(forms.ModelForm):
    class Meta:
        model = DetalleAcopio
        fields = ['id_materia_prima', 'kilos_recibidos', 'precio_unitario']
        widgets = {
            'id_materia_prima': forms.Select(attrs={'class': 'form-select'}),
            'kilos_recibidos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }