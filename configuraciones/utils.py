from django.conf import settings
from datetime import datetime
import zipfile
import os

def compress_backup(files, zip_name):
    backup_folder = os.path.join(settings.BASE_DIR, 'backup')
    zip_path = os.path.join(backup_folder, zip_name)
    db_file = os.path.join(backup_folder, files[0])
    media_file = os.path.join(backup_folder, files[1])

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(db_file, os.path.basename(files[0]))
        zipf.write(media_file, os.path.basename(files[1]))

    os.remove(db_file)
    os.remove(media_file)

def get_last_backup():
    backup_folder = os.path.join(settings.BASE_DIR, 'backup')
    backups = os.listdir(backup_folder)
    formato = "Backup_%Y-%m-%d_%H-%M-%S.zip"
    backups_dt = [datetime.strptime(backup, formato) for backup in backups]
    index = max(enumerate(backups_dt), key=lambda x: x[1])[0]
    return backup_folder + "\\" + backups[index], backups[index]