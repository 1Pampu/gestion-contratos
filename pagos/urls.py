from django.urls import path
from .views import *

urlpatterns = [
    path("contrato/<int:id_contrato>/pagos/", lista_pagos_contrato, name="lista_pagos_contrato"),
    path("pago/<int:id_pago>/", pago, name="pago")
]