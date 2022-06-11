from typing import Any
import psycopg2
from psycopg2.extensions import cursor as Cursor
from config import Config

##
#   Higher level Exceptions for DB
##

class EmptySQLQueryException(TypeError):
    pass
class NoDatabaseConnection(Exception):
    pass
class NoDatabaseRecordFound(Exception):
    pass

##
##  DB Access Layer
## 
class DBLayerAccess:
    """ Database Layer Access to communicate with DB. """

    def __init__(self, config: Config):
        self.config = config
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user        = self.config.db_user,
                password    = self.config.db_pwd,
                host        = self.config.db_host,
                port        = self.config.db_port,
                database    = self.config.db_name
            )
            print("DB Success - Connection to DB created")
        except (psycopg2.OperationalError) as error:
            print(error)
    
    def close(self):
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")
        
        self.connection.close()
        print("DB Success - Connection to DB closed")

    def fetch_one(self, cursor: Cursor, sql: str) -> tuple[Any, ...] | None:
        """ Method used to execute a query which returns exactly one record. """
        cursor.execute(sql)
        res = cursor.fetchone()
        self.connection.commit()
        return res

    def fetch_multiple(self, cursor: Cursor, sql: str) -> list[tuple]:
        cursor.execute(sql)
        res = cursor.fetchall()
        self.connection.commit()
        return res

    def execute_fetch_one(self, sql: str) -> tuple:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor() as cur:
            return self.fetch_one(cur, sql)
                        
    def execute_fetch_all(self, sql) -> list[tuple]:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor() as cur:
            return self.fetch_multiple(cur, sql)
    
    def execute_insert(self, sql: str) -> tuple:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor() as cur:
            return self.fetch_one(cur, sql)

    def execute_update(self, sql:str) -> tuple:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor() as cur:
            return self.fetch_one(cur, sql)