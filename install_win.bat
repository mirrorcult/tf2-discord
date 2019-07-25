@echo off

rem Windows Installer

echo "--------------------------------------------"
echo "Windows Installer for tf2-rich-presence"
echo "--------------------------------------------"
echo ""

rem Steps:
rem 1. Make sure user is using condebug
rem 2. Get user's TF2 directory
rem 3. Run 'pip install -r requirements.txt' 
rem 4. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
rem 4.5 Copy steamdir into config.py
rem 5. Ensure that the program runs in background and runs on startup (pythonw for windows, nohup python & for linux)

rem Step 1

echo **IMPORTANT**
echo Before you go any further, go into your TF2 launch options by right clicking on TF2 in steam,
echo going to Properties, and selecting Launch Options. From there, add the launch option '-condebug'
echo This allows tf2-rich-presence to snoop your console output to tell when you've connected to a server
echo If you're concerned about this program looking at your console.log, remember that everything is open source
echo and really all the program looks for is the server's IP that you're connecting to.
echo.

rem Step 2

echo Your Steam directory is assumed to be at 'C:\Program Files (x86)\Steam.
:steamdir_prompt
set /P "promptcorrect=Is this correct (y/n)? "
if /I "%promptcorrect%" equ "n" goto steamdir_no
if /I "%promptcorrect%" equ "y" goto steamdir_yes
goto steamdir_prompt

:steamdir_no
set /P "steamdir=What is your steam directory? "
goto continue_steamdir

:steamdir_yes
set steamdir="C:\Program Files (x86)\Steam"
goto continue_steamdir

rem Step 3

:continue_steamdir

echo If you need to change your steam directory, change console_log_directory in C:\Program Files(x86)\tf2-rich-presence\config.py.
echo.

rem Step 4

echo Make sure you have pip and python installed, by the way. Just saying that in case this errors so you know what the problem is.
pip install -r requirements.txt
echo. 

rem Step 5

echo Creating new directory at C:\Program Files(x86)\tf2-rich-presence...
mkdir "Z:\Program Files (x86)\tf2-rich-presence"
mkdir "Z:\Program Files (x86)\tf2-rich-presence\src"

echo Copying files over..
xcopy "src\main.py" "Z:\Program Files (x86)\tf2-rich-presence\src"
xcopy "src\config.py" "Z:\Program Files (x86)\tf2-rich-presence\src"
xcopy "dist\windows\open_tf2_rich_presence.bat" "Z:\Program Files (x86)\tf2-rich-presence\"
xcopy "dist\windows\open_tf2_rich_presence.bat" "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup" 
xcopy "README.md" "Z:\Program Files (x86)\tf2-rich-presence\"
xcopy "LICENSE" "Z:\Program Files (x86)\tf2-rich-presence\"
ren "Z:\Program Files (x86)\tf2-rich-presence\src\main.py" "main.pyw"

echo. >> "Z:\Program Files (x86)\tf2-rich-presence\config.py"
echo console_log_directory = "%steamdir%\steamapps\common\Team Fortress 2\tf\console.log" >> "Z:\Program Files (x86)\tf2-rich-presence\config.py"
echo.