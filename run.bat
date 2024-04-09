@echo off
set VIRTUAL_ENV=%CD%\.venv

%VIRTUAL_ENV%\Scripts\python.exe -m pip install -r requirements.txt
%VIRTUAL_ENV%\Scripts\python.exe startapp.py