from copy import copy
import io
import logging
from logging import Logger, Formatter, StreamHandler, Handler
from logging.handlers import SysLogHandler
import os
from os import path
import sys
import tomllib
from typing import Any, TypedDict, Optional, Dict, NotRequired, Union, Literal

from typeguard import check_type, TypeCheckError


logger: Logger = logging.getLogger()

class DictAttr(dict):
    """Dictionary wrapper that allows attribute access to get/set items."""
    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as ex:
            raise AttributeError(*ex.args)

    __setattr__ = dict.__setitem__


def dict_attr(_dict: Dict) -> DictAttr:
    """Recursively wrap dictionaries in DictAttr."""
    _dict = DictAttr(_dict)
    for (key, value) in dict.items(_dict):
        if isinstance(value, dict) and not isinstance(value, DictAttr):
            _dict[key] = dict_attr(value)
    return _dict


class Config():
    def __init__(self, config: Dict[str, Any]):
        try:
            check_type(config, TypedDict("Config", **self.__annotations__))
        except TypeCheckError as ex:
            logger.critical(str(ex))
            exit()

        self.__dict__ = dict_attr(config)

    def __iadd__(self, rhs: "Config"):
        self.__dict__.update(rhs.__dict__)
        return self

    @staticmethod
    def from_toml_file(path: str | os.PathLike) -> "Config":
        with io.open(path, "rb") as config:
            return Config(tomllib.load(config))

    def into_log_handler(self) -> Handler:
        match self.log_target:
            case "stderr":
                handler = StreamHandler(sys.stderr)
            case "syslog":
                handler = SysLogHandler("/dev/log")

        handler.setLevel(self.log_level.upper())
        handler.setFormatter(Formatter("[%(levelname)s:%(filename)s:%(lineno)s] %(message)s"))
        return handler


    log_level: Union[int, Literal['debug', 'info', 'warning', 'error', 'critical']]
    log_target: Literal["stderr", "syslog"]
    jwt_secret: str

    api: TypedDict("api",
        host=str,
        port=int,
    )

    db: TypedDict("db",
        host=str,
        user=str,
        password=NotRequired[Optional[str]],
        database=str,
    )

    ollama: TypedDict("",
        endpoint=str,
        model=str,
    )
