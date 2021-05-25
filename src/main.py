#!/usr/bin/env python3

from valve.source.a2s import ServerQuerier, NoResponseError
from socket import gaierror
import logging.config
import psutil
import asyncio

from parsing import ConsoleLogParser
from presence import PresenceHandler
from config import LOGGING_CONFIG, LOGGING_PATH, INSTALL_PATH

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("tf2discord")


async def tf2_running() -> bool:
    """Returns true if TF2 is currently running."""
    for proc in psutil.process_iter():
        try:
            # checking exe name just in case its like, actually HL2
            if "hl2" in proc.name().lower() and "Team Fortress" in proc.exe():
                return True
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


async def discord_running() -> bool:
    """Returns True if Discord is currently running."""
    for proc in psutil.process_iter():
        try:
            if "discord" in proc.name().lower():
                return True
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False


async def query_server(ip, port):
    """Queries a server with the given IP and port"""
    try:
        with ServerQuerier((ip, int(port)), timeout=60) as server:
            log.info(f"Queried server {ip}:{port}!")
            return server.info()
    except NoResponseError:
        log.error(f"No response received from {ip}!")
        return None
    except gaierror:
        log.error(f"Couldn't get server info from {ip}!")
        return None


class TF2Discord:
    def __init__(self):
        # set in run()
        self.discord = PresenceHandler()
        self.parser = ConsoleLogParser()  # TODO check for exceptions here
        self.parser.clear_console_log()

        self.current_ip = ""
        self.current_port = ""

    async def check_running(self) -> bool:
        """Checks if TF2 and Discord are running.
        If either isn't, then sleep and check later.
        If it's running now, then return control flow to run()."""

        if not await tf2_running():
            if not self.discord.cleared_presence:
                log.info("TF2 isn't running! Clearing RPC and console.log..")
                self.parser.clear_console_log()
                if await discord_running():
                    # Discord up, TF2 not running
                    self.discord.RPC.clear()
                    self.discord.cleared_presence = True
                    self.discord.timestamp = int(time.time())
                else:
                    log.info("Couldn't clear RPC, discord not running!")
        else:
            if not discord_running():
                log.info("Discord isn't running but TF2 is!")
            else:
                log.info("Discord and TF2 are running!")
                return True
        return False

    async def run(self) -> None:
        """Main program entry point."""
        if not await self.check_running(): return
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
                if server_info:
                    self.discord.server_presence(server_info)
        else:
            # if we have a current ip, then who cares, lets keep querying
            if self.current_ip != "" and self.current_port != "":
                server_info = query_server(self.current_ip, self.current_port)
                if server_info:
                    self.discord.server_presence(server_info)
            else:
                if not self.discord.on_main_menu:
                    self.discord.timestamp = int(time.time())
                self.discord.main_menu_presence()

        self.parser.cache_console_log()
        if self.parser.cache_fails >= 5 and self.current_ip != "":
            log.info("Console.log hasn't changed in 5 cycles,\
            resetting stored IP.")
            self.current_ip = ""
            self.current_port = ""
            self.discord.timestamp = int(time.time())
            self.parser.cache_fails = 0
        self.parser.clear_console_log()

if __name__ == "__main__":
    # truncate logfile
    with open(LOGGING_PATH, "w") as f:
        pass
    loop = asyncio.get_event_loop()
    tf2d = TF2Discord()
    asyncio.run_(tf2d.run())
