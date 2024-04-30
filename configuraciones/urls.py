from django.urls import path
from .views import *

urlpatterns = [
    path('', configs, name='configs'),
    path('backup/', backup, name='backup'),
]
