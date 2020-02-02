#!/bin/bash

echo "-------------------"
echo "- Linux Installer -"
echo "-------------------"
echo ""

# Steps:
# 1. Make sure user is running -condebug
# 2. Get user's TF2 directory
# 3. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
# 4. Copy steamdir into path.dat 
# 5. Ensure that the program runs in background and runs on startup 

# Step 1:

echo "**IMPORTANT**"
echo "Before you go any further, go into your TF2 launch options by right clicking on TF2 in steam,"
echo "going to Properties, and selecting Launch Options. From there, add the launch option '-condebug'"
echo "This allows tf2-discord to snoop your console output to tell when you've connected to a server"
echo "If you're concerned about this program looking at your console.log, remember that everything is open source"
echo "and really all the program looks for is the server's IP that you're connecting to."
echo ""

# Step 2:

could_find=0
steamdir=""
steamdir_prompt="n"

if [ -d ~/.steam/steam/steamapps/common/Team\ Fortress\ 2/ ]; then
    echo "Your TF2 directory is assumed to be at ~/.steam/steam/steamapps/common/Team Fortress 2. Is this correct? [y/n] "
    read steamdir_prompt
    if [ $steamdir_prompt == "y" ]; then
    	steamdir="$HOME/.steam/steam"
    fi
else
    if [ -d ~/.local/share/Steam/steamapps/common/Team\ Fortress\ 2/ ]; then
        echo "Your steam games directory is assumed to be at ~/.local/share/steam. Is this correct? [y/n] "
        read steamdir_prompt
        if [ $steamdir_prompt == "y" ]; then
            steamdir="$HOME/.local/share/steam"
        fi
    fi
fi

if [ ! $steamdir_prompt == "y" ]; then
    echo "Could not find steam directory. Enter location of steam directory: "
    read steamdir
    if [ ! -d $steamdir/steamapps/common/Team\ Fortress\ 2/ ]; then
        echo "Not a valid steam installation containing TF2."
        exit
    fi
fi

# Step 3:
echo "Copying files to correct dir.. "
if [ -d "/usr/share/tf2-rich-presence" ]; then rm -rf /usr/share/tf2-rich-presence; fi
sudo mkdir /usr/share/tf2-rich-presence/
sudo cp -r ./* /usr/share/tf2-rich-presence/
sudo rm /usr/share/tf2-rich-presence/tf2richpresence.service # extra file and im lazy

# Step 4:
echo "Adding steam directory to path.dat..."
sudo touch /usr/share/tf2-rich-presence/path.dat
sudo chmod a+w /usr/share/tf2-rich-presence/path.dat # since sudo echo doesnt work for some reason
echo $steamdir > /usr/share/tf2-rich-presence/path.dat

# Step 5:
echo "Adding service to systemd.."
sudo cp tf2richpresence.service /usr/lib/systemd/user
systemctl --user enable tf2richpresence

echo -e "\nStarting tf2-discord..."
systemctl --user start tf2richpresence
