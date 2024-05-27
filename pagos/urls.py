from django.urls import path
from .views import *

urlpatterns = [
    path("contrato/<int:id_contrato>", lista_pagos_contrato, name="lista_pagos_contrato"),
    path("<int:id_pago>/", pago, name="pago"),
    path("<int:id_pago>/pagar", pagar_cuota, name="pagar_cuota"),
]