from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pago
from .forms import PagarForm
from datetime import date, datetime
from .utils import generar_factura

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
        'hoy': date.today(),
    }
    return render(request, 'pagos/resumen_pago.html', context)

def pagar_cuota(request, id_pago):
    pago = Pago.objects.get(pk = id_pago)

    if pago.pago:
        return render(request, 'global/errors.html', {'error':'404','message': 'El pago ya fue realizado'})

    if request.method == 'POST':
        form = PagarForm(request.POST)
        if form.is_valid():
            formated_date = datetime.strptime(form.data['fecha_pago'], "%Y-%m-%d").date()
            pago.fecha_pago = formated_date

            if formated_date > pago.hasta:
                pago.vencido = True

            recargo = 0
            if pago.vencido:
                # ! LOGICA CALCULAR EL MONTO DE RECARGO
                pass

            salario_basico = float(form.data['salario_basico'])
            pago.salario_basico = salario_basico

            pago.monto = (salario_basico * (float(pago.contrato.porcentaje_pago) / 100)) + recargo

            pago.pago = True
            pago.save()
            generar_factura(pago)

            return redirect('pago', id_pago = id_pago)
    else:
        form = PagarForm()


    context = {
        'pago': pago,
        'form': form,
        'nav_cp': 'p',
        'contrato': pago.contrato,
    }
    return render(request, 'pagos/pagar_cuota.html', context)

def descargar_factura(request, id_pago):
    pago = Pago.objects.get(pk = id_pago)

    with open(pago.factura.path, 'rb') as pdf:
        pdf = pdf.read()

    nombre_archivo = pago.factura.name.split('/')[-1]

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response