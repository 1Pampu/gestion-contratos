from django.urls import path
from .views import *

urlpatterns = [
    path('buscar_persona/', buscar_persona, name='buscar_persona'),
]