from django.db import migrations

def cargar_vehiculos_iniciales(apps, schema_editor):
    Vehiculo = apps.get_model('mi_app', 'Vehiculo')

    vehiculos_a_cargar = [
        Vehiculo(nombre='Auron City', categoria='baja', precio=8500000.00, img='imagenes/blanco.png'),
        Vehiculo(nombre='Velkar Nova', categoria='media', precio=12000000.00, img='imagenes/rojo.png'),
        Vehiculo(nombre='Oryex Prime', categoria='alta', precio=18500000.00, img='imagenes/azul.png'),
        Vehiculo(nombre='Zenthor', categoria='premium', precio=26000000.00, img='imagenes/negro.png'),
    ]

    Vehiculo.objects.bulk_create(vehiculos_a_cargar)

def revertir_carga(apps, schema_editor):
    Vehiculo = apps.get_model('mi_app', 'Vehiculo')
    Vehiculo.objects.filter(nombre__in=['Auron City', 'Velkar Nova', 'Oryex Prime', 'Zenthor']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_vehiculos_iniciales, revertir_carga),
    ]