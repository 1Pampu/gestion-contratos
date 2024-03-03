from django.shortcuts import render, redirect
from .models import Contrato, Inmueble, Persona
from .forms import ContratoForm
from django.utils import timezone

# Create your views here.
def index(request):
    # Filtrar los contratos que ya finalizaron y conservar los vigentes
    contratos_activos = Contrato.objects.filter(fecha_finalizacion__gt = timezone.now()).order_by('-id')

    # Pasar los contratos a la plantilla
    context = {
        'contratos': contratos_activos
    }
    return render(request, 'contratos/index.html', context)

def contrato(request, id_contrato):
    contrato = Contrato.objects.get(pk = id_contrato)

    context = {
        'contrato': contrato
    }
    return render(request, 'contratos/contrato.html', context)

def nuevo_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():

            if not form.cleaned_data['locador'] or form.cleaned_data.get('locador_checkbox'):
                locador = Persona(
                    nombre = form.cleaned_data['nombre_locador'],
                    dni = form.cleaned_data['dni_locador'],
                    email = form.cleaned_data['email_locador'],
                    celular = form.cleaned_data['celular_locador'],
                    domicilio = form.cleaned_data['domicilio_locador'],
                    ciudad = form.cleaned_data['ciudad_locador']
                )
                locador.save()
            else:
                locador = form.cleaned_data['locador']

            if not form.cleaned_data['locatario'] or form.cleaned_data.get('locatario_checkbox'):
                locatario = Persona(
                    nombre = form.cleaned_data['nombre_locatario'],
                    dni = form.cleaned_data['dni_locatario'],
                    email = form.cleaned_data['email_locatario'],
                    celular = form.cleaned_data['celular_locatario'],
                    domicilio = form.cleaned_data['domicilio_locatario'],
                    ciudad = form.cleaned_data['ciudad_locatario']
                )
                locatario.save()
            else:
                locatario = form.cleaned_data['locatario']

            if not form.cleaned_data['inmueble'] or form.cleaned_data.get('inmueble_checkbox'):
                inmueble = Inmueble(
                    direccion = form.cleaned_data['direccion_inmueble'],
                    ciudad = form.cleaned_data['ciudad_inmueble'],
                    num_partida = form.cleaned_data['num_partida_inmueble'],
                    composicion = form.cleaned_data['composicion_inmueble']
                )
                inmueble.save()
            else:
                inmueble = form.cleaned_data['inmueble']

            contrato = Contrato(
                locador = locador,
                locatario = locatario,
                inmueble = inmueble,
                condicion = form.cleaned_data['condicion'],
                fecha_inicio = form.cleaned_data['fecha_inicio'],
                duracion = form.cleaned_data['duracion']
            )
            contrato.save()

            return redirect('contrato', id_contrato=contrato.id)
    else:
        form = ContratoForm()

    context = {
        'form': form
    }
    return render(request, 'contratos/nuevo_contrato.html', context)