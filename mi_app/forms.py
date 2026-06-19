from django import forms
from django.core.validators import RegexValidator

validador_nombre = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
    message='El nombre no puede contener números ni caracteres especiales.',
    code='nombre_invalido'
)

validador_solo_numeros = RegexValidator(
    regex=r'^\d+$',
    message=None,
    code='solo_numeros'
)

class SimulacionForm(forms.Form):
    nombre_t = forms.CharField(
        max_length=100,
        validators=[validador_nombre],
        error_messages={
            'required': 'Por favor, ingresá el nombre completo del Titular.',
            'max_length': 'El nombre del titular es demasiado largo (máximo 100 caracteres).'
        }
    )
    dni_t = forms.CharField(
        max_length=8,
        validators=[validador_solo_numeros],
        error_messages={
            'required': 'El número de DNI del Titular es obligatorio.',
            'max_length': 'El DNI no puede superar los 8 caracteres.',
            'solo_numeros': 'El DNI no puede contener letras ni puntos.'
        }
    )
    telefono_t = forms.CharField(
        max_length=10,
        validators=[validador_solo_numeros],
        error_messages={
            'required': 'El teléfono de contacto del Titular es obligatorio.',
            'max_length': 'El teléfono debe ser válido.',
            'solo_numeros': 'El teléfono no puede contener letras ni puntos.'
        }
    )
    email_t = forms.EmailField(
        error_messages={
            'required': 'El correo electrónico del Titular es obligatorio.',
            'invalid': 'Ingresá una dirección de correo electrónico válida (ejemplo@dominio.com).'
        }
    )
    edad_t = forms.IntegerField(
        min_value=18,
        max_value=68,
        error_messages={
            'required': 'La edad del Titular es obligatoria.',
            'min_value': 'El Titular debe ser mayor de 18 años.',
            'max_value': 'El Titular superará los 75 años al finalizar el plan.',
            'invalid': 'Ingresá la edad del titular usando solo números enteros.'
        }
    )
    ingreso_t = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={
            'required': 'Los ingresos mensuales del Titular son obligatorios.',
            'invalid': 'Ingresá un monto numérico válido para los ingresos del titular.'
        }
    )

    nombre_g = forms.CharField(
        max_length=100,
        validators=[validador_nombre],
        error_messages={
            'required': 'Por favor, ingresá el nombre completo del Garante.',
            'max_length': 'El nombre del garante es demasiado largo (máximo 100 caracteres).'
        }
    )
    edad_g = forms.IntegerField(
        min_value=18,
        error_messages={
            'required': 'La edad del Garante es obligatoria.',
            'min_value': 'El Garante debe ser mayor de 18 años.',
            'invalid': 'Ingresá la edad del garante usando solo números.'
        }
    )
    tipo_trabajo_g = forms.ChoiceField(
        choices=[('dependencia', 'Relación de Dependencia'), ('independiente', 'Independiente')],
        error_messages={
            'required': 'Seleccioná el tipo de situación laboral del Garante.',
            'invalid_choice': 'La opción laboral seleccionada no es válida.'
        }
    )
    antiguedad_g = forms.IntegerField(
        min_value=0,
        error_messages={
            'required': 'La antigüedad laboral del Garante es obligatoria.',
            'min_value': 'La antigüedad laboral no puede ser un número negativo.',
            'invalid': 'Ingresá los años de antigüedad usando solo números.'
        }
    )
    ingreso_g = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={
            'required': 'El ingreso mensual neto del Garante es obligatorio.',
            'invalid': 'Ingresá un monto numérico válido para los ingresos del garante.'
        }
    )

    modelo = forms.CharField(
        max_length=50,
        error_messages={
            'required': 'No se detectó la selección de ningún vehículo. Hacé clic en una de las tarjetas del catálogo.'
        }
    )
    plan = forms.ChoiceField(
        choices=[('70/30', 'Plan 70/30'), ('80/20', 'Plan 80/20')],
        error_messages={
            'required': 'Seleccioná el tipo de plan de ahorro (70/30 u 80/20).',
            'invalid_choice': 'El tipo de plan seleccionado no es válido.'
        }
    )