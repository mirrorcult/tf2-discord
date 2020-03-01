@echo off

rem Windows Installer

echo -------------------------------------------
echo - Windows Installer for tf2-rich-presence -
echo -------------------------------------------
echo.

rem Steps:
rem 1. Make sure user is using condebug
rem 2. Get user's TF2 directory
rem 3. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
rem 4. Copy steamdir into path.dat
rem 5. Ensure that the program runs in background and runs on startup 

rem first check for admin perms
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Current permissions inadequate. Please run this program as administrator.
	timeout /t 5
    exit /B
)

rem Step 1

echo.
echo **IMPORTANT**
echo Before you go any further, go into your TF2 launch options by right clicking on TF2 in steam,
echo going to Properties, and selecting Launch Options. From there, add the launch option '-condebug'
echo This allows tf2-rich-presence to snoop your console output to tell when you've connected to a server
echo If you're concerned about this program looking at your console.log, remember that everything is open source
echo and really all the program looks for is the server's IP that you're connecting to.
echo **IMPORTANT**
echo.

pause

rem Step 2

if exist "C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2" (
	echo Your Steam directory containing TF2 is assumed to be at 'C:\Program Files ^(x86^)\Steam.'
	:steamdir_prompt
	set /P "promptcorrect=Is this correct (y/n)? "
	if /I "%promptcorrect%" equ "n" goto steamdir_no
	if /I "%promptcorrect%" equ "y" goto steamdir_yes
	goto steamdir_prompt
)

goto steamdir_no

:steamdir_no
set /P "steamdir=What is your steam directory? "
if exist "%steamdir%\steamapps\common\Team Fortress 2" goto continue_steamdir
echo Failure: Either you put in the wrong directory (use Steam, not steamapps or common) or that steam library does not contain TF2.
goto steamdir_no

:steamdir_yes
set "steamdir=C:\Program Files (x86)\Steam"
goto continue_steamdir

:continue_steamdir

echo If you need to change your steam directory, change C:\Program Files (x86)\tf2-rich-presence\path.dat to read the correct directory.
echo.

rem Step 3

rem check for any errors first
if %errorlevel% neq 0 (
	echo Found errors! Please make sure you followed the instructions carefully and correctly.
	exit /B %errorlevel%
)

echo Creating new directory at C:\Program Files (x86)\tf2-rich-presence...
set "installpath=C:\Program Files (x86)\tf2-rich-presence"
rmdir /s /q "%installpath%"
mkdir "%installpath%"

echo Copying files over..
xcopy "%~dp0*" "%installpath%\" /i /s

rem Step 4

echo Copying steamdir into path.dat...

echo %steamdir% >> "%installpath%\path.dat"
echo.

if %errorlevel% == 0 (
	schtasks /create /tn "TF2Discord" /sc onlogon /tr "%installpath%\tf2-rich-presence\main.exe"
	echo TF2 Rich Presence is now installed and will run on startup!
	echo Running TF2 Rich Presence..
	schtasks /run /tn "TF2Discord"
) else (
	echo Found errors installing! Please try running the uninstall script and then reinstalling.
)

pause
