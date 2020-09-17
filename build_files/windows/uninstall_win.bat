@echo off

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Current permissions inadequate. Please run this program as administrator.
    timeout /t 5
    exit /B
)

rd /s /q "C:\Program Files (x86)\tf2-rich-presence"
echo Uninstalled TF2 Discord.
schtasks /delete /tn "TF2Discord"

echo Done!
pause
