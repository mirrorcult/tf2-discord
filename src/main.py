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
import random

# globals
server_ip = ""

RPC = Presence(client_id)
RPC.connect()

def parse_console_log():
    pass

def clear_console_log():
    pass

# Converts a name of a map (i.e. koth_viaduct) to its image value in the Rich Presence app (viaduct)
def map_name_to_map_image(name):
    for map_name, image in maps.items():
        if map_name in name: return image 

# Main loop
while True:
    try:
        if server_ip != "":
            with ServerQuerier(("167.114.32.85", 27015), timeout=60) as server:
                details = server.info()["server_name"]
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
                server.close()
        else:
            RPC.update(
                small_image="tf2button", 
                small_text="TF2 Rich Presence by cyclowns#1440", 
                large_image="mainmenu",
                large_text="Main Menu",
                details="Main Menu"
            )
        time.sleep(15)
    except NoResponseError:
        print("Got no response from server! Resetting IP...")
