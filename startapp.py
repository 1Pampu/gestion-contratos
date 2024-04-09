import os
import webbrowser
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

def git_pull():
    # Actualizar el repositorio
    os.system("git pull origin main")

def run_server():
    # Actualizar pip
    os.system("pip install --upgrade pip")

    # Verificar si la base de datos existe
    newDB = False
    if not os.path.exists("db.sqlite3"):
        newDB = True

    # Ejecutar migraciones
    execute_from_command_line(["manage.py", "makemigrations"])
    execute_from_command_line(["manage.py", "makemigrations", "contratos"])
    execute_from_command_line(["manage.py", "migrate"])

    # Crear superusuario si la base de datos es nueva
    if newDB:
        execute_from_command_line(["manage.py", "createsuperuser"])

    # Abrir el navegador
    webbrowser.open("http://127.0.0.1:8000/")
    execute_from_command_line(["manage.py", "runserver", "--noreload"])

if __name__ == "__main__":
    git_pull()
    run_server()