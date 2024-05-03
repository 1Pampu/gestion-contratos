from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from datetime import datetime
from .utils import create_and_compress_backup, get_backup, get_backup_list

# Create your views here.
def configs(request):
    return render(request, 'configuraciones/configs.html')

@require_GET
def backup(request):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")

    valid = create_and_compress_backup(f'Backup_{date}.zip')
    if not valid:
        return HttpResponseServerError('Error al realizar la copia de seguridad.')

    return HttpResponse('Copia de seguridad realizada correctamente.', 200)

@require_GET
def descargar_backup(request):
    try:
        index = int(request.GET.get('index', -1))
    except:
        return HttpResponseServerError('Índice inválido.')

    valid, backup_path, backup_name = get_backup(index)
    if not valid:
        return HttpResponseServerError('No se encontró la copia de seguridad.')

    with open(backup_path, 'rb') as doc:
        doc = doc.read()

    response = HttpResponse(doc, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{backup_name}"'
    return response

@require_GET
def backup_list(request):
    backup_list = get_backup_list()

    context = {
        'backup_list': backup_list
    }
    return JsonResponse(context)