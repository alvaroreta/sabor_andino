from django import forms
from .models import Proveedor, MateriaPrima, ComprobanteAcopio, DetalleAcopio


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'direccion', 'rubro']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre / Razón Social'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3874123456'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección / Localidad'}),
            'rubro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Productor Agrícola'}),
        }


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = ['id_proveedor', 'nombre', 'stock_kilos', 'descripcion', 'precio_compra', 'peso_grs', 'estado_calidad']
        widgets = {
            'id_proveedor': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pimentón o Ají'}),
            'stock_kilos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción u observaciones'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_grs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado_calidad': forms.Select(attrs={'class': 'form-select'}),
        }


class ComprobanteAcopioForm(forms.ModelForm):
    class Meta:
        model = ComprobanteAcopio
        fields = ['id_proveedor', 'kilos_brutos', 'tara', 'porcentaje_humedad']
        widgets = {
            'id_proveedor': forms.Select(attrs={'class': 'form-select'}),
            'kilos_brutos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Kilos brutos'}),
            'tara': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Tara'}),
            'porcentaje_humedad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00 a 100.00'}),
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