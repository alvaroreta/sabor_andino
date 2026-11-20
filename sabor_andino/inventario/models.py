from django.db import models
from django.conf import settings


class AjusteStock(models.Model):

    class TipoAjuste(models.TextChoices):
        ALTA = 'ALTA', 'Alta'
        BAJA = 'BAJA', 'Baja'

    class Motivo(models.TextChoices):
        MERMA = 'MERMA', 'Merma'
        ROTURA = 'ROTURA', 'Rotura'
        DESECHO = 'DESECHO', 'Desecho'
        SALDO_INICIAL = 'SALDO_INICIAL', 'Saldo inicial'

    id_ajuste = models.AutoField(primary_key=True)

    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    id_materia_prima = models.ForeignKey(
        'acopio.MateriaPrima',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    id_producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    tipo_ajuste = models.CharField(
        max_length=4,
        choices=TipoAjuste.choices
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    motivo = models.CharField(
        max_length=20,
        choices=Motivo.choices
    )

    def __str__(self):
        return f"Ajuste {self.id_ajuste} - {self.tipo_ajuste} - {self.motivo}"

