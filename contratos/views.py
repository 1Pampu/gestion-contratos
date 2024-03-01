from django.shortcuts import render
from .models import Contrato
from django.utils import timezone

# Create your views here.
def index(request):
    # Filtrar los contratos que ya finalizaron y conservar los vigentes
    contratos_activos = Contrato.objects.filter(fecha_finalizacion__lte = timezone.now())

    # Pasar los contratos a la plantilla
    context = {
        'contratos': contratos_activos
    }
    return render(request, 'contratos/index.html', context)