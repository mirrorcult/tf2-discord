import logging.config
import os
import codecs
import re

from config import LOGGING_CONFIG, INSTALL_PATH
from errors import NoPathFileError, InvalidConsoleLogPathError

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("parser")


class ConsoleLogParser:
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

        CL_PATH_LINUX = "/steamapps/common/Team Fortress 2/tf/console.log"
        CL_PATH_WIN = "\\steamapps\\common\\Team Fortress 2\\tf\\console.log"

        pathdat = os.path.join(INSTALL_PATH, "path.dat")
        if os.path.isfile(pathdat):
            with open(pathdat, "r") as file:
                steampath = file.read().rstrip()
                if os.path.isfile(steampath + CL_PATH_LINUX):
                    log.info(f"Running Linux! Found console_log_path at {steampath + CL_PATH_LINUX}")
                    return steampath + CL_PATH_LINUX
                elif os.path.isfile(steampath + CL_PATH_WIN):
                    log.info(f"Running Windows! Found console log path at {steampath + CL_PATH_WIN}")
                    return steampath + CL_PATH_WIN
                else:
                    raise InvalidConsoleLogPathError(steampath, "Invalid path given. Either it does not refer to a Steam installation with TF2 in it, or you haven't added -condebug to your launch options.")
        else:
            raise NoPathFileError(pathdat, "No path.dat file could be found at the expected location")

    def parse_console_log(self):
        """Parses the console.log file and returns the IP and port
        of the connected server, if found."""

        log.debug("Parsing console.log..")
        with codecs.open(self.console_log_path, "r", encoding="utf-8", errors="ignore") as clog:
            lines = clog.readlines()
            data = []
            for line in lines:
                if line.startswith("Connecting to"):
                    line_stripped = re.sub(self.whitelist_regex, "", line)
                    ip = re.search(self.ip_regex, line_stripped).group(0)
                    port_unstripped = re.search(self.port_regex, line_stripped).group(0)
                    # first char is a : which we need to get rid of
                    port = port_unstripped[1:]
                    data.append("server")
                    data.append((ip, port))
                    log.info(f"Found connected server {ip}:{port}!")
                    break
            return data

    def clear_console_log(self):
        """Clears the content of the console.log file."""

        log.info("Cleared console.log!")
        open(self.console_log_path, "w").close()

    def cache_console_log(self):
        """Caches the console.log file, and checks if the cache has
        changed at all. If it hasn't, it ups a counter (cache_fails).
        If this counter reaches 5, the program assumes you're on
        the main menu."""

        f = codecs.open(self.console_log_path, "r", encoding="utf-8", errors="ignore")
        to_cache = f.read()
        if to_cache == self.current_cache:
            self.cache_fails += 1
        else:
            self.cache_fails = 0
        self.current_cache = to_cache
        f.close()
