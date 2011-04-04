IF "%py26%" == "" SET py26="C:\Python26"
"%py26%\python.exe" ..\py2exe\setup.py

xcopy Images dist\Images /S
xcopy Media dist\Media /S

rmdir ..\exe /s /q
rename dist exe
move exe ..\
rmdir build /s /q