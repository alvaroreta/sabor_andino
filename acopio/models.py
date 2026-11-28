from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre / Razón Social', max_length=150)
    telefono = models.CharField('Teléfono de Contacto', max_length=50, blank=True, null=True)
    direccion = models.CharField('Dirección / Localidad', max_length=200, blank=True, null=True)
    rubro = models.CharField('Rubro / Actividad', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class MateriaPrima(models.Model):
    ESTADO_CALIDAD_CHOICES = [
        ('PENDIENTE', 'Pendiente de Control'),
        ('APTA', 'Apta'),
        ('RECHAZADA', 'Rechazada'),
    ]

    id_materia_prima = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='materias_primas', verbose_name='Proveedor')
    nombre = models.CharField('Nombre de Materia Prima', max_length=100)
    stock_kilos = models.DecimalField('Stock Actual (Kg)', max_digits=10, decimal_places=2, default=0.00)
    descripcion = models.TextField('Descripción / Observaciones', blank=True, null=True)
    precio_compra = models.DecimalField('Precio de Compra ($)', max_digits=10, decimal_places=2, default=0.00)
    peso_grs = models.DecimalField('Peso (Gramos)', max_digits=8, decimal_places=2, default=0.00)
    estado_calidad = models.CharField('Estado de Calidad', max_length=20, choices=ESTADO_CALIDAD_CHOICES, default='PENDIENTE')

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.id_proveedor.nombre}"


class ComprobanteAcopio(models.Model):
    id_comprobante_acopio = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='comprobantes', verbose_name='Proveedor')
    fecha_emision = models.DateField('Fecha de Emisión', auto_now_add=True)
    hora_emision = models.TimeField('Hora de Emisión', auto_now_add=True)
    kilos_brutos = models.DecimalField('Kilos Brutos', max_digits=10, decimal_places=2)
    tara = models.DecimalField('Tara (Kg)', max_digits=10, decimal_places=2)
    kilos_netos = models.DecimalField('Kilos Netos', max_digits=10, decimal_places=2, editable=False)
    porcentaje_humedad = models.DecimalField(
        'Porcentaje de Humedad (%)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )

    class Meta:
        verbose_name = 'Comprobante de Acopio'
        verbose_name_plural = 'Comprobantes de Acopio'
        ordering = ['-fecha_emision', '-hora_emision']

    def save(self, *args, **kwargs):
        # Cálculo automático de kilos netos antes de guardar en la base de datos
        if self.kilos_brutos is not None and self.tara is not None:
            self.kilos_netos = self.kilos_brutos - self.tara
        else:
            self.kilos_netos = 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ACO-{self.id_comprobante_acopio:05d} | {self.id_proveedor.nombre}"

class DetalleAcopio(models.Model):
    id_detalle_acopio = models.AutoField(primary_key=True)
    id_comprobante_acopio = models.ForeignKey(ComprobanteAcopio, on_delete=models.CASCADE, related_name='detalles', verbose_name='Comprobante')
    id_materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT, related_name='detalles_acopio', verbose_name='Materia Prima')
    kilos_recibidos = models.DecimalField('Kilos Recibidos', max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField('Precio Unitario ($)', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Acopio'
        verbose_name_plural = 'Detalles de Acopio'

    def __str__(self):
        return f"Detalle #{self.id_detalle_acopio} - Comprobante ACO-{self.id_comprobante_acopio.id_comprobante_acopio:05d}"