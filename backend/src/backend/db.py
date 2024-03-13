"""Database connection stuff."""


import asyncio
import re
from string import Formatter
from typing import Self
import functools

from psycopg import AsyncConnection, AsyncCursor, AsyncTransaction
from psycopg.rows import dict_row

from backend import config, logger


_RE_CONX_ESCAPE = re.compile(r"(['\\])")


class Database:
    conx: AsyncConnection

    def __init__(self, conx: AsyncConnection):
        self.conx = conx

    @staticmethod
    async def connect() -> Self:
        logger.debug("connecting to db: " + config.db.conx)
        return Database(
            await AsyncConnection.connect(
                config.db.conx,
                # make .fetch methods produce dicts by default, instead of tuples
                row_factory=dict_row,
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

    @functools.wraps(AsyncConnection.cursor)
    def cursor(self, **kwargs) -> AsyncCursor: return self.conx.cursor(**kwargs)

    # fixme: this does not work with async connections!! different async threads will interefere with transactions!
    # fixme: use a connection pool instead!
    @functools.wraps(AsyncConnection.transaction)
    def transaction(self, **kwargs) -> AsyncTransaction: return self.conx.transaction(**kwargs)
