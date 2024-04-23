from .forms import InmuebleForm
from .models import Inmueble

def agregar_actualizar_inmueble(request):
    if request.method == 'POST':
        request_updated = request.POST.copy()
        partida = formatear_partida(request.POST.get('partida', ""))
        request_updated.update({'partida': partida})
        form = InmuebleForm(request_updated)

        if form.is_valid():
            form.save()
            return True, form
        else:
            partida_existente = Inmueble.objects.filter(partida = partida).first()
            if partida_existente:
                form = InmuebleForm(request_updated, instance = partida_existente)
                if form.is_valid():
                    form.save()
                    return True, form
    else:
        form = InmuebleForm()
    return False, form

def verificar_inmueble(partida):
    if partida:
        try:
            inmueble = Inmueble.objects.get(partida=partida)
            return True
        except Inmueble.DoesNotExist:
            return False
    return False

def formatear_partida(partida):
    try:
        formated = int(partida.replace("-", ""))
    except ValueError:
        return 0
    return formated

def getInmueble(PK):
    inmueble = Inmueble.objects.get(partida = PK)
    return inmueble