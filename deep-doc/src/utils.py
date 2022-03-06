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
##  DB Access Layer
## 
import psycopg2
from datetime import date

class DBLayerAccess:
    def __init__(self, config):
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
            print("Error while connecting to DB: ", error)
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("All DB connections have been closed")

    def create_piece(self, piece):
        # TODO: Load the model, not beautiful to hardcode

        current_timestamp = date.today()
        sql = f"""
        INSERT INTO piece VALUES (
            '1',
            '{piece.content}',
            '{current_timestamp}',
            '{current_timestamp}'
        )
        """

        cursor = self.connection.cursor()
        cursor.execute(sql)

        print("Piece created")
        
        if cursor:
            cursor.close()

    def create_doc(self, doc):
        # TODO: Load the model, not beautiful to hardcode

        current_timestamp = date.today()
        sql = f"""
        INSERT INTO piece VALUES (
            '1',
            '{doc.content}',
            '{current_timestamp}',
            '{current_timestamp}'
        )
        """

        print("Doc created")

        cursor = self.connection.cursor()
        cursor.execute(sql)
        
        if cursor:
            cursor.close()

##
##  Classes for database access layer
##
class Piece:
    def __init__(self, content):
        self.content = content

class Doc:
    def __init__(self, content):
        self.content = content