from django.urls import path
from .views import *

urlpatterns = [
    path('buscar_inmueble/', buscar_inmueble, name='buscar_inmueble'),
    path('', inmuebles, name='lista_inmuebles'),
    path('<int:partida>/', detalle_inmueble, name='detalle_inmueble'),
    path('agregar_editar/', agregar_editar_inmueble, name='agregar_editar_inmueble'),
]