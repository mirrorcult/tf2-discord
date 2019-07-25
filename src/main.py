# TODO: Get tf2-rich-presence running on Windows and Linux
# TODO: Make sure connecting to server + querying information works
# TODO: Make sure mapping the map name to an image in config.py works
# TODO: Make sure updating RPC works
# TODO: Make sure reading console.log file works (and that it works on Windows and Linux)

from config import *
from pypresence import Presence
from valve.source.a2s import ServerQuerier
from valve.source import NoResponseError
import time
import sys
import re

# globals
server_ip = ""
server_port = ""
ip_regex = r".+?(?=:)"
port_regex = r":[0-9]+"
current_cache = ""
cache_fails = 0

# check if console_log_path exists
if not ('console_log_path' in globals() or 'console_log_path' in locals()):  # should be in config.py if installed correctly
    print("Couldn't find console_log_path! Did you install correctly?")
    sys.exit()

RPC = Presence(client_id)
RPC.connect()

# Parses console.log file for ip and port
def parse_console_log():
    with open(console_log_path, 'r') as log:
        lines = log.readlines()
        for line in lines:
            if line.startswith("Connecting to"):
                ip = re.search(ip_regex, line[14:]).group(0) # after first 14 is actual ip/port
                port_unstripped = re.search(port_regex, line).group(0) # first char is a : which we need to get rid of
                port = port_unstripped[1:]
                return (ip, port)
        return ("", "")

# Clears console.log completely
def clear_console_log():
    open(console_log_path, 'w').close()

# Caches the console.log file, and checks if the
# cache has changed at all. If it hasn't, it ups a counter. (cache_fails)
# If this counter reaches 5, then the game assumes you're on the main menu
def cache_console_log():
    global current_cache
    global cache_fails
    to_cache = open(console_log_path, 'r').read()
    if to_cache == current_cache: cache_fails += 1
    else: cache_fails = 0

    current_cache = to_cache

# Converts a name of a map (i.e. koth_viaduct) to its image value in the Rich Presence app (viaduct)
def map_name_to_map_image(name):
    for map_name, image in maps.items():
        if map_name in name: return image 
    return "unknown"

# Queries the server specified by ip and port and updates rich presence
def query_server_and_update(ip, port):
    cache_console_log()
    with ServerQuerier((ip, int(port)), timeout=60) as server:
        details = server.info()["server_name"]
        if details[0] == chr(1):
            details = details.replace(chr(1), '') # sometimes server names will have a bunch of chars with code 1 at the beginning, so we remove them
        large_text = server.info()["map"]
        large_image = map_name_to_map_image(server.info()["map"])
        if server.info()["player_count"] == 0: party_size = (server.info()["player_count"] + 1, server.info()["max_players"]) # player_count can be off slightly, which messes with everything
        else: party_size = (server.info()["player_count"], server.info()["max_players"])

        RPC.update(
            small_image="tf2button", 
            small_text="TF2 Rich Presence by cyclowns#1440",
            large_image=large_image,
            large_text=large_text,
            details=details,
            state="Playing",
            party_size=party_size
        )
    time.sleep(20)

# clear once beforehand
clear_console_log()

# Main loop
while True:
    try:
        (ip, port) = parse_console_log()
        if ip != "":
            clear_console_log()
            if ip != server_ip:
                print(f'Found server at {ip}')
                server_ip = ip
                cache_fails = 0
                query_server_and_update(ip, port)
        elif server_ip == "":
            RPC.update(
                small_image="tf2button", 
                small_text="TF2 Rich Presence by cyclowns#1440", 
                large_image="mainmenu",
                large_text="Main Menu",
                details="Main Menu"
            )
        else:
            if cache_fails >= 5:
                print("console.log hasn't changed in 5 cycles, resetting IP...")
                server_ip = ""
                cache_fails = 0
    except NoResponseError:
        print("Got no response from server! Resetting IP...")
        server_ip = ""
    time.sleep(15)
