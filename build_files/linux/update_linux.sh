systemctl --user stop tf2richpresence
echo "Copying files over.."
sudo cp -r ./* /usr/share/tf2-rich-presence/
echo "Restarting process.."
systemctl --user start tf2richpresence