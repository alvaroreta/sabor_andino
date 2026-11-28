from django.contrib import admin
from .models import PlanillaCalidad


@admin.register(PlanillaCalidad)
class PlanillaCalidadAdmin(admin.ModelAdmin):
    list_display = (
        'id_planilla_calidad',
        'tipo_evaluacion',
        'resultado',
        'id_usuario',
        'id_detalle_acopio',
        'id_lote',
        'fecha_evaluacion',
        'is_active',
    )
    list_filter = ('tipo_evaluacion', 'resultado', 'is_active')
    search_fields = ('id_usuario__email', 'id_lote__id_producto__nombre')
    list_select_related = ('id_usuario', 'id_detalle_acopio', 'id_lote')
    ordering = ('-fecha_evaluacion',)
