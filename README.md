![logo](https://i.imgur.com/keDuc38.png)

> A python script that provides a Discord Rich Presence description for Team Fortress 2. All vanilla maps are supported with images, and plenty of competitive ones are too! Not currently finished, expect bugs.

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence) ![license](https://img.shields.io/github/license/cyclowns/tf2-discord.svg?style=for-the-badge)

![presencetest](https://i.imgur.com/oTfCn9n.png)

# **What makes tf2-discord good / different from other TF2 Rich Presence clients?**

Well, I'm glad you asked!

- It has **cross-platform support** for Windows and Linux, with Mac planned soon!
- It runs in the background, and is extremely **lightweight and unintrusive**.
- It's **easy to setup** and has a detailed installation/uninstallation/updating/building guide.
- It has an **active developer**, fixing things and adding new features all the time.
- It has image support for **every vanilla map in the game**, and plenty of mainstream competitive ones as well as most Creators.tf maps. It even has custom images for surf maps, jump maps, and MGE maps!
- **It's pretty smart**, and can figure out whether you're in a server or on the main menu 90% of the time (there are some restrictions due to how this information is gathered, unfortunately)
- It shows **lots of information**--including a map image, map name, server name, number of players and maximum players, a timestamp...

## Disclaimer

A tester on windows confirmed to that, apparently, tf2-discord can register as malware with some anti-virus suites. I tried to fix this, but everything that popped up seemed to confirm that it was an issue with cxfreeze/pyinstaller that I didn't really have any way of fixing because I'm not a large corporation. If tf2-discord being detected as malware *at all* gives you some unease, I get it. On the other hand, if you've encountered this issue and know how to fix it, please tell me or submit a PR!

# **Installation**

This installation assumes you have working internet and a brain.

- First, and **very importantly**, go into your TF2 Launch Options by right-clicking on Team Fortress 2 in Steam, going to Properties, and clicking Set Launch Options.
- Then, add the launch option `-condebug`. This is integral to the program working, which is explained in `'Hows it Work?'` below.
- Now, click the button at the top of this github page that says ['releases'](https://github.com/cyclowns/tf2-discord/releases) and download the latest release for whatever operating system you're running (Mac isn't supported yet.)

Now, follow the guide for your OS:

## Windows Installation

`tf2-discord` is confirmed to work on Windows 8, 8.1, and 10. Anything lower is unconfirmed, but let me know if it works.

- With the folder you downloaded unzipped anywhere open, right click on `install_windows.bat` and click `Run as Administrator`.
- The program will prompt you for your Steam installation. 99% of the time its at `C:\Program Files (x86)\Steam`, but if it isn't just make sure you give it a valid path to your `Steam` directory specifically. Note: If you have multiple steam installs, **use the one with TF2 actually in it!!**
- From here on out, `tf2-discord` will install itself, make itself run on startup, and then run itself!
- You're free to delete the folder you downloaded earlier worry-free--all of the files `tf2-discord` needs are in `C:\Program Files (x86)\tf2-rich-presence`.
- If you have questions or need help getting the program to run, feel free to contact me at `cyclowns#1440` on Discord. If you find any bugs or unexpected behavior, PLEASE post an issue report here on GitHub. I'll really appreciate it.

## Linux Installation

`tf2-discord` is confirmed to work on Manjaro and Arch Linux. I'm 95% sure it'll work on Ubuntu, Debian, and Fedora too, so let me know if it does so I can add it here!

- From here on out, I'm assuming you're in your terminal. If you're in a graphical file manager, the fact that you are running linux means you probably know what you're doing anyway and can improvise.
- With the folder you downloaded  unzipped, `cd` into it and run `./install_linux.sh` (not as root). If it doesn't run, you might need to do `chmod u+x install_linux.sh` first.
- Now, the program will ask you for your Steam installation. Most of the time its either at `~/.steam/steam` or `~/.local/share/Steam`, but if it isn't you can enter it here. Make sure to give it a path to the directory that contains `steamapps`, not the path to your TF2 installation or the path to `steamapps`! Note: If you have multiple steam installs, **use the one with TF2 actually in it!!**
- `tf2-discord` will now install itself to `/usr/share/tf2-rich-presence`, and add a `systemd` service called `tf2richpresence.service` that autostarts `tf2-discord` whenever you boot up. If you're interested, it installs as a user service so to debug/stop/restart it you'll need to run `journalctl` or `systemctl` with `--user`.
- You're free to delete the temporary folder you downloaded earlier worry-free. If you have questions or need help getting the program to run, feel free to contact me at `cyclowns#1440` on Discord. If you find any bugs or unexpected behavior, PLEASE post an issue report here on GitHub. I'll really appreciate it.

# **Updating**

Updating `tf2-discord` is fairly simple.

## Updating on Windows

- Redownload the newest version of `tf2-discord` using the same method you did installing it, and unzip it.
- Run `update_win.bat` **as administrator**.
- Your `tf2-discord` is now fully updated!

## Updating on Linux

- Redownload the newest version of `tf2-discord` using the same method you did installing it, unzip it, and `cd` in.
- Run `update_linux.sh`.
- Your `tf2-discord` is now fully updated!

# **Uninstallation**

No hard feelings.

## Uninstallation on Windows

- Run `C:\Program Files (x86)\tf2-rich-presence\uninstall_windows.bat` **as administrator**. If you don't have this file or don't know where to find it, you can download a release at the top of the page and it will be in there.

If a bunch of errors pop up, then go into Task Manager and kill the process named 'main.exe'.

## Uninstallation on Linux

- Run `/usr/share/tf2-rich-presence/uninstall_linux.sh`. If you don't have this file or don't know where to find it, you can download a release at the top of the page and it will be in there.

# **Building from Source**

If you don't trust my pre-packaged releases (fair enough), then you can build `tf2-discord` from source fairly easily.

**Prerequisites: `python3.7` with `pip`**

If you need help installing `python` message me on Discord at `cyclowns#1440`.

## Building on Linux

- Clone/download this whole repository using `git` or the button at the top.
- `cd` into the `dist` directory, and run `./build_linux.sh`
- If your prereqs are set up correctly, after a minute or two a directory called `tf2disc-linux` should appear, containing every file you need to run `tf2-discord`.
  - One common error on Linux is with `cxfreeze`. Installing `cxfreeze` initially was hell for me, at least on Manjaro/Arch. Pro-tip if you're on either of those: just `pacman -S python-cx-freeze` and don't bother installing with `pip`.
- From here, you can install it yourself by following the installation directions above using the `tf2disc-linux` build you created.

## Building on Windows

- Clone/download this whole repository using `git` or the button at the top.
- Unzip it anywhere, and open the `dist` directory.
- Run `./build_windows.bat`.
- If your prereqs are set up correctly, after a minute or two a directory called `tf2disc-windows` should appear, containing every file you need to then install `tf2-discord`.
  - If `pip` hangs, or the script doesn't complete, try running `pip install -r requirements.txt` yourself and rerunning the script.
- From here, you can install it yourself by following the installation directions above using the `tf2disc-windows` build you created.

# How it Works

Basically, I found out about a nifty little debugging launch option called `-condebug`. This prints out the contents of your console to a file called console.log, in your `/tf` directory. More importantly, all the servers you connect to and their IPs are listed in this console.log. Essentially, my program parses the console.log for the IP and port of the server, asks the server you connected to for its game data using [python-valve](https://github.com/serverstf/python-valve), and then displays the game data through [pypresence](https://github.com/qwertyquerty/pypresence).

# Contributing

I'm happy to accept any contributions, whether its just grammar fixes in the README or actual features. If you'd like to tackle anything in the list below, go for it (but let me know first)!

- Look over my README and make sure the wording makes sense. If you were confused following any directions here, then please let me know!
- Unit testing? I doubt anyone will do this, and this program is nigh impossible to mock test input for, but go for it.
- Mac support! I don't have a Mac machine to test it on or a friend with one, so if you do then go ahead and attempt to implement support for Macs. You'll need somewhere to store the application data, somewhere to store the logs, separate install/uninstall/update scripts (Linux ones will be close with some modification), and some way to make the program start on startup. I don't know if `psutil` works for Mac, so check that out as well.
- I might try and figure out a way to figure out what class you're playing, and display that as the small image rather than the TF2 logo.
- Install directory shouldn't be fixed, but I'm too lazy to change it.
- NSIS installer package for Windows?? Somehow?? I have no idea how they work.

# Known Bugs

Please report any bugs using the `Issues` tab in this repository. Please.

- Sometimes, even if you're on a server, `tf2-discord` will recognize that your console.log hasn't changed in a really long time and will assume incorrectly that you're probably on the main menu. This is pretty rare, but still. Not a whole lot you can do about this, except maybe.. like.. bind W or mouse1 or something to print to the console when you press it ingame?
