import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None

setup(  name = "tf2-discord",
        version = "3.1.1",
        description = "Rich Presence for TF2",
        options = {"build_exe": build_exe_options},
        executables = [Executable("src/main.py", base=base)]
)