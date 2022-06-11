from typing import Any
import psycopg2
import psycopg2.extras

from psycopg2.extras import RealDictCursor, RealDictConnection, RealDictRow

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

    def commit(self):
        self.connection.commit()
    
    def close(self):
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")
        
        self.connection.close()
        print("DB Success - Connection to DB closed")

    #def fetch_one(self, cursor: Cursor, sql: str) -> dict | None:
    #    """ Method used to execute a query which returns exactly one record if found. """
    #    cursor.execute(sql)
    #    res = cursor.fetchone()
    #    self.commit()
    #    return RealDictRow(res)

    def execute(self, cursor: Cursor, sql: str) -> list[dict] | None:
        """ Method used to execute a query which returns multiple records if found. """
        cursor.execute(sql)
        res = cursor.fetchall()
        self.commit()
        return res #type: ignore
                        
    def select(self, sql) -> list[dict] | None:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            return self.execute(cur, sql)
    
    def insert(self, sql: str) -> list[dict] | None:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            return self.execute(cur, sql)

    def update(self, sql:str) -> list[dict] | None:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not sql: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            return self.execute(cur, sql)