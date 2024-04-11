from django.shortcuts import render, redirect
from .models import Contrato, Inmueble, Persona
from .forms import ContratoForm
from .utils import autocompletar_docx, numero_a_texto, fecha_a_texto
from django.utils import timezone
from personas.utils import agregar_actualizar_persona


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

    datos = {
        # Locador Info
        'nombre_locador' : contrato.locador.nombre.upper(),
        'dni_locador' : contrato.locador.dni,
        'email_locador' : contrato.locador.email,
        'celular_locador' : contrato.locador.celular,
        'domicilio_locador' : contrato.locador.domicilio,
        'ciudad_locador' : contrato.locador.ciudad,

        # Locatario Info
        'nombre_locatario' : contrato.locatario.nombre.upper(),
        'dni_locatario' : contrato.locatario.dni,
        'email_locatario' : contrato.locatario.email,
        'celular_locatario' : contrato.locatario.celular,
        'domicilio_locatario' : contrato.locatario.domicilio,
        'ciudad_locatario' : contrato.locatario.ciudad,

        # Garantia Info
        'nombre_garantia' : contrato.garantia.nombre.upper(),
        'dni_garantia' : contrato.garantia.dni,
        'email_garantia' : contrato.garantia.email,
        'celular_garantia' : contrato.garantia.celular,
        'domicilio_garantia' : contrato.garantia.domicilio,
        'ciudad_garantia' : contrato.garantia.ciudad,

        # Inmueble Info
        'direccion_inmueble' : contrato.inmueble.direccion,
        'ciudad_inmueble' : contrato.inmueble.ciudad,
        'num_partida' : contrato.inmueble.num_partida,
        'composicion_inmueble' : contrato.inmueble.composicion,

        # Contrato Info
        'fecha_inicio' : fecha_a_texto(contrato.fecha_inicio),
        'fecha_fin' : fecha_a_texto(contrato.fecha_finalizacion),
        'duracion_str' : numero_a_texto(contrato.duracion),
        'condicion_inmueble' : contrato.condicion,      # ! ATENTO CON ESTO SI LO CAMBIO
    }

    response = autocompletar_docx('static/documents/plantilla_contratos.docx', datos)
    return response

def nuevo_contrato_locador(request):
    valid, form = agregar_actualizar_persona(request)
    if valid:
        return redirect('nuevo_contrato_locatario')

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Locador',
    }
    return render(request, 'contratos/nuevo_contrato/personas.html', context)

def nuevo_contrato_locatario(request):
    valid, form = agregar_actualizar_persona(request)
    if valid:
        return redirect('index') #! CAMBIAR CUANDO ESTE LISTO GARANTE

    context = {
        'form': form,
        'page': 'nuevo_contrato',
        'title': 'Locatario',
    }
    return render(request, 'contratos/nuevo_contrato/personas.html', context)


# def nuevo_contrato(request):
#     if request.method == 'POST':
#         form = ContratoForm(request.POST)
#         if form.is_valid():

#             # Extraer informacion de el locador
#             if request.POST.get('locador-checkbox'):
#                 locador = Persona(
#                     nombre = form.cleaned_data['nombre_locador'],
#                     dni = form.cleaned_data['dni_locador'],
#                     email = form.cleaned_data['email_locador'],
#                     celular = form.cleaned_data['celular_locador'],
#                     domicilio = form.cleaned_data['domicilio_locador'],
#                     ciudad = form.cleaned_data['ciudad_locador']
#                 )
#             else:
#                 locador = form.cleaned_data['locador']

#             # Extraer informacion de el lacatario
#             if request.POST.get('locatario-checkbox'):
#                 locatario = Persona(
#                     nombre = form.cleaned_data['nombre_locatario'],
#                     dni = form.cleaned_data['dni_locatario'],
#                     email = form.cleaned_data['email_locatario'],
#                     celular = form.cleaned_data['celular_locatario'],
#                     domicilio = form.cleaned_data['domicilio_locatario'],
#                     ciudad = form.cleaned_data['ciudad_locatario']
#                 )
#             else:
#                 locatario = form.cleaned_data['locatario']

#             # Extraer informacion de el garante
#             if request.POST.get('garantia-checkbox'):
#                 garantia = Persona(
#                     nombre = form.cleaned_data['nombre_garantia'],
#                     dni = form.cleaned_data['dni_garantia'],
#                     email = form.cleaned_data['email_garantia'],
#                     celular = form.cleaned_data['celular_garantia'],
#                     domicilio = form.cleaned_data['domicilio_garantia'],
#                     ciudad = form.cleaned_data['ciudad_garantia']
#                 )
#             else:
#                 garantia = form.cleaned_data['garantia']

#             # Extraer informacion de el inmueble
#             if request.POST.get('inmueble-checkbox'):
#                 inmueble = Inmueble(
#                     direccion = form.cleaned_data['direccion_inmueble'],
#                     ciudad = form.cleaned_data['ciudad_inmueble'],
#                     num_partida = form.cleaned_data['num_partida_inmueble'],
#                     composicion = form.cleaned_data['composicion_inmueble']
#                 )
#             else:
#                 inmueble = form.cleaned_data['inmueble']

#             contrato = Contrato(
#                 locador = locador,
#                 locatario = locatario,
#                 garantia = garantia,
#                 inmueble = inmueble,
#                 condicion = form.cleaned_data['condicion'],
#                 fecha_inicio = form.cleaned_data['fecha_inicio'],
#                 duracion = form.cleaned_data['duracion']
#             )

#             if request.POST.get('locador-checkbox'):
#                 locador.save()
#             if request.POST.get('locatario-checkbox'):
#                 locatario.save()
#             if request.POST.get('garantia-checkbox'):
#                 garantia.save()
#             if request.POST.get('inmueble-checkbox'):
#                 inmueble.save()

#             contrato.save()

#             return redirect('resumen_contrato', id_contrato=contrato.id)
#     else:
#         form = ContratoForm()

#     context = {
#         'form': form,
#         'page': 'nuevo_contrato'
#     }
#     return render(request, 'contratos/nuevo_contrato.html', context)