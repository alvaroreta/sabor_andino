from django.db import migrations


def backfill(apps, schema_editor):
    Lote = apps.get_model('produccion', 'Lote')
    PlanillaCalidad = apps.get_model('calidad', 'PlanillaCalidad')
    for lote in Lote.objects.all():
        planilla = PlanillaCalidad.objects.filter(
            id_lote_id=lote.pk,
            tipo_evaluacion='LOTE_PT',
            resultado__in=['LIBERADO', 'RECHAZADO'],
        ).order_by('-fecha_evaluacion', '-id_planilla_calidad').first()
        lote.estado_calidad = planilla.resultado if planilla else 'PENDIENTE'
        lote.save(update_fields=['estado_calidad'])


def reverse(apps, schema_editor):
    Lote = apps.get_model('produccion', 'Lote')
    Lote.objects.update(estado_calidad='PENDIENTE')


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0003_lote_estado_calidad'),
        ('calidad', '0003_alter_planillacalidad_resultado'),
    ]

    operations = [
        migrations.RunPython(backfill, reverse),
    ]
