from django.urls import path
from .views import *

urlpatterns = [
    path('buscar_inmueble/', buscar_inmueble, name='buscar_inmueble'),
    path('', inmuebles, name='lista_inmuebles')
]