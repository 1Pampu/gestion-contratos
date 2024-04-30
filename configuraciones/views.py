from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.core import management
from datetime import datetime

# Create your views here.
def configs(request):
    return render(request, 'configuraciones/configs.html')

@require_GET
def backup(request):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")

    try:
        dbfile = 'DB_Backup_' + date + '.dump'
        management.call_command('dbbackup', output_filename=dbfile)

        MediaFile = 'Media_Backup_' + date + '.tar'
        management.call_command('mediabackup', output_filename=MediaFile)

    except:
        return HttpResponse('Error al realizar la copia de seguridad.', 500)

    return HttpResponse('Copia de seguridad realizada correctamente.', 200)