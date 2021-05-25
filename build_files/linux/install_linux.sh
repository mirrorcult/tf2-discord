#!/bin/sh

echo -e "-------------------"
echo -e "- Linux Installer -"
echo -e "-------------------"
echo -e ""

# Steps:
# 1. Make sure user is running -condebug
# 2. Get user's TF2 directory
# 3. Copy all necessary files to installation directory, based on OS (C:\Program Files (x86)\ or /usr/share)
# 4. Copy steamdir into path.dat 
# 5. Ensure that the program runs in background and runs on startup 

# Step 1:

echo -e "**IMPORTANT**"
echo -e "Before you go any further, go into your TF2 launch options by right clicking on TF2 in steam,"
echo -e "going to Properties, and selecting Launch Options. From there, add the launch option '-condebug'"
echo -e "This allows tf2-discord to snoop your console output to tell when you've connected to a server"
echo -e "If you're concerned about this program looking at your console.log, remember that everything is open source"
echo -e "and really all the program looks for is the server's IP that you're connecting to."
echo -e "\nEnter any key to confirm that you have read the text above."
read -rsn1 -p ""

# Step 2:

steamdir=""
steamdir_prompt="n"

if [ -d ~/.steam/steam/steamapps/common/Team\ Fortress\ 2/ ]; then
    echo -e "\nYour steam directory is assumed to be at ~/.steam/steam. Is this correct? [y/n] "
    read steamdir_prompt
    if [ $steamdir_prompt == "y" ]; then
    	steamdir="$HOME/.steam/steam"
    fi
else
    if [ -d ~/.local/share/Steam/steamapps/common/Team\ Fortress\ 2/ ]; then
        echo -e "\nYour steam directory is assumed to be at ~/.local/share/Steam. Is this correct? [y/n] "
        read steamdir_prompt
        if [ $steamdir_prompt == "y" ]; then
            steamdir="$HOME/.local/share/Steam"
        fi
    fi
fi

if [ ! $steamdir_prompt == "y" ]; then
    echo -e "\nCould not find steam directory. Enter location of steam directory: "
    read steamdir
    if [ ! -d $steamdir/steamapps/common/Team\ Fortress\ 2/ ]; then
        echo -e "Not a valid steam installation containing TF2. Make sure you give the path to 'Steam', not 'steamapps' or 'common'"
        exit
    fi
fi

# Step 3:
echo -e "\nCopying files to correct dir.. "
if [ -d "/usr/share/tf2-rich-presence" ]; then rm -rf /usr/share/tf2-rich-presence; fi
sudo mkdir /usr/share/tf2-rich-presence/
sudo cp -r ./* /usr/share/tf2-rich-presence/
sudo rm /usr/share/tf2-rich-presence/tf2richpresence.service # extra file and im lazy

# Step 4:
echo -e "Adding steam directory to path.dat..."
sudo touch /usr/share/tf2-rich-presence/path.dat
sudo chmod a+w /usr/share/tf2-rich-presence/path.dat # since sudo echo -e doesnt work for some reason
echo -e $steamdir > /usr/share/tf2-rich-presence/path.dat

# Step 4.5:
echo -e Creating log directory..
sudo mkdir /var/log/tf2discord
sudo chmod a+w /var/log/tf2discord

# Step 5:
echo -e "Adding service to systemd.."
sudo cp tf2richpresence.service /usr/lib/systemd/user
systemctl --user enable tf2richpresence

echo -e "\ntf2-discord installed successfully!"
echo -e "Starting tf2-discord..."
systemctl --user start tf2richpresence
