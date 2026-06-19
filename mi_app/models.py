from django.db import models

class Vehiculo(models.Model):
    CATEGORIAS = [
        ('baja', 'Gama Baja'),
        ('media', 'Gama Media'),
        ('alta', 'Gama Alta'),
        ('premium', 'Premium'),
    ]
    nombre = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    img = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} (${self.precio:,.2f})"


class Garante(models.Model):
    EMPLEO_CHOICES = [
        ('dependencia', 'Relación de Dependencia'),
        ('independiente', 'Trabajador Independiente'),
    ]
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    tipo_empleo = models.CharField(max_length=20, choices=EMPLEO_CHOICES)
    antiguedad = models.IntegerField()
    ingreso = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Garante: {self.nombre} (Ingreso: ${self.ingreso:,.2f})"


class SolicitudSimulacion(models.Model):
    PLAN_CHOICES = [
        ('70/30', 'Plan 70/30'),
        ('80/20', 'Plan 80/20'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name="Vehículo")
    garante = models.OneToOneField(Garante, on_delete=models.CASCADE, verbose_name="Garante")

    titular_nombre = models.CharField(max_length=100)
    titular_dni = models.CharField(max_length=20)
    titular_telefono = models.CharField(max_length=20)
    titular_email = models.EmailField()
    titular_edad = models.IntegerField()
    titular_ingreso = models.DecimalField(max_digits=12, decimal_places=2)

    plan_tipo = models.CharField(max_length=10, choices=PLAN_CHOICES)
    cantidad_cuotas = models.IntegerField(default=84)
    es_calificado = models.BooleanField(default=False)
    valor_cuota_mensual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    motivos_rechazo = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Aprobado" if self.es_calificado else "Rechazado"
        return f"Simulación #{self.id} de {self.titular_nombre} - {estado}"