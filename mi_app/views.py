from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .forms import SimulacionForm
from .models import Vehiculo, Garante, SolicitudSimulacion
from .serializers import SolicitudSimulacionSerializer

def pagina_inicio(request):
    autos_db = Vehiculo.objects.all().order_by('precio')
    context = {
        'vehiculos': autos_db
    }
    return render(request, 'mi_app/index.html', context)

def procesar_simulacion(request):
    if request.method == 'POST':
        form = SimulacionForm(request.POST)

        if not form.is_valid():
            return JsonResponse({'success': False, 'errores': form.errors}, status=400)

        datos = form.cleaned_data
        cod_auto_slug = datos.get('modelo')
        nombre_auto = cod_auto_slug.replace('_', ' ').title()

        try:
            auto_db = Vehiculo.objects.get(nombre=nombre_auto)
        except Vehiculo.DoesNotExist:
            return JsonResponse({
                'success': False,
                'motivos': [f"El vehículo '{nombre_auto}' no está registrado en el sistema. Contacte al administrador."]
            }, status=200)

        precio_vehiculo = float(auto_db.precio)
        motivos_rechazo = []

        tipo_plan = datos['plan']
        cantidad_cuotas = 84
        tasa_interes = 0.065

        if datos['edad_g'] - datos['antiguedad_g'] < 17:
            motivos_rechazo.append("La antiguedad no corresponde con la edad del garante.")

        if datos['tipo_trabajo_g'] == 'dependencia' and datos['antiguedad_g'] < 1:
            motivos_rechazo.append("El Garante en relación de dependencia requiere mínimo 1 año de antigüedad.")
        elif datos['tipo_trabajo_g'] == 'independiente' and datos['antiguedad_g'] < 2:
            motivos_rechazo.append("El Garante independiente requiere mínimo 2 años de antigüedad.")


        porcentaje_financiado = 0.70 if tipo_plan == '70/30' else 0.80
        porcentaje_adjudicacion = 0.30 if tipo_plan == '70/30' else 0.20

        importe_financiado_base = precio_vehiculo * porcentaje_financiado
        importe_adjudicacion = precio_vehiculo * porcentaje_adjudicacion
        importe_retiro = precio_vehiculo * 0.08

        monto_interes_total = importe_financiado_base * tasa_interes
        monto_financiado_con_interes = importe_financiado_base + monto_interes_total
        valor_cuota_mensual = monto_financiado_con_interes / cantidad_cuotas

        ingreso_minimo_requerido_garante = valor_cuota_mensual * 4
        if datos['ingreso_g'] < ingreso_minimo_requerido_garante:
            motivos_rechazo.append(
                f"Los ingresos del Garante son insuficientes. Requiere un neto mínimo de ${ingreso_minimo_requerido_garante:,.2f} (4 veces el valor de la cuota).")

        garante_db = Garante.objects.create(
            nombre=datos['nombre_g'],
            edad=datos['edad_g'],
            tipo_empleo=datos['tipo_trabajo_g'],
            antiguedad=datos['antiguedad_g'],
            ingreso=datos['ingreso_g']
        )

        solicitud = SolicitudSimulacion(
            vehiculo=auto_db,
            garante=garante_db,
            titular_nombre=datos['nombre_t'],
            titular_dni=datos['dni_t'],
            titular_telefono=datos['telefono_t'],
            titular_email=datos['email_t'],
            titular_edad=datos['edad_t'],
            titular_ingreso=datos['ingreso_t'],
            plan_tipo=tipo_plan,
            es_calificado=len(motivos_rechazo) == 0,
            valor_cuota_mensual=valor_cuota_mensual,
            motivos_rechazo="\n".join(motivos_rechazo) if motivos_rechazo else None
        )
        solicitud.save()

        if motivos_rechazo:
            return JsonResponse({
                'success': False,
                'motivos': motivos_rechazo
            }, status=200)

        precio_formateado = f"${precio_vehiculo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        cuota_formateada = f"${valor_cuota_mensual:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        adj_formateado = f"${importe_adjudicacion:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        retiro_formateado = f"${importe_retiro:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        asunto_mail = f"Confirmación de tu Simulación - Plan {tipo_plan} ({nombre_auto})"

        cuerpo_mail = (
            f"Hola {datos['nombre_t']},\n\n"
            f"¡Felicitaciones! Tu solicitud de simulación para el vehículo {nombre_auto} "
            f"ha sido procesada y aprobada de forma exitosa en nuestro sistema.\n\n"
            f"A continuación, te detallamos los datos de tu Informe Final de Financiación:\n"
            f"--------------------------------------------------\n"
            f"• Vehículo Seleccionado: {nombre_auto}\n"
            f"• Valor del Vehículo: {precio_formateado}\n"
            f"• Tipo de Financiamiento: Plan {tipo_plan}\n"
            f"• Cantidad de Cuotas: 84 meses\n"
            f"• Tasa de Interés: 6.5% Fija\n"
            f"--------------------------------------------------\n"
            f"• Importe para Adjudicación: {adj_formateado}\n"
            f"• Importe para Retiro y Patentamiento: {retiro_formateado}\n"
            f"--------------------------------------------------\n"
            f"• VALOR DE LA CUOTA MENSUAL: {cuota_formateada}\n"
            f"--------------------------------------------------\n\n"
            f"Un asesor comercial se estará contactando con vos y tu garante ({datos['nombre_g']}) "
            f"al teléfono {datos['telefono_t']} para coordinar los pasos de la firma del contrato.\n\n"
            f"Gracias por confiar en nosotros.\n"
            f"Sistema de Gestión Web de Planes de Ahorro."
        )

        try:
            send_mail(
                subject=asunto_mail,
                message=cuerpo_mail,
                from_email=None,
                recipient_list=[datos['email_t']],
                fail_silently=False,
            )
        except Exception as error_smtp:
            print(f"Error al enviar el correo SMTP: {error_smtp}")

        return JsonResponse({
            'success': True,
            'informe': {
                'tipo_plan': f"Plan {tipo_plan}",
                'importe_adjudicacion': adj_formateado,
                'importe_retiro_patentamiento': retiro_formateado,
                'tasa_interes': "6.5% Fija",
                'valor_cuota_mensual': cuota_formateada,
                'vehiculo_valor': precio_formateado
            }
        })

    return JsonResponse({'success': False, 'error': 'Método no válido'}, status=405)

def es_administrador(user):
    return user.is_authenticated and user.is_staff


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_lista_solicitudes(request):
    solicitudes = SolicitudSimulacion.objects.select_related('vehiculo', 'garante').all().order_by('-fecha_creacion')

    serializer = SolicitudSimulacionSerializer(solicitudes, many=True)

    respuesta_data = {
        'success': True,
        'cantidad': len(serializer.data),
        'solicitudes': serializer.data
    }

    return Response(respuesta_data, status=status.HTTP_200_OK)