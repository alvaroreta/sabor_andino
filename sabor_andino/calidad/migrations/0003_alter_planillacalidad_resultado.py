from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calidad', '0002_is_active_soft_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planillacalidad',
            name='resultado',
            field=models.CharField(choices=[('APROBADO', 'Aprobado'), ('LIBERADO', 'Liberado'), ('RECHAZADO', 'Rechazado'), ('PENDIENTE', 'Pendiente'), ('EN_OBSERVACION', 'En Observación')], max_length=20, verbose_name='Resultado'),
        ),
    ]
