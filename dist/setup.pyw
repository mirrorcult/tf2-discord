# if you're wondering why this is a .pyw its because
# the install script copies in the source python files
# temporarily and then wildcard deletes *.py and it kept
# deleting this one and I didn't wanna hardcode it so
# whatever who cares now its a pyw

import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pypresence", "valve", "psutil", "config", "errors", "parsing", "presence"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name="tf2-discord",
        version="3.1.0",
        description="TF2 Rich Presence",
        options={"build_exe": build_exe_options},
        executables=[Executable("main.py", base=base, targetName="tf2-discord", icon="tf2discord.ico")])
