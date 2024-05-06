from django.conf import settings
from django.core import management
from datetime import datetime
import shutil
import zipfile
import os

APPS = ['personas', 'inmuebles', 'contratos'] # ADD APS TO BACKUP ( IN ORDER FOR FK RELATIONS TO WORK )

def get_backup_data():
    backup_folder = os.path.join(settings.BASE_DIR, 'backup')
    backups = os.listdir(backup_folder)

    if not len(backups) == 0:
        formato = "Backup_%Y-%m-%d_%H-%M-%S.zip"
        backups_dt = [datetime.strptime(backup, formato) for backup in backups]
    else:
        backups_dt = []
    return backup_folder, backups, backups_dt

def create_and_compress_backup(zip_name):
    backup_folder, _, _ = get_backup_data()

    files = []
    for app in APPS:
        output = os.path.join(backup_folder, f"{app}.json")
        management.call_command('dumpdata', app, output=output)
        files.append(output)
    management.call_command('mediabackup', output_filename="Media_Backup.tar")

    zip_path = os.path.join(backup_folder, zip_name)
    media_file = os.path.join(backup_folder, "Media_Backup.tar")

    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(media_file, os.path.basename("Media_Backup.tar"))
            i = 0
            for file in files:
                zipf.write(file, os.path.basename(APPS[i] + ".json"))
                i += 1

    except:
        for file in files:
            os.remove(file)
        os.remove(media_file)
        return False

    for file in files:
        os.remove(file)
    os.remove(media_file)
    return True

def get_backup(index = -1):
    try:
        backup_folder, backups, backups_dt = get_backup_data()
        path = os.path.join(backup_folder, backups[index])
        return True, path, backups[index], backups_dt[index]
    except:
        return False, None, None

def get_backup_list():
    _, _, backups_dt = get_backup_data()
    return backups_dt

def restore(bakcup_path):
    restore_folder = os.path.join(settings.BASE_DIR, 'restore')
    try:
        with zipfile.ZipFile(bakcup_path, 'r') as zipf:
            zipf.extractall(restore_folder)

        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

        management.call_command('flush', '--noinput')

        for app in APPS:
            input_path = os.path.join(restore_folder, f"{app}.json")
            management.call_command('loaddata', input_path)

        media_file = os.path.join(restore_folder, "Media_Backup.tar")
        management.call_command('mediarestore','--noinput', input_path=media_file)

    except Exception as e:
        print(e)
        shutil.rmtree(restore_folder)
        return False

    shutil.rmtree(restore_folder)
    return True