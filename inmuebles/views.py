from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Inmueble

# Create your views here.
@require_POST
def buscar_inmueble(request):
    partida = str(request.POST.get('num_partida',""))

    if len(partida) >= 2:
        inmuebles = Inmueble.objects.filter(num_partida__startswith = partida)
        if inmuebles:
            if inmuebles[0].num_partida == partida:
                informacion_inmueble = {
                    'direccion': inmuebles[0].direccion,
                    'ciudad': inmuebles[0].ciudad,
                    'composicion': inmuebles[0].composicion,
                    'condicion': inmuebles[0].condicion
                }
                return JsonResponse({'inmueble': informacion_inmueble})

            partidas_inmuebles = list(inmuebles.values_list('num_partida', flat=True))
            return JsonResponse({'inmueble': partidas_inmuebles})

    return JsonResponse({'Error': 'No se ha encontrado el inmueble'})