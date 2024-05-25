from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('resumen_contrato/<int:id_contrato>/', resumen_contrato, name='resumen_contrato'),
    path('descargar_contrato/<int:id_contrato>/', descargar_contrato, name='descargar_contrato'),
    path('nuevo_contrato/locador', nuevo_contrato_locador, name='nuevo_contrato_locador'),
    path('nuevo_contrato/locatario', nuevo_contrato_locatario, name='nuevo_contrato_locatario'),
    path('nuevo_contrato/garantia', nuevo_contrato_garantia, name='nuevo_contrato_garantia'),
    path('nuevo_contrato/inmueble', nuevo_contrato_inmueble, name='nuevo_contrato_inmueble'),
    path('nuevo_contrato/final', nuevo_contrato_final, name='nuevo_contrato_final'),
    path('archivados/', contratos_arhivados, name="contratos_archivados"),
    path('archivar/<int:id_contrato>/', alternar_archivado, name='archivar_contrato'),
]