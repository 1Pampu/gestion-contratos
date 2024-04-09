from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('nuevo_contrato/', nuevo_contrato, name='nuevo_contrato'),
    path('resumen_contrato/<int:id_contrato>/', resumen_contrato, name='resumen_contrato'),
    path('descargar_contrato/<int:id_contrato>/', descargar_contrato, name='descargar_contrato'),
    path('nuevo_contrato/locador', locador, name='locador'),
    path('buscar_persona/', buscar_persona, name='buscar_persona'), # ! CAMBIAR A MODULO PERSONA
]