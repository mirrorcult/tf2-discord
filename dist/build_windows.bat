@echo off

if exist tf2disc-windows ( del /f /q /s tf2disc-windows\*.* > NUL && rmdir /q /s tf2disc-windows )

pip install -r requirements.txt

xcopy "%~dp0..\src\*.py" .
xcopy "%~dp0..\assets\tf2discord.ico" .
python setup.pyw build
del *.py

mkdir tf2disc-windows

xcopy /E "%~dp0build\exe.win32-3.6" tf2disc-windows
xcopy /E "%~dp0..\build_files\windows\*" tf2disc-windows
xcopy "%~dp0..\LICENSE" tf2disc-windows
xcopy "%~dp0..\README.md" tf2disc-windows

del /f /q /s "%~dp0build\*.*" > NUL
rmdir /q /s build
del tf2discord.ico