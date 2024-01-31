"""CLI tools for setting up config and performing database migrations.

Installed on your path with installation of the package."""

from os import path
import io
import random
import re
import shutil
import string

from backend import MODULE_ROOT
import backend.cfg


def setup_cfg():
    if path.isfile(path.join(MODULE_ROOT, "config.toml")):
        logger.warning(f"config.toml already exists; not overwriting")
        return

    shutil.copy(
        path.join(MODULE_ROOT, "config.default.toml"),
        path.join(MODULE_ROOT, "config.toml")
    )

    jwt_secret = "".join(random.choices(string.ascii_letters + string.digits, k=128))

    with io.open(path.join(MODULE_ROOT, "config.toml"), "r+") as file:
        toml = file.read()

        toml = re.sub(
            pattern=r"""jwt_secret\s*=\s*["'].*?["'].*""",
            repl=f"jwt_secret = \"{jwt_secret}\"",
            string=toml
        )

        file.seek(0)
        file.write(toml)

    logger.info(f"generated config.toml")
