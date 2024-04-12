from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('resumen_contrato/<int:id_contrato>/', resumen_contrato, name='resumen_contrato'),
    path('descargar_contrato/<int:id_contrato>/', descargar_contrato, name='descargar_contrato'),
    path('nuevo_contrato/locador', nuevo_contrato_locador, name='nuevo_contrato_locador'),
    path('nuevo_contrato/locatario', nuevo_contrato_locatario, name='nuevo_contrato_locatario'),
    path('nuevo_contrato/garantia', nuevo_contrato_garantia, name='nuevo_contrato_garantia'),
]