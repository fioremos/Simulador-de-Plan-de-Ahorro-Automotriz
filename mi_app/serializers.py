from rest_framework import serializers
from .models import SolicitudSimulacion, Vehiculo, Garante


class VehiculoSerializer(serializers.ModelSerializer):
    precio_lista = serializers.FloatField(source='precio')

    class Meta:
        model = Vehiculo
        fields = ['id', 'nombre', 'categoria', 'precio_lista']


class GaranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garante
        fields = ['id', 'nombre', 'edad', 'tipo_empleo', 'antiguedad', 'ingreso']


class SolicitudSimulacionSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%d/%m/%Y %H:%M')

    vehiculo = VehiculoSerializer(read_only=True)
    garante = GaranteSerializer(read_only=True)

    titular = serializers.SerializerMethodField()
    motivos_rechazo = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudSimulacion
        fields = ['id', 'fecha_creacion', 'es_calificado', 'motivos_rechazo',
                  'valor_cuota_mensual', 'titular', 'vehiculo', 'garante', 'plan_tipo']

    def get_titular(self, obj):
        return {
            'nombre': obj.titular_nombre,
            'dni': obj.titular_dni,
            'email': obj.titular_email,
            'telefono': obj.titular_telefono,
            'edad': obj.titular_edad,
            'ingreso': float(obj.titular_ingreso)
        }

    def get_motivos_rechazo(self, obj):
        return obj.motivos_rechazo.split('\n') if obj.motivos_rechazo else []