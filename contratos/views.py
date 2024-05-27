from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Contrato, ContratoDetalle
from .forms import ContratoForm
from .utils import autocompletar_docx_contrato, validaciones_contrato
from django.http import HttpResponse
from personas.utils import agregar_actualizar_persona, getPersona
from inmuebles.utils import agregar_actualizar_inmueble, getInmueble
from pagos.models import Pago

# Create your views here.
def index(request):
    contratos = Contrato.objects.filter(active = True).order_by('-id')

    context = {
        'contratos': contratos,
        'page': 'index'
    }
    return render(request, 'contratos/index.html', context)

def contratos_arhivados(request):
    contratos = Contrato.objects.filter(active = False).order_by('-id')

    context = {
        'contratos': contratos,
        'page': 'datos',
    }
    return render(request, 'contratos/index.html', context)

def alternar_archivado(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)
    if contrato.active:
        contrato.active = False
    else:
        contrato.active = True
    contrato.save()
    return redirect('index')

def resumen_contrato(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)
    detalle = ContratoDetalle.objects.get(contrato = contrato)
    personas = zip(['Locador', 'Locatario', 'Garantia'], [contrato.locador, contrato.locatario, contrato.garantia])

    context = {
        'contrato': contrato,
        'personas':personas,
        'detalle': detalle,
        'nav_cp': 'c'
    }
    return render(request, 'contratos/resumen_contrato.html', context)

def descargar_contrato(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)

    with open(contrato.docx.path, 'rb') as doc:
        doc = doc.read()

    nombre_archivo = contrato.docx.name.split('/')[-1]

    response = HttpResponse(doc, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response

def nuevo_contrato_locador(request):
    valid, form = agregar_actualizar_persona(request)
    if valid:
        dni_locador = form.cleaned_data['dni']
        url = reverse('nuevo_contrato_locatario') + f'?locador={dni_locador}'
        return redirect(url)

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Locador',
    }
    return render(request, 'contratos/nuevo_contrato/personas.html', context)

def nuevo_contrato_locatario(request):
    valid, url_or_error = validaciones_contrato(request, 1)
    if not valid:
        return render(request, 'global/errors.html', {'error': 404, 'mensaje': f'{url_or_error.capitalize()} no encontrado'})

    valid, form = agregar_actualizar_persona(request)
    if valid:
        dni_locatario = form.cleaned_data['dni']
        url = reverse('nuevo_contrato_garantia') + url_or_error + f'locatario={dni_locatario}'
        return redirect(url)

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Locatario',
    }
    return render(request, 'contratos/nuevo_contrato/personas.html', context)

def nuevo_contrato_garantia(request):
    valid, url_or_error = validaciones_contrato(request, 2)
    if not valid:
        return render(request, 'global/errors.html', {'error': 404, 'mensaje': f'{url_or_error.capitalize()} no encontrado'})

    valid, form = agregar_actualizar_persona(request)
    if valid:
        dni_garantia = form.cleaned_data['dni']
        url = reverse('nuevo_contrato_inmueble') + url_or_error + f'garantia={dni_garantia}'
        return redirect(url)

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Garantia',
    }
    return render(request, 'contratos/nuevo_contrato/personas.html', context)

def nuevo_contrato_inmueble(request):
    valid, url_or_error = validaciones_contrato(request, 3)
    if not valid:
        return render(request, 'global/errors.html', {'error': 404, 'mensaje': f'{url_or_error.capitalize()} no encontrado'})

    valid, form = agregar_actualizar_inmueble(request)
    if valid:
        num_partida = form.cleaned_data['partida']
        url = reverse('nuevo_contrato_final') + url_or_error + f'inmueble={num_partida}'
        return redirect(url)

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Inmueble',
    }
    return render(request, 'contratos/nuevo_contrato/inmueble.html', context)

def nuevo_contrato_final(request):
    valid, url_or_error = validaciones_contrato(request, 4)
    if not valid:
        return render(request, 'global/errors.html', {'error': 404, 'mensaje': f'{url_or_error.capitalize()} no encontrado'})

    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.locador = getPersona(request.GET.get('locador'))
            contrato.locatario = getPersona(request.GET.get('locatario'))
            contrato.garantia = getPersona(request.GET.get('garantia'))
            contrato.inmueble = getInmueble(request.GET.get('inmueble'))
            contrato.active = True
            contrato.save()
            autocompletar_docx_contrato(contrato)
            detalle = ContratoDetalle(contrato = contrato, composicion = contrato.inmueble.composicion, condicion = contrato.inmueble.condicion)
            detalle.save()
            for i in range(1, contrato.duracion + 1):
                pago = Pago(contrato = contrato, num_cuota = i)
                pago.save()
            return redirect('resumen_contrato', id_contrato=contrato.id)
    else:
        form = ContratoForm()

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Terminos del Contrato',
    }
    return render(request, 'contratos/nuevo_contrato/terminos.html', context)