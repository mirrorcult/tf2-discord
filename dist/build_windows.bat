mkdir windows
xcopy "%~dp0..\build_files\windows\*" "windows" /i
xcopy "%~dp0..\LICENSE" "windows" /i
xcopy "%~dp0..\README.md" "windows" /i

pip install "%~dp0..\requirements.txt"

pyinstaller ..\src\main.py --clean --noconsole -F --distpath windows
ren "%~dp0windows\main" "%~dp0windows\tf2-discord"

del build
del main.spec