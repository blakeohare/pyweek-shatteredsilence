IF "%py25%" == "" SET py25="C:\Python25"
"%py25%\python.exe" ..\py2exe\setup.py

xcopy Images dist\Images /S
xcopy Levels dist\Levels /S
xcopy GrayImages dist\GrayImages /S
xcopy Media dist\Media /S

rmdir ..\exe /s /q
rename dist exe
move exe ..\
rmdir build /s /q