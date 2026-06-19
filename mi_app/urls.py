from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='index'),
    path('simulador/procesar/', views.procesar_simulacion, name='procesar_simulacion'),
    path('api/solicitudes/', views.api_lista_solicitudes, name='api_solicitudes')
]

