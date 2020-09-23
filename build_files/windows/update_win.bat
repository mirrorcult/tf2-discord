@echo off

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Current permissions inadequate. Please run this program as administrator.
    timeout /t 5
    exit /B
)

set "installpath=C:\Program Files (x86)\tf2-rich-presence"

echo Killing process..
taskkill /F /im tf2-discord.exe

echo Copying files over..
xcopy "%~dp0*" "%installpath%\" /i /s /Y > NUL

echo Restarting process..
schtasks /delete /tn "TF2Discord"
schtasks /create /tn "TF2Discord" /sc onlogon /tr "C:\Program Files (x86)\tf2-rich-presence\tf2-discord.exe"
schtasks /run /tn "TF2Discord"

echo Complete!
pause