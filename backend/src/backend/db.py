import psycopg2
from constants import POSTGRES_URL, CREATE_TABLES_QUERY, DROP_TABLES_QUERY


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(POSTGRES_URL)
        self.cursor = self.connection.cursor()
    def __del__(self):
        self.connection.close()

    def create_tables(self):
        self.cursor.execute(CREATE_TABLES_QUERY)
        self.connection.commit()

    def drop_tables(self):
        self.cursor.execute(DROP_TABLES_QUERY)
        self.connection.commit()
    
    def add_test_data(self):
        # TODO
        self.connection.commit()

    def register_user(self):
        # TODO
        self.connection.commit()

    def login_user(self):
        # TODO
        self.connection.commit()

    def get_history_route(self):
        # TODO
        pass
    

database = Database()