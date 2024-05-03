from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from datetime import datetime
from .utils import create_and_compress_backup, get_last_backup, get_backup_list

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
def descargar_ultimo_backup(request):
    backup_path, backup_name = get_last_backup()

    if backup_path == None or backup_name == None:
        return HttpResponse('No hay copias de seguridad disponibles.', 404)

    with open(backup_path, 'rb') as doc:
        doc = doc.read()

    response = HttpResponse(doc, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{backup_name}"'
    return response

@require_GET
def backup_list(request):
    backup_list = get_backup_list()

    context = {
        'backup_list': backup_list
    }
    return JsonResponse(context)