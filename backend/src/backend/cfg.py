from copy import copy
import io
import os
from os import path
import tomllib
from typing import Any, TypedDict, Optional, Dict, NotRequired

from typeguard import check_type


class DictAttr(dict):
    """Dictionary wrapper that allows attribute access to get/set values."""
    # Normally we'd use __getattr__ but in this case we want to plow through
    # the default attributes on dict (e.g. update, keys, items, values, etc.)
    def __getattribute__(self, name: str) -> Any:
        # Plowing through magic methods breaks shit, so uh don't
        if name.startswith("__") and name.endswith("__"):
            return getattr(super(), name)

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
    def __init__(self, config: Dict[str, Any], /, *, type_check: bool = True):
        if type_check:
            check_type(config, TypedDict("Config", **self.__annotations__))
        self.__dict__ = dict_attr(config)

    def __add__(self, rhs: "Config") -> "Config":
        mixed = {**self.__dict__, **rhs.__dict__}
        return Config(mixed, type_check = False)

    @staticmethod
    def from_toml_file(path: str | os.PathLike) -> "Config":
        with io.open(path, "rb") as config:
            return Config(tomllib.load(config))

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
