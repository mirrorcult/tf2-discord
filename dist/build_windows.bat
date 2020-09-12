@echo off


if exist tf2disc-windows ( del /f /q /s tf2disc-windows\*.* > NUL && rmdir /q /s tf2disc-windows )

pip install -r requirements.txt

xcopy ..\src\*.py .
python setup.pyw build
del *.py

mkdir tf2disc-windows

xcopy /E "build\exe.win32-3.6" tf2disc-windows
xcopy /E "..\build_files\windows\*" tf2disc-windows
xcopy ..\LICENSE tf2disc-windows
xcopy ..\README.md tf2disc-windows

del /f /q /s build\*.* > NUL
rmdir /q /s build