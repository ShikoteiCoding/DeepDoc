from typing import Any, Optional
import psycopg2

from psycopg2.extras import RealDictCursor
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

    def pg_execute(self, cursor: Cursor, sql: str, placeholder: tuple[str,...] | None) -> list[dict] | None:
        cursor.execute(sql, placeholder)
        res = cursor.fetchall()
        self.commit()
        return res #type: ignore

    def execute(self, query: str, placeholder: tuple[str,...] | None = None) -> list[dict] | None:
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not query: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor(cursor_factory = RealDictCursor) as cur:
            return self.pg_execute(cur, query, placeholder)