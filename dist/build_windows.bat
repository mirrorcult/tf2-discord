@echo off

if exist %~dp0windows rmdir %~dp0windows
mkdir %~dp0windows
xcopy "%~dp0..\build_files\windows\*" "%~dp0windows" /i
xcopy "%~dp0..\LICENSE" "%~dp0windows" /i
xcopy "%~dp0..\README.md" "%~dp0windows" /i

pip install -r "%~dp0..\requirements.txt"

python -m pynsist %~dp0..\src\main.py --clean --noconsole --onefile --distpath %~dp0windows
ren "%~dp0windows\main\" "tf2-discord"

del %~dp0main.spec
