#!/usr/bin/env python3

# TODO: change to python log files
# TODO: add error handling instead of just f uckin prints
# TODO: refactor to be async (do this later i dont wanna do it now)

from config import CLIENT_ID, MAPS
from pypresence import Presence
from valve.source.a2s import ServerQuerier
import os.path
import psutil
import time
import sys
import re


def tf2_running():
    """Returns true if TF2 is currently running."""
    for proc in psutil.process_iter():
        try:
            # checking exe name just in case its like, actually HL2
            if "hl2" in proc.name().lower() and "Team Fortress" in proc.exe():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def discord_running():
    """Returns True if Discord is currently running."""
    for proc in psutil.process_iter():
        try:
            if "discord" in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def map_name_to_map_image(name):
    """Converts a name of a map (i.e. koth_viaduct) to its image value
    in the Rich Presence app (i.e viaduct)"""
    for map_name, image in MAPS.items():
        if map_name in name:
            return image
    return "unknown"


def query_server(ip, port):
    """Queries a server with the given IP and port"""
    with ServerQuerier((ip, int(port)), timeout=60) as server:
        print(f'Querying server {ip}:{port}')
        return server.info()


class PresenceHandler:
    def __init__(self):
        self.RPC = Presence(CLIENT_ID)
        self.RPC.connect()
        self.cleared_presence = False
        self.presence_loaded = False
        self.timestamp = int(time.time())
        self.on_main_menu = False

    def server_presence(self, info):
        details = info["server_name"]
        if details[0] == chr(1):
            # sometimes server names will have a bunch of
            # chars with code 1 at the beginning, so we remove them
            details = details.replace(chr(1), '')
        large_text = info["map"]
        large_image = map_name_to_map_image(info["map"])

        # player_count can be off slightly, which messes with everything
        if info["player_count"] == 0:
            party_size = (info["player_count"] + 1, info["max_players"])
        else:
            party_size = (info["player_count"], info["max_players"])

        self.RPC.update(
            small_image="tf2button",
            small_text="TF2 Rich Presence by cyclowns#1440",
            large_image=large_image,
            large_text=large_text,
            details=details,
            state="Playing",
            party_size=party_size,
            start=self.timestamp
        )
        print(f'Updated presence for server {info["server_name"]}!')

    def main_menu_presence(self):
        self.on_main_menu = True
        self.RPC.update(
            small_image="tf2button",
            small_text="TF2 Rich Presence by cyclowns#1440",
            large_image="mainmenu",
            large_text="Main Menu",
            details="Main Menu",
            start=self.timestamp
        )


class ParserHandler:
    def __init__(self):
        self.ip_regex = r".+?(?=:)"
        self.port_regex = r":[0-9]+"
        self.whitelist_regex = r"[^0-9:.]+"
        self.current_cache = ""
        self.cache_fails = 0
        self.console_log_path = self.get_console_log_path()

    def get_console_log_path(self):
        """Returns the path of the console.log file.
        Errors if path.dat is not configured properly,
        or console.log doesn't exist."""

        if os.path.isfile("/usr/share/tf2-rich-presence/path.dat"):
            with open("/usr/share/tf2-rich-presence/path.dat", "r") as file:
                steampath = file.read().rstrip()
                if os.path.isfile(steampath + "/steamapps/common/Team Fortress 2/tf/console.log"):
                    return steampath + "/steamapps/common/Team Fortress 2/tf/console.log"
                    # print("Running Linux! Found console_log_path at " + console_log_path)
                else:
                    # print(f"That path ( {steampath} ) is not a valid path to a Steam installation with TF2 in it, or you haven't added -condebug to your launch options.")
                    sys.exit()
        elif os.path.isfile("C:\\Program Files (x86)\\tf2-rich-presence\\path.dat"):
            with open("C:\\Program Files (x86)\\tf2-rich-presence\\path.dat", "r") as file:
                steampath = file.read().rstrip()
                if os.path.isfile(steampath + "\\steamapps\\common\\Team Fortress 2\\tf\\console.log"):
                    return steampath + "\\steamapps\\common\\Team Fortress 2\\tf\\console.log"
                else:
                    # print(f"That path ( {steampath} ) is not a valid path to a Steam installation with TF2 in it, or you haven't added -condebug to your launch options.")
                    sys.exit()  # TODO THROW ERRORS
        else:
            # print("No path.dat file found!")
            sys.exit()  # TODO THROW ERRORS

    def parse_console_log(self):
        """Parses the console.log file and returns the IP and port
        of the connected server, if found."""

        print("Parsing console.log..")
        with open(self.console_log_path, 'r', encoding='utf-8') as log:
            lines = log.readlines()
            data = []
            for line in lines:
                if line.startswith("Connecting to"):
                    line_stripped = re.sub(self.whitelist_regex, '', line)
                    ip = re.search(self.ip_regex, line_stripped).group(0)
                    port_unstripped = re.search(self.port_regex, line_stripped).group(0)
                    # first char is a : which we need to get rid of
                    port = port_unstripped[1:]
                    data.append("server")
                    data.append((ip, port))
                    print(f'Found server {ip}:{port}!')
                    break
            return data

    def clear_console_log(self):
        """Clears the content of the console.log file."""

        print("Cleared console.log!")
        open(self.console_log_path, 'w').close()

    def cache_console_log(self):
        """Caches the console.log file, and checks if the cache has
        changed at all. If it hasn't, it ups a counter (cache_fails).
        If this counter reaches 5, the program assumes you're on
        the main menu."""

        f = open(self.console_log_path, 'r', encoding='utf-8')
        to_cache = f.read()
        if to_cache == self.current_cache:
            self.cache_fails += 1
        else:
            self.cache_fails = 0
        self.current_cache = to_cache
        f.close()


class TF2Discord:
    def __init__(self):
        # set in run()
        self.setup_rpc()
        self.parser = ParserHandler()  # TODO check for exceptions here
        self.parser.clear_console_log()

        self.current_ip = ""
        self.current_port = ""

    def setup_rpc(self):
        """Returns a valid PresenceHandler, after checking
        if it can create one."""

        if discord_running():
            # rpc might not be running immediately
            # so lets just wait 10 seconds to be sure
            time.sleep(10)
            print("Discord is up! Connecting to RPC..")
            self.discord = PresenceHandler()  # TODO check for exceptions here
            return
        print("Couldn't connect to RPC initially! Trying again in 30 seconds.")
        time.sleep(30)
        self.setup_rpc()

    def check_running(self):
        """Checks if TF2 and Discord are running.
        If either isn't, then sleep and check later.
        If it's running now, then return control flow to run()."""

        if not tf2_running():
            if not self.discord.cleared_presence:
                print("TF2 isn't running! Clearing RPC and console.log..")
                self.parser.clear_console_log()
                if discord_running():
                    # Discord up, TF2 not running
                    self.discord.RPC.clear()
                    self.discord.cleared_presence = True
                    self.discord.timestamp = int(time.time())
                else:
                    print("Couldn't clear RPC, discord not running!")
        else:
            if not discord_running():
                print("Discord isn't running!")  # TODO log.debug
            else:
                print("Discord and TF2 are running!")  # TODO log.debug
                return

        time.sleep(30)
        self.check_running()

    def run(self):
        """Main program entry point."""
        self.check_running()

        try:  # TODO what the fuck change this dude whats wrong with you
            self.discord.cleared_presence = False
            data = self.parser.parse_console_log()
            if data:  # data[0] = type of data
                if data[0] == "server":
                    self.discord.on_main_menu = False
                    # new server!
                    (ip, port) = data[1]
                    self.current_ip = ip
                    self.current_port = int(port)
                    self.discord.timestamp = int(time.time())
                    server_info = query_server(ip, int(port))
                    self.discord.server_presence(server_info)
            else:
                # if we have a current ip, then who cares, lets keep querying
                if self.current_ip != "" and self.current_port != "":
                    server_info = query_server(self.current_ip, self.current_port)
                    self.discord.server_presence(server_info)
                else:
                    print("On main menu!")
                    if not self.discord.on_main_menu:
                        self.discord.timestamp = int(time.time())
                    self.discord.main_menu_presence()
        except:
            print(f'Something messed up querying the server or updating RPC! Error: {sys.exc_info()[0]}')

        self.parser.cache_console_log()
        if self.parser.cache_fails >= 5 and self.current_ip != "":
            print("console.log hasn't changed in 5 cycles, resetting IP...")
            self.current_ip = ""
            self.current_port = ""
            self.discord.timestamp = int(time.time())
            self.parser.cache_fails = 0
        self.parser.clear_console_log()

        time.sleep(30)
        self.run()


def tf2_discord():
    """pynsist entry point."""
    tf2d = TF2Discord()
    tf2d.run()


if __name__ == "__main__":
    """pyinstaller ELF executable entry point."""
    tf2_discord()
