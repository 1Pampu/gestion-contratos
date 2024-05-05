from django.conf import settings
from django.core import management
from datetime import datetime
import zipfile
import os

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

    management.call_command('dbbackup', output_filename="DB_Backup.dump")
    management.call_command('mediabackup', output_filename="Media_Backup.tar")

    zip_path = os.path.join(backup_folder, zip_name)
    db_file = os.path.join(backup_folder, "DB_Backup.dump")
    media_file = os.path.join(backup_folder, "Media_Backup.tar")

    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(db_file, os.path.basename("DB_Backup.dump"))
            zipf.write(media_file, os.path.basename("Media_Backup.tar"))

    except:
        os.remove(db_file)
        os.remove(media_file)
        return False

    os.remove(db_file)
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