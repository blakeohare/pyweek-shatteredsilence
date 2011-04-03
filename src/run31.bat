@echo OFF
del /s *.pyc
IF "%py31%" == "" SET py31="C:\Python31"
"%py31%\python.exe" run.py
