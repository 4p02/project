from os import path

from backend.cfg import Config


MODULE_ROOT: str = path.join(path.dirname(__file__), "../../")

config: Config = Config.from_toml_file(path.join(MODULE_ROOT, "config.default.toml"))

if path.isfile(path.join(MODULE_ROOT, "config.toml")):
    config = config + Config.from_toml_file(path.join(MODULE_ROOT, "config.toml"))
