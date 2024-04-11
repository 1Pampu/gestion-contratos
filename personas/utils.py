from .forms import PersonaForm
from .models import Persona

def agregar_actualizar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)

        if form.is_valid():
            form.save()
            return True, form
        else:
            dni = request.POST.get('dni', "")
            persona_existente = Persona.objects.filter(dni = dni).first()
            if persona_existente:
                form = PersonaForm(request.POST, instance = persona_existente)
                if form.is_valid():
                    form.save()

                    return True, form
    else:
        form = PersonaForm()
        return False, form