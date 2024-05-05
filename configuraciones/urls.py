from django.urls import path
from .views import *

urlpatterns = [
    path('', configs, name='configs'),
    path('backup/', backup, name='backup'),
    path('descargar_backup/', descargar_backup, name='descargar_backup'),
    path('backup_list/', backup_list, name='backup_list'),
    path('eliminar_backup/', eliminar_backup, name='eliminar_backup')
]
