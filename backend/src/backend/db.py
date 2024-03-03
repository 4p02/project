"""Database connection stuff."""


import asyncio
import re
from string import Formatter
from typing import Self

from psycopg import AsyncConnection, AsyncCursor
from psycopg.rows import dict_row

from backend import config, logger


_RE_CONX_ESCAPE = re.compile(r"(['\\])")


class Database:
    conx: AsyncConnection

    def __init__(self, conx: AsyncConnection):
        self.conx = conx
        # make cursor .fetch methods produce dicts by default, instead of tuples
        self.conx.row_factory = dict_row

    @staticmethod
    async def connect() -> Self:
        logger.debug("connecting to db: " + config.db.conx)
        return Database(
            await AsyncConnection.connect(
                config.db.conx,
                autocommit=True  # don't treat everything as a transaction
            )
        )

    # Both AsyncConnection and this class *must* be used in `async with` blocks
    # to ensure that when the connection is freed, any running transactions are
    # either rolled back or committed and the connection is closed to avoid
    # database inconsistencies or data loss on abnormal exit.
    async def __aenter__(self) -> Self:
        await self.conx.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.conx.__aexit__(*args, **kwargs)
        return

    def cursor(self) -> AsyncCursor: return self.conx.cursor()

    def transaction(self) -> AsyncTransaction: return self.conx.transaction()
