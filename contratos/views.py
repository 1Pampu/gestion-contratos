from django.shortcuts import render, redirect
from .models import Contrato
from .forms import ContratoForm
from .utils import autocompletar_docx, numero_a_texto, fecha_a_texto, validaciones_contrato
from django.urls import reverse
from django.utils import timezone
from personas.utils import agregar_actualizar_persona, getPersona
from inmuebles.utils import agregar_actualizar_inmueble, getInmueble


# Create your views here.
def index(request):
    # Filtrar los contratos que ya finalizaron y conservar los vigentes
    contratos_activos = Contrato.objects.filter(fecha_finalizacion__gt = timezone.now()).order_by('-id')

    # Pasar los contratos a la plantilla
    context = {
        'contratos': contratos_activos,
        'page': 'index'
    }
    return render(request, 'contratos/index.html', context)

def resumen_contrato(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)

    context = {
        'contrato': contrato
    }
    return render(request, 'contratos/resumen_contrato.html', context)

def descargar_contrato(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)

    response = autocompletar_docx('static/documents/plantilla_contratos.docx', contrato)
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

    form = ContratoForm()
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.locador = getPersona(request.GET.get('locador'))
            contrato.locatario = getPersona(request.GET.get('locatario'))
            contrato.garantia = getPersona(request.GET.get('garantia'))
            contrato.inmueble = getInmueble(request.GET.get('inmueble'))
            contrato.save()
            return redirect('resumen_contrato', id_contrato=contrato.id)

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Terminos del Contrato',
    }
    return render(request, 'contratos/nuevo_contrato/terminos.html', context)