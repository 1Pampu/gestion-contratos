from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core import management
from datetime import datetime
from .utils import compress_backup, get_last_backup

# Create your views here.
def configs(request):
    return render(request, 'configuraciones/configs.html')

@require_GET
def backup(request):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")

    try:
        management.call_command('dbbackup', output_filename="DB_Backup.dump")
        management.call_command('mediabackup', output_filename="Media_Backup.tar")

        compress_backup(["DB_Backup.dump", "Media_Backup.tar"], f'Backup_{date}.zip')

    except:
        return HttpResponse('Error al realizar la copia de seguridad.', 500)

    return HttpResponse('Copia de seguridad realizada correctamente.', 200)

@require_GET
def descargar_ultimo_backup(request):
    backup_path, backup_name = get_last_backup()
    with open(backup_path, 'rb') as doc:
        doc = doc.read()

    response = HttpResponse(doc, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{backup_name}"'
    return response