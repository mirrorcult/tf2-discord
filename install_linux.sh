#!/bin/bash

###################
# Linux Installer #
###################

# Steps:
# 1. Make sure user is running -condebug
# 2. Get user's TF2 directory
# 3. Run 'pip install -r requirements.txt' 
# 4. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
# 4.5: Copy steamdir into config.py
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
steamdir_prompt="n"

if [ -d ~/.steam/steam ]; then
    echo "Your steam games directory is assumed to be at ~/.steam/steam. Is this correct? [y/n] "
    read steamdir_prompt
    if [ $steamdir_prompt == "y" ]; then
        let steamdir="~/.steam/steam"
    fi
else
    if [ -d ~/.local/share/Steam ]; then
        echo "Your steam games directory is assumed to be at ~/.local/share/steam. Is this correct? [y/n] "
        read steamdir_prompt
        if [ $steamdir_prompt == "y" ]; then
            let steamdir="~/.local/share/steam"
        fi
    fi
fi

if [ ! steamdir_prompt == "y" ]; then
    echo "Could not find steam directory. Enter location of steam directory: "
    read steamdir
    if [ ! -d $steamdir ]; then
        echo "Not a valid directory."
        exit
    fi
fi

# Step 3:
echo "Make sure you have python3 and pip installed, if you didn't listen earlier!"
pip install -r requirements.txt

# Step 4:
echo "Copying files to correct dir.. Make sure you ran this as root!"

mkdir /usr/share/tf2-rich-presence
mkdir /usr/share/tf2-rich-presence/src
cp src/* /usr/share/tf2-rich-presence/src
cp dist/linux/open_tf2_rich_presence.sh /usr/share/tf2-rich-presence
cp README.md /usr/share/tf2-rich-presence/
cp LICENSE /usr/share/tf2-rich-presence/

chmod +x /usr/share/tf2-rich-presence/open_tf2_rich_presence.sh

# Step 4.5:
echo "Adding steamdir to config.py..."
echo -e "\nconsole_log_directory = \"$steamdir/steamapps/common/Team Fortress 2/tf/console.log\"" >> /usr/share/tf2-rich-presence/config.py

# Step 5:
# echo "Adding service to systemd.."
# cp dist/linux/tf2richpresence.service /etc/systemd/system/
# systemctl start tf2richpresence
# systemctl enable tf2richpresence