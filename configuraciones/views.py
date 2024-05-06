from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from datetime import datetime
from .utils import create_and_compress_backup, get_backup, get_backup_list, restore
import os

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

    valid, backup_path, backup_name, _ = get_backup(index)
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

@require_POST
def eliminar_backup(request):
    try:
        index = int(request.POST.get('index', None))
        fecha = request.POST.get('fecha', None)
        valid, backup_path, _, backup_dt = get_backup(index)
        if not valid:
            return HttpResponseServerError('No se encontró la copia de seguridad.')

        fecha_dt = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S")
        if not backup_dt == fecha_dt:
            return HttpResponseServerError('Fecha inválida.')

        os.remove(backup_path)

    except:
        return HttpResponseServerError('Índice inválido.')

    return HttpResponse('Copia de seguridad eliminada correctamente.', 200)

@require_POST
def restaurar_backup(request):
    try:
        index = int(request.POST.get('index', None))
        fecha = request.POST.get('fecha', None)
        valid, backup_path, _, backup_dt = get_backup(index)
        if not valid:
            return HttpResponseServerError('No se encontró la copia de seguridad.')

        fecha_dt = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S")
        if not backup_dt == fecha_dt:
            return HttpResponseServerError('Fecha inválida.')

        restore(backup_path)

    except Exception as e:
        print(e)
        return HttpResponseServerError('Índice inválido.')

    return HttpResponse('Copia de seguridad restaurada correctamente.', 200)