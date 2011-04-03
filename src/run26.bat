@echo OFF
del /q /s *.pyc
IF "%py26%" == "" SET py26="C:\Python26"
"%py26%\python.exe" run.py
