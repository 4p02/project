import logging
from logging import Logger
from os import path

from backend.cfg import Config

__all__ = ["logger", "config", "MODULE_ROOT"]


MODULE_ROOT: str = path.join(path.dirname(__file__), "../../")

logger: Logger = logging.getLogger()
config: Config = None

def __init__():
    global logger
    global config

    config = Config.from_toml_file(path.join(MODULE_ROOT, "config.default.toml"))
    logger.addHandler(log_handler := config.into_log_handler())
    logger.setLevel(config.log_level.upper())

    if path.isfile(path.join(MODULE_ROOT, "config.toml")):
        config += Config.from_toml_file(path.join(MODULE_ROOT, "config.toml"))
        logger.removeHandler(log_handler)
        logger.addHandler(log_handler := config.into_log_handler())
        logger.setLevel(config.log_level.upper())

        logger.info("configuration from config.toml loaded")
    else:
        logger.warning("no config.toml present; configuration from config.default.toml loaded instead")

__init__()
