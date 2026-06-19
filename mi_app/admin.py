from django.contrib import admin

from django.contrib import admin
from .models import Vehiculo, Garante, SolicitudSimulacion

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'img')
    list_editable = ('precio',)
    list_filter = ('categoria',)
    search_fields = ('nombre',)

    def precio_formateado(self, obj):
        return f"${obj.precio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    precio_formateado.short_description = 'Precio de Lista'

@admin.register(Garante)
class GaranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'edad', 'tipo_empleo', 'antiguedad', 'ingreso_formateado')
    list_filter = ('tipo_empleo',)
    search_fields = ('nombre',)

    def ingreso_formateado(self, obj):
        return f"${obj.ingreso:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ingreso_formateado.short_description = 'Ingreso Mensual Neto'

@admin.register(SolicitudSimulacion)
class SolicitudSimulacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha_creacion',
        'titular_nombre',
        'vehiculo',
        'plan_tipo',
        'cuota_formateada',
        'estado_calificacion'
    )

    list_filter = ('es_calificado', 'plan_tipo', 'fecha_creacion', 'vehiculo')

    search_fields = ('titular_nombre', 'titular_dni', 'vehiculo__nombre')

    ordering = ('-fecha_creacion',)

    fieldsets = (
        ('Información de Control', {
            'fields': ('fecha_creacion', 'es_calificado', 'motivos_rechazo')
        }),
        ('Datos Personales del Titular', {
            'fields': ('titular_nombre', 'titular_dni', 'titular_email', 'titular_telefono', 'titular_edad',
                       'titular_ingreso')
        }),
        ('Detalle del Financiamiento', {
            'fields': ('vehiculo', 'plan_tipo', 'valor_cuota_mensual')
        }),
        ('Garante Asociado', {
            'fields': ('garante',),
            'description': 'Clave foránea directa a la tabla relacional de garantes.'
        }),
    )

    readonly_fields = ('fecha_creacion', 'cuota_formateada', 'estado_calificacion')

    def cuota_formateada(self, obj):
        return f"${obj.valor_cuota_mensual:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    cuota_formateada.short_description = 'Cuota Calculada'

    def estado_calificacion(self, obj):
        return "APROBADO" if obj.es_calificado else "RECHAZADO"

    estado_calificacion.short_description = 'Estado Financiero'