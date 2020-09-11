@echo off

pip install -r "%~dp0..\build_files\windows\requirements.txt"

rem need to copy every src file over because pynsist requires module names
rem as the entrypoint, and doing that with our cur file system is dumb
rem we'll just delete them after

xcopy ..\src\*.py .

pynsist installer.cfg

del *.py