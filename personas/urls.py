from django.urls import path
from .views import *

urlpatterns = [
    path('buscar_persona/', buscar_persona, name='buscar_persona'),
    path('', personas, name='lista_personas'),
    path('<int:dni>/', detalle_persona, name='detalle_persona'),
    path('agregar_editar/', agregar_editar_persona, name='agregar_editar_persona'),
]