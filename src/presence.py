import time
import sys
import logging.config

from pypresence import Presence, exceptions

from config import CLIENT_ID, MAPS, LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("presence")


def map_name_to_map_image(name):
    """Converts a name of a map (i.e. koth_viaduct) to its image value
    in the Rich Presence app (i.e viaduct)"""
    for map_name, image in MAPS.items():
        if map_name in name:
            return image
    return "unknown"


class PresenceHandler:
    """Handles changing and updating discord rich presence."""
    def __init__(self):
        self.RPC = Presence(CLIENT_ID)
        self.attempt_connection()
        self.cleared_presence = False
        self.timestamp = int(time.time())
        self.on_main_menu = False

    def attempt_connection(self):
        """Attempts to connect to discord RPC. If discord isn't open, then
        try again later."""

        try:
            log.info("Connecting to RPC...")
            # this throws like 20 different exceptions
            # for 500 different reasons if discord isnt up
            self.RPC.connect()
        except:  # so fuck it. bare except
            log.debug(sys.exc_info()[0])
            log.warning("Couldn't connect to RPC! Trying again in 30 seconds.")
            self.attempt_connection()
        log.info("Connected to RPC!")

    def server_presence(self, info):
        details = info["server_name"]
        if details[0] == chr(1):
            # sometimes server names will have a bunch of
            # chars with code 1 at the beginning, so we remove them
            # not sure why that is.
            details = details.replace(chr(1), "")
        large_text = info["map"]
        large_image = map_name_to_map_image(info["map"])

        # player_count can be off slightly, which messes with everything
        if info["player_count"] == 0:
            party_size = (info["player_count"] + 1, info["max_players"])
        else:
            party_size = (info["player_count"], info["max_players"])

        try:
            self.RPC.update(
                small_image="tf2button",
                small_text="TF2 Discord by cyclowns#1440",
                large_image=large_image,
                large_text=large_text,
                details=details,
                state="Playing",
                party_size=party_size,
                start=self.timestamp
            )
            log.info(f'Updated presence for server {info["server_name"]}!')
        except exceptions.InvalidID:
            log.error("Couldn't update server presence, RPC not connected / messed up for some reason!")

    def main_menu_presence(self):
        self.on_main_menu = True
        try:
            self.RPC.update(
                small_image="tf2button",
                small_text="TF2 Discord by cyclowns#1440",
                large_image="mainmenu",
                large_text="Main Menu",
                details="Main Menu",
                start=self.timestamp
            )
            log.info("Updated presence to main menu!")
        except exceptions.InvalidID:
            log.error("Couldn't update menu presence, RPC not connected / messed up for some reason!")
