from typing import Any
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor as Cursor
from psycopg2 import OperationalError
from psycopg2.pool import SimpleConnectionPool
from psycopg2.errors import UndefinedColumn, UndefinedTable

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
    err_type, _, traceback = sys.exc_info()

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
    """ Database Layer Access to communicate with DB. Handle simple connection pooling. """

    def __init__(self, config: Config, debug=False):
        self.config = config
        self.debug = debug
    
    def connect(self):
        try:
            self.pool = SimpleConnectionPool(
                1, 1,
                user        = self.config.db_user,
                password    = self.config.db_pwd,
                host        = self.config.db_host,
                port        = self.config.db_port,
                database    = self.config.db_name
            )
        except (OperationalError) as error:
            if self.debug: print_psycopg2_exception(error)
            self.pool = None
    
    def close(self):
        if not self.pool: raise NoDatabaseConnection("Connection does not exist.")
        self.pool.closeall()

    def execute(self, query: str, placeholder: tuple[str, ...] | dict[str, str] | None = None) -> list[dict] | None:
        """ Execute method abstraction. """
        if not self.pool: raise NoDatabaseConnection("Connection does not exist.")

        if not query: raise EmptySQLQueryException("SQL Query provided is Null.")

        connection = self.pool.getconn()

        with connection.cursor(cursor_factory = RealDictCursor) as cur:
            try:
                cur.execute(query, placeholder)
                res = cur.fetchall()
                connection.commit()
            except (UndefinedTable, UndefinedColumn) as error:
                raise error
            except (Exception) as error:
                if self.debug: print_psycopg2_exception(error)
                res = None
            finally:
                self.pool.putconn(connection)
            return res # type: ignore