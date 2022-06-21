from typing import Any
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor as Cursor
from psycopg2 import OperationalError, errorcodes, errors, connect as pg_connect

from config import Config

import sys

##
#   Higher level Exceptions for DB
##
class EmptySQLQueryException(TypeError):
    pass
class NoDatabaseConnection(Exception):
    pass
class NoDatabaseRecordFound(Exception):
    pass

def print_psycopg2_exception(err):
    """ Psycopg errors printer. """
    err_type, err_obj, traceback = sys.exc_info()

    if traceback:
        line_num = traceback.tb_lineno

        # print the connect() error
        print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print ("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)

        # print the pgcode and pgerror exceptions
        print ("pgerror:", err.pgerror)
        print ("pgcode:", err.pgcode, "\n")

##
##  DB Access Layer
## 
class DBLayerAccess:
    """ Database Layer Access to communicate with DB. """

    def __init__(self, config: Config, debug=False):
        self.config = config
        self.debug = debug
    
    def connect(self):
        try:
            self.connection = pg_connect(
                user        = self.config.db_user,
                password    = self.config.db_pwd,
                host        = self.config.db_host,
                port        = self.config.db_port,
                database    = self.config.db_name
            )
        except (OperationalError) as error:
            print_psycopg2_exception(error)
            self.connection = None

    def commit(self):
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")
        self.connection.commit()
    
    def close(self):
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")
        self.connection.close()

    def execute(self, query: str, placeholder: tuple[str, ...] | dict[str, str] | None = None) -> list[dict] | None:
        """ Execute method abstraction. """
        if not self.connection: raise NoDatabaseConnection("Connection does not exist.")

        if not query: raise EmptySQLQueryException("SQL Query provided is Null.")

        with self.connection.cursor(cursor_factory = RealDictCursor) as cur:
            try:
                cur.execute(query, placeholder)
                res = cur.fetchall()
                self.commit()
            except Exception as error:
                if self.debug: print_psycopg2_exception(error)
                res = None
            return res # type: ignore