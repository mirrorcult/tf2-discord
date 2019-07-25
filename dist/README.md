# dist folder

The dist folder is where all files for actually installing and opening the program properly are.

Installing this program should _really_ only be done with install_YOUROSHERE.py unless you know
what you're doing enough to do it manually. If you need help installing tf2-rich-presence, contact me at
cyclowns#1440 on Discord.

## dist_linux

open_tf2_rich_presence.sh runs the program in the background using nohup.

The .service file is for systemd, so that the program runs on startup. This can be disabled
during install.

## dist_windows

open_tf2_rich_presence.bat runs the program in the background using pythonw.exe.
