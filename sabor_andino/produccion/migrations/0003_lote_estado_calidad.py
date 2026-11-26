from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0002_is_active_soft_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='estado_calidad',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('LIBERADO', 'Liberado'), ('RECHAZADO', 'Rechazado')], default='PENDIENTE', max_length=10, verbose_name='Estado de calidad'),
        ),
    ]
