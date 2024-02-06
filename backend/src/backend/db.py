"""Database connection stuff."""

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
        #will create this table inside my own server to test
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        """
        self.cursor.execute(create_users_table_query)
        self.connection.commit()


    def drop_tables(self):
        # self.cursor.execute(DROP_TABLES_QUERY)
        self.conx.commit()

    def add_test_data(self):
        # TODO
        self.conx.commit()

    #inserting users into the db, using name, email(username) and password
    def register_user(self, full_name, user_name, password):
        insert_user_query = """
        INSERT INTO users (fullname, username, password) VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(insert_user_query, (full_name, user_name, password))
            self.connection.commit()
            return True  # Return True if registration is successful
        except psycopg2.Error as e:
            print("Error registering user:", e)
            self.connection.rollback()
            return False  # Return False if registration fails

    #checking the database for the username and password
    def login_user(self,username, password):
        select_user_query = """
        SELECT id FROM users WHERE username = %s AND password = %s
        """
        try:
            self.cursor.execute(select_user_query, (username, password))
            user = self.cursor.fetchone()
            if user:
            # If user exists, return true
                return True
            else:
            # If user doesn't exist or credentials are incorrect, return None
                return False
        except psycopg2.Error as e:
            print("Error logging in user:", e)
            return False  # Return False if login fails

    def get_history_route(self):
        # TODO
        pass
