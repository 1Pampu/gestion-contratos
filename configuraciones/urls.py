from django.urls import path
from .views import *

urlpatterns = [
    path('', configs, name='configs'),
    path('backup/', backup, name='backup'),
    path('descargar_ultimo_backup/', descargar_ultimo_backup, name='descargar_ultimo_backup')
]
