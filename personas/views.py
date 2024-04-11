from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Persona

# Create your views here.
@require_POST
def buscar_persona(request):
    dni = str(request.POST.get('dni',""))

    if len(dni) >= 2:
        personas = Persona.objects.filter(dni__startswith = dni)
        if personas:
            if personas[0].dni == int(dni):
                informacion_persona = {
                    'nombre': personas[0].nombre,
                    'email': personas[0].email,
                    'celular': personas[0].celular,
                    'domicilio': personas[0].domicilio,
                    'ciudad': personas[0].ciudad
                }
                return JsonResponse({'persona': informacion_persona})

            dni_personas = list(personas.values_list('dni', flat=True))
            return JsonResponse({'persona': dni_personas})

    return JsonResponse({'Error': 'No se ha encontrado la persona'})