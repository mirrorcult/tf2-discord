![logo](https://i.imgur.com/keDuc38.png)

>A python script that provides a Discord Rich Presence description for TF2 servers. All vanilla maps are supported with images, and plenty of competitive ones are too! 

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) ![license](https://img.shields.io/github/license/cyclowns/tf2-discord.svg?style=for-the-badge)

![presencetest](https://i.imgur.com/oTfCn9n.png)

# **What makes tf2-discord good / different from other TF2 Rich Presence clients?**

Well, I'm glad you asked!

- It has **cross-platform support** for Windows and Linux, with Mac planned soon!
- It runs in the background, and is extremely **lightweight and unintrusive**.
- It's **easy to setup** and has a detailed installation guide.
- It has an **active developer**, fixing things and adding new features all the time.
- It has image support for **every vanilla map in the game**, and plenty of mainstream competitive ones. It even has custom images for surf maps, jump maps, and MGE maps!
- **It's pretty smart**, and can figure out whether you're in a party queue, a server, or on the main menu 99% of the time (there are some restrictions due to how this information is gathered, unfortunately)
- It shows **lots of information**--including a map image, map name, server name, number of players and maximum players, a timestamp...

# **Installation**

This installation assumes you have working internet and a brain.

- First, *MAKE SURE* you have `python3` (3.7 preferred) and `pip` installed and in your system PATH. Visit the python website if you don't already have them installed at [python.org](https://python.org/downloads/). **Make sure you specifically download `pip` with it and add both to your PATH**!!! Python is pretty great, and you should have it installed regardless. Most linux distros have python3 and pip preinstalled--and, honestly, if you're running Linux you probably know how to install
Python.
- Next, and **very importantly**, go into your TF2 Launch Options by right-clicking on Team Fortress 2 in Steam, going to Properties, and clicking Set Launch Options.
- Then, add the launch option `-condebug`. This is integral to the program working, which is explained in `'Hows it Work?'` below.
- Now, download this repository. You can do this by clicking "Clone or download" at the top. Save it anywhere, and unzip it. If you have `git` installed, you can just do `git clone https://github.com/cyclowns/tf2-discord` and unzip that.

Now, follow the guide for your OS:

`Windows:`

- Note: `tf2-discord` is confirmed to work on Windows 8, 8.1, and 10. Anything lower is unconfirmed, but let me know if it works.
- With the folder unzipped anywhere, right click on `install_windows.bat` and click `'Run as Administrator'`. It is very important that you run as admin, or copying files won't work.
- The program will prompt you for your Steam installation. 99% of the time its at `C:\Program Files (x86)\Steam`, but if it isn't just make sure you give it a valid path to your `Steam` directory specifically. Note: If you have multiple steam installs, **use the one with TF2 actually in it!!**
- From here on out, `tf2-discord` will install itself, make itself run on startup, and then run itself! If you get any errors with `pip install`, it's because its not in your PATH or you never installed it.
- You're free to delete the folder you downloaded earlier worry-free--all of the files `tf2-discord` needs are in `C:\Program Files (x86)\tf2-rich-presence`.
- If you have questions or need help getting the program to run, feel free to contact me at `cyclowns#1440` on Discord. If you find any bugs or unexpected behavior, PLEASE post an issue report here on GitHub. I'll really appreciate it.

`Linux:`

- Note: `tf2-discord` is confirmed to work on Manjaro and Arch Linux. I'm 95% sure it'll work on Ubuntu, Debian, and Fedora too, so let me know if it does so I can add it here!
- From here on out, I'm assuming you're in your terminal. If you're in a graphical file manager, the steps shouldn't be that hard to follow anyway.
- With your folder unzipped, `cd` into it and run `./install_linux.sh` (not as super user!!!). If it doesn't run, you might need to do `chmod u+x install_linux.sh` first.
- Now, the program will ask you for your Steam installation. Most of the time its either at `~/.steam/steam` or `~/.local/share/steam`, but if it isn't you can enter it here. Note: If you have multiple steam installs, **use the one with TF2 actually in it!!**
- `tf2-discord` will now install itself to `/usr/share/tf2-rich-presence`, and add a `systemd` service called `tf2richpresence.service` that autostarts `tf2-discord` whenever you boot up.
- You're free to delete the temporary folder you downloaded earlier worry-free. If you have questions or need help getting the program to run, feel free to contact me at `cyclowns#1440` on Discord. If you find any bugs or unexpected behavior, PLEASE post an issue report here on GitHub. I'll really appreciate it.

## **Updating**

Updating `tf2-discord` is fairly simple.

`Windows:`

- Redownload the newest version of `tf2-discord` using the same method you did installing it, and unzip it.
- Run update_win.bat as administrator. !!(NOT CURRENTLY IMPLEMENTED)!!
- Reenter your steam directory when prompted. If you don't know it, it's probably `C:\Program Files (x86)\Steam`--wherever TF2 is installed.
- Your `tf2-discord` is now fully updated!

`Linux:`

- Redownload the newest version of `tf2-discord` using the same method you did installing it, unzip it, and `cd` in.
- Run `chmod +x ./update_linux.sh` and then `./install_linux.sh`.
- Reenter your steam directory when prompted. If you don't know it, it's probably `~/.local/share/Steam` or `~/.steam/steam`--wherever TF2 is installed.
- Your `tf2-discord` is now fully updated!

## **Uninstallation**

No hard feelings.

`Windows:`

- Delete `C:\Program Files (x86)\tf2-rich-presence`
- Remove `open_tf2_rich_presence.bat` from your startup folder at `%appdata%\Microsoft\Windows\Start Menu\Programs\Startup` on modern Windows.

`Linux:`

- Run `systemctl --user stop tf2richpresence && systemctl --user disable tf2richpresence && rm ~/.config/systemd/user/tf2richpresence.service` (be careful with those `rm`s!)
- Delete `/usr/share/tf2-rich-presence`.

## Hows it Work?

Basically, I found out about a nifty little debugging launch option called `-condebug`. This prints out the contents of your console to a file called console.log, in your `/tf` directory. More importantly, all the servers you connect to and their IPs are listed in this console.log. Essentially, my program parses the console.log for the IP and port of the server, asks the server you connected to for its game data using [python-valve](https://github.com/serverstf/python-valve), and then displays the game data through [pypresence](https://github.com/qwertyquerty/pypresence).

## Future Updates

- Better installation (preferably not requiring Python to be installed at all) coming soon.
- Mac support will be added soon! All I really need is a Mac machine to test it on, or someone with one. If you're interested in helping me out with that, hit me up at `cyclowns#1440` on Discord.
- Timestamps are coming very soon!
- I might try and figure out a way to figure out what class you're playing, and display that as the small image rather than the TF2 logo.
- I'm planning on adding every map RGL is using for 6s/7s/HL to the image list, but certain ones like product, prolands, warmfrost, ramjam, and vigil are supported already.
- For the actual code side of things, I'll probably refactor and document the code a little bit over time, and improve the CI/CD. I created this entire project in the span of like, a day and a half, so its not amazing.

## Known Bugs

- Sometimes, even if you're on a server, `tf2-discord` will recognize that your console.log hasn't changed in a really long time and will assume incorrectly that you're probably on the main menu. This is pretty rare, but still. Not a whole lot you can do about this, except maybe.. like.. bind W or mouse1 or something to print to the console when you press it ingame?
- Rich presence updating for queueing is a little buggy.
