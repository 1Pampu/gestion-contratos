import os
import webbrowser
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

def git_pull():
    # Update repository
    os.system("git pull origin main")

def run_server():
    # Install requirements
    os.system("pip install --upgrade pip")
    os.system("pip install -r requirements.txt")

    # Check if database exists in directory
    newDB = False
    if not os.path.exists("db.sqlite3"):
        newDB = True

    # Run migrations / Create database
    execute_from_command_line(["manage.py", "makemigrations"])
    execute_from_command_line(["manage.py", "migrate"])

    # Create superuser if database is new
    if newDB:
        execute_from_command_line(["manage.py", "createsuperuser"])

    # Open browser and run server
    webbrowser.open("http://127.0.0.1:8000/")
    execute_from_command_line(["manage.py", "runserver", "--noreload"])

if __name__ == "__main__":
    git_pull()
    run_server()