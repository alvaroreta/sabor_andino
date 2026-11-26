from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    nombre = models.CharField('Nombre', max_length=150)
    telefono = models.CharField('Teléfono', max_length=30)
    direccion = models.CharField('Dirección', max_length=200)
    rubro = models.CharField('Rubro', max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.rubro})"

class EstadoCalidad(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    APTA = 'APTA', 'Apta'
    RECHAZADA = 'RECHAZADA', 'Rechazada'

class MateriaPrima(models.Model):
    id_materia_prima = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='materias_primas',
        verbose_name='Proveedor'
    )
    nombre = models.CharField('Nombre de materia prima', max_length=100)
    stock_kilos = models.DecimalField('Stock en Kilos', max_digits=10, decimal_places=2, default=0.00)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    precio_compra = models.DecimalField('Precio de compra', max_digits=10, decimal_places=2)
    peso_grs = models.DecimalField('Peso en gramos', max_digits=10, decimal_places=2)
    estado_calidad = models.CharField(
        'Estado de calidad',
        max_length=20,
        choices=EstadoCalidad.choices,
        default=EstadoCalidad.PENDIENTE
    )

    def __str__(self):
        return f"{self.nombre} - {self.id_proveedor.nombre} ({self.get_estado_calidad_display()})"

class ComprobanteAcopio(models.Model):
    id_comprobante_acopio = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    id_proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='comprobantes_acopio',
        verbose_name='Proveedor'
    )
    fecha_emision = models.DateField('Fecha de emisión', auto_now_add=True)
    hora_emision = models.TimeField('Hora de emisión', auto_now_add=True)
    kilos_brutos = models.DecimalField('Kilos brutos', max_digits=10, decimal_places=2)
    tara = models.DecimalField('Tara', max_digits=10, decimal_places=2)
    kilos_netos = models.DecimalField('Kilos netos', max_digits=10, decimal_places=2, editable=False)
    porcentaje_humedad = models.DecimalField(
        'Porcentaje de humedad (%)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )

    def __str__(self):
        return f"ACO-{self.id_comprobante_acopio:05d} | {self.id_proveedor.nombre} ({self.fecha_emision})"

class DetalleAcopio(models.Model):
    id_detalle_acopio = models.AutoField(primary_key=True)
    is_active = models.BooleanField('Activo', default=True)
    id_comprobante_acopio = models.ForeignKey(
        ComprobanteAcopio,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Comprobante de Acopio'
    )
    id_materia_prima = models.ForeignKey(
        MateriaPrima,
        on_delete=models.PROTECT,
        related_name='detalles_acopio',
        verbose_name='Materia Prima'
    )
    kilos_recibidos = models.DecimalField('Kilos recibidos', max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle #{self.id_detalle_acopio} - Comprobante ACO-{self.id_comprobante_acopio.id_comprobante_acopio:05d}"
