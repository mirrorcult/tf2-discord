@echo off

pip install -r "%~dp0..\build_files\windows\requirements.txt"

python -m pynsist win_installer.cfg
