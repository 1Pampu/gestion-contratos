from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from contratos.models import Contrato
from .models import Inmueble
from .utils import formatear_partida, agregar_actualizar_inmueble
from .forms import InmuebleForm

# Create your views here.
@require_POST
def buscar_inmueble(request):
    partida = str(request.POST.get('partida',""))
    partida = formatear_partida(partida)

    if partida >= 100:
        inmuebles = Inmueble.objects.filter(partida__startswith = partida)
        if inmuebles:
            if inmuebles[0].partida == partida:
                informacion_inmueble = {
                    'direccion': inmuebles[0].direccion,
                    'ciudad': inmuebles[0].ciudad,
                    'composicion': inmuebles[0].composicion,
                    'condicion': inmuebles[0].condicion
                }
                return JsonResponse({'inmueble': informacion_inmueble})

            partidas_inmuebles = [str(inmueble) for inmueble in inmuebles]
            return JsonResponse({'inmueble': partidas_inmuebles})

    return JsonResponse({'Error': 'No se ha encontrado el inmueble'})

def inmuebles(request):
    inmuebles = Inmueble.objects.all()

    context = {
        "inmuebles": inmuebles,
        "page": "datos"
    }
    return render(request, 'inmuebles/list_inmuebles.html', context)

def detalle_inmueble(request, partida):
    inmueble = get_object_or_404(Inmueble, partida = partida)
    if request.method == 'POST':
        request_updated = request.POST.copy()
        request_updated.update({'partida': partida})
        form = InmuebleForm(request_updated, instance = inmueble)
        if form.is_valid():
            form.save()
    else:
        form = InmuebleForm(instance = inmueble)

    contratos = Contrato.objects.filter(inmueble = inmueble)
    context= {
        'inmueble': inmueble,
        'form': form,
        'contratos': contratos
    }
    return render(request, 'inmuebles/detalle_inmueble.html', context)

def agregar_editar_inmueble(request):
    valid, form = agregar_actualizar_inmueble(request)
    if valid:
        return redirect('detalle_inmueble', partida = form.cleaned_data['partida'])

    context = {
        'form': form,
        'page': 'datos',
    }
    return render(request, 'inmuebles/agregar_editar_inmueble.html', context)