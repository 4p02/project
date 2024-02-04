"""CLI tools for setting up config and performing database migrations.

Installed on your path with installation of the package."""

import glob
import io
from os import path
import random
import re
import shutil
import string

from psycopg.pq import error_message as pg_error_message

from backend import MODULE_ROOT, logger, config
from backend.db import Database
from backend.misc import asyncio_entrypoint
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


@asyncio_entrypoint
async def migrate_db():
    async with (await Database.connect()) as db:
        MIGRATIONS_ROOT = path.join(MODULE_ROOT, "db")
        migrations = glob.glob(
            "**/*.sql", root_dir=MIGRATIONS_ROOT,
            include_hidden=False,
            recursive=True
        )
        migrations.sort()
        logger.info(f"found {len(migrations)} migrations")
        logger.info(f"current tracked migration: {config.db.current_migration or 'none'}")

        with io.open(path.join(MODULE_ROOT, "config.toml"), "r+") as config_file:
            migrations_applied = 0
            for migration_path in filter(lambda path: path > config.db.current_migration, migrations):
                logger.info(f"applying migration: {migration_path}")
                with io.open(path.join(MIGRATIONS_ROOT, migration_path), "r") as migration:
                    # actually apply the migration
                    # todo: this is shit; abstract this away into Database plz
                    res = (await db.cursor().execute(migration.read())).pgresult
                    logger.info(pg_error_message(res))

                config.db.current_migration = migration_path

                config_file.seek(0)
                new_toml = re.sub(
                    pattern=r"""current_migration\s*=\s*["'].*?["'].*?""",
                    repl=f"current_migration = \"{config.db.current_migration}\"",
                    string=config_file.read()
                )
                config_file.seek(0)
                config_file.write(new_toml)
                config_file.truncate()
                migrations_applied += 1

        if migrations_applied == 0:
            logger.info(f"no migrations to apply; nothing to do")
        else:
            logger.info(f"{migrations_applied} migrations applied; now at tracking: {config.db.current_migration or 'none'}")
