# tf2-rich-presence

A python script that provides a discord rich presence description for TF2 servers.

## Usage / How To Run

TF2 Rich Presence, by default, will start itself on startup on whatever system you're running, unless you disable this.
If it's not currently running, go to your installation directory (either `C:\Program Files (x86)\tf2-rich-presence` or `/usr/share/tf2-rich-presence`)
and run either `open_tf2_rich_presence.bat` or `open_tf2_rich_presence.sh`, if you're running Windows or Linux respectively. This will run TF2 Rich Presence
in the background.

## Installation

First, *MAKE SURE* you have `python3` (3.7 preferred) and `pip` installed and in your system PATH. Visit the python website if you don't
already have them installed and do it there.

Next, depending on whether you're running Windows or Linux, run `install_windows.bat` (*AS ADMIN*) or `sudo ./install_linux.sh`. The installer will
guide you through the process of installing TF2 Rich Presence.

## Uninstallation

No hard feelings.

To uninstall on windows:

- Delete `C:\Program Files (x86)\tf2-rich-presence`
- Remove `open_tf2_rich_presence.bat` from your startup folder at `%appdata%\Microsoft\Windows\Start Menu\Programs\Startup` on modern Windows.

To uninstall on linux:

- Run `systemctl stop tf2-rich-presence && systemctl disable tf2-rich-presence && rm /etc/systemd/system/tf2-rich-presence.service` (be careful with those `rm`s!)
- Delete `/usr/share/tf2-rich-presence`.
