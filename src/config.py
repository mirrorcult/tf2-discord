import os

CLIENT_ID = "451950787996680192"

INSTALL_PATH_LINUX = "/usr/share/tf2-rich-presence"
LOG_PATH_LINUX = "/var/log/tf2discord.log"
INSTALL_PATH_WINDOWS = "C:\\Program Files (x86)\\tf2-rich-presence"
LOG_PATH_WINDOWS = os.path.join(os.getenv('LOCALAPPDATA'), "tf2discord.log")

MAPS = {
        "surf_": "surf",
        "jump_": "jump",
        "bhop_": "bhop",
        "cp_orange_": "orange",
        "mge_": "mge",
        "trade_": "trade",
        "achievement_": "achievementidle",
        "pl_vigil": "vigil",
        "koth_cascade": "cascade",
        "cp_cardinal": "cardinal",
        "koth_ramjam": "ramjam",
        "koth_ashville": "ashville",
        "koth_coalplant": "coalplant",
        "koth_airfield": "airfield",
        "cp_warmfrost": "warmfrost",
        "ctf_2fort": "2fort",
        "ctf_2fort_invasion": "2fortinvasion",
        "cp_5gorge": "5gorge",
        "rd_asteroid": "asteroid",
        "cp_badlands": "badlands",
        "cp_prolands": "badlands",
        "koth_badlands": "badlands",
        "arena_badlands": "badlands",
        "pl_badwater": "badwater",
        "plr_bananabay": "bananabay",
        "pl_barnblitz": "barnblitz",
        "mvm_bigrock": "bigrock",
        "pl_borneo": "borneo",
        "koth_brazil": "brazil",
        "pass_brickyard": "brickyard",
        "pl_fifthcurve_event": "brimstone",
        "arena_byre": "byre",
        "pl_cactuscanyon": "cactuscanyon",
        "sd_doomsday_event": "carnage",
        "cp_cloak": "cloak",
        "mvm_coaltown": "coaltown",
        "cp_coldfront": "coldfront",
        "mvm_decoy": "decoy",
        "cp_degrootkeep": "degrootkeep",
        "pass_district": "district",
        "sd_doomsday": "doomsday",
        "ctf_doublecross": "doublecross",
        "cp_dustbowl": "dustbowl",
        "tr_dustbowl": "dustbowl",
        "cp_egypt_final": "egypt",
        "pl_enclosure_final": "enclosure",
        "mvm_example": "example",
        "cp_fastlane": "fastlane",
        "cp_foundry": "foundry",
        "ctf_foundry": "foundry",
        "cp_freight_final1": "freight",
        "pl_frontier_final": "frontier",
        "mvm_ghost_town": "ghosttown",
        "pl_goldrush": "goldrush",
        "cp_gorge": "gorge",
        "ctf_gorge": "gorge",
        "cp_gorge_event": "gorgeevent",
        "cp_granary": "granary",
        "arena_granary": "granary",
        "cp_gravelpit": "gravelpit",
        "cp_gullywash_final1": "gullywash",
        "koth_harvest_final": "harvest",
        "koth_harvest_event": "harvestevent",
        "ctf_hellfire": "hellfire",
        "koth_highpass": "highpass",
        "plr_hightower": "hightower",
        "plr_hightower_event": "hightowerevent",
        "pl_hoodoo_final": "hoodoo",
        "tc_hydro": "hydro",
        "itemtest": "itemtest",
        "cp_junction_final": "junction",
        "koth_king": "kongking",
        "koth_lakeside_final": "lakeside",
        "koth_lakeside_event": "lakesideevent",
        "ctf_landfall": "landfall",
        "koth_lazarus": "lazarus",
        "arena_lumberyard": "lumberyard",
        "mvm_mannhattan": "mannhattan",
        "cp_manor_event": "mannmanor",
        "mvm_mannworks": "mannworks",
        "koth_maple_ridge": "mapleridge",
        "cp_mercenarypark": "mercpark",
        "cp_metalworks": "metalworks",
        "pl_millstone_event": "millstoneevent",
        "koth_moonshine_event": "moonshine",
        "cp_mossrock": "mossrock",
        "cp_mountainlab": "mountainlab",
        "plr_nightfall_final": "nightfall",
        "koth_nucleus": "nucleus",
        "arena_nucleus": "nucleus",
        "arena_offblast_final": "offblast",
        "plr_pipeline": "pipeline",
        "pd_pit_of_death_event": "pitofdeath",
        "cp_powerhouse": "powerhouse",
        "koth_probed": "probed",
        "cp_process_final": "process",
        "koth_product": "product",
        "arena_ravine": "ravine",
        "mvm_rottenburg": "rottenburg",
        "koth_sawmill": "sawmill",
        "arena_sawmill": "sawmill",
        "ctf_sawmill": "sawmill",
        "cp_sunshine_event": "sinshine",
        "cp_snakewater": "snakewater",
        "cp_snowplow": "snowplow",
        "pl_snowycoast": "snowycoast",
        "cp_standin": "standin",
        "cp_steel": "steel",
        "koth_suijin": "suijin",
        "cp_sunshine": "sunshine",
        "pl_swiftwater": "swiftwater",
        "tr_target": "target",
        "pl_thundermountain": "thundermountain",
        "pass_timberlodge": "timberlodge",
        "ctf_turbine": "turbine",
        "pl_upward": "upward",
        "cp_vanguard": "vanguard",
        "koth_viaduct": "viaduct",
        "koth_viaduct_event": "viaductevent",
        "arena_watchtower": "watchtower",
        "pd_watergate": "watergate",
        "cp_well": "well",
        "ctf_well": "well",
        "arena_well": "well",
        "cp_yukon": "yukon"
}

log_path = ""
if os.path.isdir(INSTALL_PATH_LINUX):
    log_path = LOG_PATH_LINUX
elif os.path.isdir(INSTALL_PATH_WINDOWS):
    log_path = LOG_PATH_WINDOWS

# truncate log path
with open(log_path, 'w'):
    pass

LOGGING_CONFIG = {
    "version": 1.0,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s %(name)s %(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": log_path,
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False
        },
        "parser": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "presence": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        },
        "tf2discord": {
            "handlers": ["console", "file"],
            "level": "DEBUG",  # a little less important
            "propagate": False,
        },
    }
}