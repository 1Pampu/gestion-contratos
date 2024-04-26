from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Inmueble
from .utils import formatear_partida

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