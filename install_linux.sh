#!/bin/bash

###################
# Linux Installer #
###################

# Steps:
# 1. Make sure user is running -condebug
# 1. Get user's TF2 directory
# 2. Copy info about TF2 dir into config.py
# 3. Run 'pip install -r requirements.txt' 
# 4. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
# 5. Ensure that the program runs in background and runs on startup (pythonw for windows, nohup python & for linux)

echo "**IMPORTANT**"
echo "Before you go any further, go into your TF2 launch options by right clicking on TF2 in steam,"
echo "going to Properties, and selecting Launch Options. From there, add the launch option '-condebug'"
echo "This allows tf2-rich-presence to snoop your console output to tell when you've connected to a server"
echo "If you're concerned about this program looking at your console.log, remember that everything is open source"
echo "and really all the program looks for is the server's IP that you're connecting to."
echo ""

# Step 2:

could_find=0
steamdir=""
steamdir_prompt="y"

if [ -d ~/.steam/steam ]; then
    let could_find=1
    echo "Your steam games directory is assumed to be at ~/.steam/steam. Is this correct? [y/n] "
    read steamdir_prompt
    if [ $steamdir_prompt == "y" ]; then
        let steamdir="~/.steam/steam"
    fi
else
    if [ -d ~/.local/share/Steam ]; then
        let could_find=1
        echo "Your steam games directory is assumed to be at ~/.local/share/steam. Is this correct? [y/n] "
        read steamdir_prompt
        if [ $steamdir_prompt == "y" ]; then
            let steamdir="~/.local/share/steam"
        fi
    else
        echo "Could not find steam directory. Enter location of steam directory: "
        read steamdir
        if [ ! -d $steamdir ]; then
            echo "Not a valid directory."
            exit
        fi
    fi
fi

if [ steamdir_prompt != "y" ]; then
    echo "Could not find steam directory. Enter location of steam directory: "
    read steamdir
    if [ ! -d $steamdir ]; then
        echo "Not a valid directory."
        exit
    fi
fi

echo -e "\nconsole_log_directory = \"$steamdir/steamapps/common/Team Fortress 2/tf/console.log\"" >> src/config.py