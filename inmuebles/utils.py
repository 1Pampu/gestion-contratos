from .forms import InmuebleForm
from .models import Inmueble

def agregar_actualizar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)

        if form.is_valid():
            form.save()
            return True, form
        else:
            partida = request.POST.get('num_partida', "")
            partida_existente = Inmueble.objects.filter(num_partida = partida).first()
            if partida_existente:
                form = InmuebleForm(request.POST, instance = partida_existente)
                if form.is_valid():
                    form.save()

                    return True, form
    else:
        form = InmuebleForm()
    return False, form