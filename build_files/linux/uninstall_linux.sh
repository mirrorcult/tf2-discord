echo "---------------------"
echo "- Linux Uninstaller -"
echo "---------------------"

echo "This will uninstall tf2-discord. Do you want to continue? [y/n] "
read cont

if [ $cont == "y" ]; then
    sudo rm -r /usr/share/tf2-rich-presence
    systemctl --user stop tf2richpresence && systemctl --user disable tf2richpresence
    sudo rm /usr/lib/systemd/user/tf2richpresence.service
    echo "Done!"
fi
