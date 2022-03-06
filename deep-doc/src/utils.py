import typing
##
## Project config
##
class Config:
    def __init__(self):
        self.db_host = "localhost"
        self.db_port = "5432"
        self.db_name = "postgres"
        self.db_user = "admin"
        self.db_pwd  = "admin"

##
##  Classes for the Datbase Object Model
##

# TODO: Load types through a schema to make cleaner
class Piece:
    def __init__(self, content):
        self.content = content

class Doc:
    def __init__(self, content):
        self.content = content

##
##  DB Access Layer
## 
import psycopg2
from datetime import datetime, timezone

class DBLayerAccess:
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
        except (Exception, psycopg2.Error) as error:
            print("DB Error - Unable to connect: ", error)
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("DB Success - All connections have been closed")

    def create_piece(self, piece: Piece):
        current_timestamp = datetime.now(timezone.utc)
        sql = f"""
        INSERT INTO pieces VALUES (
            '1',
            '{piece.content}',
            '{current_timestamp}',
            '{current_timestamp}'
        );
        """

        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            self.connection.commit()
            print("DB Success - A piece has been created")
        except (Exception) as error:
            print("DB Error - A piece insert has failed: ", error)
        finally:
            if cursor:
                cursor.close()

    def create_doc(self, doc: Doc):
        current_timestamp = datetime.now(timezone.utc)
        sql = f"""
        INSERT INTO docs VALUES (
            '1',
            '{doc.content}',
            '{current_timestamp}',
            '{current_timestamp}'
        );
        """

        cursor = self.connection.cursor()

        try:
            cursor.execute(sql)
            self.connection.commit()
            print("DB Success - A doc has been created")
        except (Exception) as error:
            print("BD Error - A doc insert has failed: ", error)
        finally:
            if cursor:
                cursor.close()
        

