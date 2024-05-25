from django.shortcuts import render
from .models import Pago
from datetime import date

# Create your views here.
def lista_pagos_contrato(request, id_contrato):
    pagos = Pago.objects.filter(contrato = id_contrato).order_by('desde')

    context = {
        'pagos': pagos,
        'nav_cp': 'p',
        'contrato': pagos[0].contrato,
        'hoy': date.today(),
    }
    return render(request, 'pagos/lista_pagos_contratos.html', context)

def pago(request, id_pago):
    pago = Pago.objects.get(pk = id_pago)

    context = {
        'pago': pago,
        'nav_cp': 'p',
        'contrato': pago.contrato,
    }
    return render(request, 'pagos/resumen_pago.html', context)