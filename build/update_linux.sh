#!/bin/bash

echo "-----------------"
echo "- Linux Updater -"
echo "-----------------"
echo ""

steamdir=""

echo "Updating main script..."
sudo cp -n src/main.py /usr/share/tf2-rich-presence/src/main.py

echo "Enter steam directory: (up to steam folder; i.e. ~/.local/share/steam or ~/.steam/steam)"
read steamdir

if [ -d $steamdir ]; then
    sudo cp -n src/config.py /usr/share/tf2-rich-presence/src/config.py
    echo "Updating config script..."
    sudo chmod a+w /usr/share/tf2-rich-presence/src/config.py # since sudo echo doesnt work for some reason
    echo -e "\nconsole_log_path = \"$steamdir/steamapps/common/Team Fortress 2/tf/console.log\"" >> /usr/share/tf2-rich-presence/src/config.py
else
    echo "Not a valid directory!"
    exit
fi

echo "Updating autostart..."
systemctl --user stop tf2richpresence && systemctl --user disable tf2richpresence
sudo cp dist/linux/tf2richpresence.service ~/.config/systemd/user/tf2richpresence.service
systemctl --user daemon-reload
systemctl --user start tf2richpresence && systemctl --user enable tf2richpresence
echo "Done!"
