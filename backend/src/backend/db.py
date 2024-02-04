import re
from string import Formatter
from typing import Self

from psycopg import AsyncConnection, AsyncCursor
from backend import config, logger


_RE_CONX_ESCAPE = re.compile(r"(['\\])")


class Database:
    conx: AsyncConnection

    def __init__(self, conx: AsyncConnection):
        self.conx = conx

    @staticmethod
    async def connect() -> Self:
        params = {
            "host": config.db.host,
            "port": config.db.get("port"),
            "dbname": config.db.dbname,
            "user": config.db.get("user"),
            "password": config.db.get("password"),
        }

        conx_str = ""
        for (key, val) in params.items():
            if val is not None:
                val = _RE_CONX_ESCAPE.sub(repl=r"\\\1", string=str(val))
                conx_str += f"{key}='{val}' "

        conx_str = conx_str.rstrip()

        logger.debug("connecting to db: " + conx_str)
        return Database(
            await AsyncConnection.connect(
                conx_str,
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

    def transaction(self): return self.conx.transaction()



    def create_tables(self):
        # self.cursor.execute(CREATE_TABLES_QUERY)
        self.conx.commit()

    def drop_tables(self):
        # self.cursor.execute(DROP_TABLES_QUERY)
        self.conx.commit()

    def add_test_data(self):
        # TODO
        self.conx.commit()

    def register_user(self):
        # TODO
        self.conx.commit()

    def login_user(self):
        # TODO
        self.conx.commit()

    def get_history_route(self):
        # TODO
        pass


database = Database()
