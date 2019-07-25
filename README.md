![logo](https://i.imgur.com/keDuc38.png)

>A python script that provides a Discord Rich Presence description for TF2 servers. All vanilla maps are supported with images, and plenty of competitive ones are too! 

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) ![license](https://img.shields.io/github/license/cyclowns/tf2-rich-presence.svg?style=for-the-badge)

![presencetest](https://i.imgur.com/29WQ1UM.png)

### Usage / How To Run

TF2 Rich Presence, by default, will start itself on startup on whatever system you're running, unless you disable this.
If it's not currently running, go to your installation directory (either `C:\Program Files (x86)\tf2-rich-presence` or `/usr/share/tf2-rich-presence`)
and run either `open_tf2_rich_presence.bat` or `open_tf2_rich_presence.sh`, if you're running Windows or Linux respectively. This will run TF2 Rich Presence
in the background

# **Installation**

First, *MAKE SURE* you have `python3` (3.7 preferred) and `pip` installed and in your system PATH. Visit the python website if you don't
already have them installed and do it there.

Next, and **very importantly**, go into your TF2 Launch Options by right-clicking on Team Fortress 2 in Steam, going to Properties, and clicking Set Launch Options.
Then, add the launch option `-condebug`. This is integral to the program working, which is explained in `'Hows it Work?'` below.

Now, download this repository. You can do this by clicking "Clone or download" at the top. Save it anywhere, and unzip it.

Next, depending on whether you're running Windows or Linux, run `install_windows.bat` (*AS ADMIN*) or `./install_linux.sh`. The installer will
guide you through the process of installing TF2 Rich Presence.

## **Uninstallation**

No hard feelings.

To uninstall on windows:

- Delete `C:\Program Files (x86)\tf2-rich-presence`
- Remove `open_tf2_rich_presence.bat` from your startup folder at `%appdata%\Microsoft\Windows\Start Menu\Programs\Startup` on modern Windows.

To uninstall on linux:

- Run `systemctl --user stop tf2-rich-presence && systemctl --user disable tf2-rich-presence && rm /usr/lib/systemd/user/tf2-rich-presence.service` (be careful with those `rm`s!)
- Delete `/usr/share/tf2-rich-presence`.

## Hows it Work?

Basically, I found out about a nifty little debugging launch option called `-condebug`. This prints out the contents of your console to a file
called console.log, in your `/tf` directory. More importantly, all the servers you connect to and their IPs are listed in this console.log. Essentially,
my program parses the console.log for the IP and port of the server, asks the server you connected to its game data using [python-valve](https://github.com/serverstf/python-valve), and then displays the game data through [pypresence](https://github.com/qwertyquerty/pypresence), a wrapper around Discord Rich Presence.

## Future Updates

I'm planning on adding every map RGL is using for 6s/7s/HL to the image list, but certain ones like product, warmfrost, mge maps, ramjam, and vigil are supported
already.

For the actual code side of things, I'll probably refactor and document the code a little bit over time, and improve the CI/CD. I created this entire project in the span of like, 8 hours, so its not amazing.
