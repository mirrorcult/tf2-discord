#!/usr/bin/env python3

from config import *
from pypresence import Presence
from valve.source.a2s import ServerQuerier
from valve.source import NoResponseError
import psutil
import time
import sys
import re

# check if console_log_path exists
if not ('console_log_path' in globals() or 'console_log_path' in locals()):  # should be in config.py if installed correctly
    print("Couldn't find console_log_path! Did you install correctly?")
    sys.exit()

# Does what it says on the tin.
def is_tf2_running():
    for proc in psutil.process_iter():
        try:
            if "hl2" in proc.name().lower() and "Team Fortress 2" in proc.exe(): # just in case its hl2.exe from, like, actual HL2
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Does what it says on the tin.
def is_discord_running():
    for proc in psutil.process_iter():
        try:
            if "discord" in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# Converts a name of a map (i.e. koth_viaduct) to its image value in the Rich Presence app (viaduct)
def map_name_to_map_image(name):
    for map_name, image in maps.items():
        if map_name in name: return image 
    return "unknown"

class PresenceHandler:
    def __init__(self):
        self.RPC = Presence(client_id)
        self.RPC.connect()
        self.cleared_presence = False
        self.presence_loaded = False
        self.timestamp = int(time.time())
        self.discord_running = False
        self.tf2_running = False
        self.on_main_menu = False
        self.in_queue = False

    def server_presence(self, info):
        details = info["server_name"]
        if details[0] == chr(1):
            details = details.replace(chr(1), '') # sometimes server names will have a bunch of chars with code 1 at the beginning, so we remove them
        large_text = info["map"]
        large_image = map_name_to_map_image(info["map"])
        if info["player_count"] == 0: party_size = (info["player_count"] + 1, info["max_players"]) # player_count can be off slightly, which messes with everything
        else: party_size = (info["player_count"], info["max_players"])

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

    def queue_presence(self, type):
        self.in_queue = True
        self.RPC.update(
            small_image="tf2button",
            small_text="TF2 Rich Presence by cyclowns#1440",
            large_image="competitive",
            large_text=f"Queueing for {type}",
            details=f"Queueing for {type}",
            start=self.timestamp
        )

class ParserHandler:
    def __init__(self):
        self.ip_regex = r".+?(?=:)"
        self.port_regex = r":[0-9]+"
        self.whitelist_regex = r"[^0-9:.]+"
        self.current_cache = ""
        self.cache_fails = 0
    # Parses console.log file for ip and port
    def parse_console_log(self):
        print("Parsing console.log..")
        with open(console_log_path, 'r') as log:
            lines = log.readlines()
            data = []
            for line in lines:
                if line.startswith("Connecting to"):
                    line_stripped = re.sub(self.whitelist_regex, '', line)
                    ip = re.search(self.ip_regex, line_stripped).group(0)
                    port_unstripped = re.search(self.port_regex, line_stripped).group(0) # first char is a : which we need to get rid of
                    port = port_unstripped[1:]
                    data.append("server")
                    data.append((ip, port))
                    print(f'Found server {ip}:{port}!')
                    break
                if line.startswith("[PartyClient] Entering queue for match group 12v12"):
                    data.append("casual")
                    break
                if line.startswith("[PartyClient] Entering queue for match group 6v6"):
                    data.append("competitive")
                    break
            return data
    # Clears console.log completely
    def clear_console_log(self):
        print("Cleared console.log!")
        open(console_log_path, 'w').close()

    # Caches the console.log file, and checks if the
    # cache has changed at all. If it hasn't, it ups a counter. (cache_fails)
    # If this counter reaches 5, then the game assumes you're on the main menu
    def cache_console_log(self):
        f = open(console_log_path, 'r')
        to_cache = f.read()
        if to_cache == self.current_cache: self.cache_fails += 1
        else: self.cache_fails = 0
        self.current_cache = to_cache
        f.close()

class QueryHandler:
    def __init__(self):
        self.current_ip = ""
        self.current_port = ""
    # Queries the server specified by ip and port and updates rich presence 
    def query_server(self, ip, port):
        with ServerQuerier((ip, int(port)), timeout=60) as server:
            print(f'Querying server {ip}:{port}')
            return server.info()            

# Main loop
def main_loop():
    try:
        DiscordPresence.cleared_presence = False
        data = Parser.parse_console_log()
        if data: # data[0] = type of data for RPC, essentially
            if data[0] == "server":
                DiscordPresence.on_main_menu = False
                DiscordPresence.in_queue = False
                # new server!
                (ip, port) = data[1]
                Query.current_ip = ip
                Query.current_port = int(port)
                DiscordPresence.timestamp = int(time.time())
                server_info = Query.query_server(ip, int(port))
                DiscordPresence.server_presence(server_info)
            if data[0] == "casual" or data[0] == "competitive":
                DiscordPresence.on_main_menu = False
                print(f'In {data[0]} queue!')
                if not DiscordPresence.in_queue:
                    DiscordPresence.timestamp = int(time.time())
                    DiscordPresence.in_queue = True
                DiscordPresence.queue_presence(data[0])
        else:
            # if we have a current ip, then who cares, lets keep querying
            if Query.current_ip != "" and Query.current_port != "":
                server_info = Query.query_server(Query.current_ip, Query.current_port)
                DiscordPresence.server_presence(server_info)
            else:
                DiscordPresence.in_queue = False
                print("On main menu!")
                if not DiscordPresence.on_main_menu:
                    DiscordPresence.on_main_menu = True
                    DiscordPresence.timestamp = int(time.time())
                DiscordPresence.main_menu_presence()
    except:
        print(f'Something messed up querying the server or updating RPC! Error: {sys.exc_info()[0]}')

    Parser.cache_console_log()
    if Parser.cache_fails >= 5 and Query.current_ip != "":
        print("console.log hasn't changed in 5 cycles, resetting IP...")
        Query.current_ip = ""
        Query.current_port = ""
        Query.timestamp = int(time.time())
        Parser.cache_fails = 0

    Parser.clear_console_log()

# Load stuff initially
while True:
    if is_discord_running():
        print("Connected to RPC!")
        # rpc might not still be running so lets just wait 10 seconds to be sure
        time.sleep(10)
        Query = QueryHandler()
        Parser = ParserHandler()
        DiscordPresence = PresenceHandler()
        DiscordPresence.discord_running = True
        break
    print("Couldn't connect to RPC initially!")
    time.sleep(30)

# Start of actual program
while True:
    discord = is_discord_running()
    tf2 = is_tf2_running()
    if not tf2:
        if not DiscordPresence.cleared_presence:
            DiscordPresence.tf2_running = False
            print("TF2 isn't running! Clearing RPC and console.log..")
            Parser.clear_console_log()
            if discord:
                DiscordPresence.RPC.clear()
                DiscordPresence.cleared_presence = True
                DiscordPresence.timestamp = int(time.time())
            else:
                print("Couldn't clear RPC!")
        time.sleep(20)
        continue
    if not discord:
        print("Discord isn't running!")
        DiscordPresence.discord_running = False
        time.sleep(20)
        continue
    if DiscordPresence.discord_running == False:
        DiscordPresence.discord_running = True
        DiscordPresence.RPC.connect()
    if DiscordPresence.tf2_running == False:
        DiscordPresence.tf2_running = True
        DiscordPresence.timestamp = int(time.time())
    main_loop()
    time.sleep(20)
    