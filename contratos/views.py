from django.shortcuts import render, redirect
from .models import Contrato
from .forms import ContratoForm
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

def nuevo_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():

            if not form.cleaned_data['locador']:
                pass






            return redirect('index')

    else:
        form = ContratoForm()

    context = {
        'form': form
    }
    return render(request, 'contratos/nuevo_contrato.html', context)