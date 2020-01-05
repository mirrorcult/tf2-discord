if exist %~dp0windows del %~dp0windows
mkdir %~dp0windows
xcopy "%~dp0..\build_files\windows\*" "windows" /i
xcopy "%~dp0..\LICENSE" "windows" /i
xcopy "%~dp0..\README.md" "windows" /i

pip install -r "%~dp0..\requirements.txt"

pyinstaller %~dp0..\src\main.py --clean --noconsole --distpath windows
ren "%~dp0windows\main\" "tf2-discord"

del main.spec