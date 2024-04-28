from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils import agregar_actualizar_persona
from .models import Persona
from .forms import PersonaForm
from contratos.models import Contrato

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

def personas(request):
    personas = Persona.objects.all()

    context = {
        "personas": personas,
        "page": "datos"
    }
    return render(request, 'personas/list_personas.html', context)

def detalle_persona(request, dni):
    persona = get_object_or_404(Persona, dni = dni)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance = persona)
        if form.is_valid():
            form.save()
    else:
        form = PersonaForm(instance = persona)

    contratos = Contrato.objects.filter(
        Q(locador__dni=dni) |
        Q(locatario__dni=dni) |
        Q(garantia__dni=dni)
    )

    context = {
        'persona': persona,
        'form': form,
        'contratos': contratos
    }
    return render(request, 'personas/detalle_persona.html', context)

def agregar_editar_persona(request):
    valid, form = agregar_actualizar_persona(request)
    if valid:
        return redirect('detalle_persona', dni = form.cleaned_data['dni'])

    context = {
        'form': form,
        'page': 'datos',
    }
    return render(request, 'personas/agregar_editar_persona.html', context)