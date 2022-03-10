from turtle import goto
import typing
from datetime import datetime, timezone
import json

SCHEMA_PATH = "../schema/"

def read_schema(path: str) -> dict:

    with open(path) as f:
        return json.load(f)

def pg_row_to_dict(row: tuple, schema: dict) -> dict:
    new_dict = {}

    for index, key in enumerate(schema.keys()):
        new_dict[key] = row[index]

    return new_dict

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
class Piece:

    schema = read_schema(SCHEMA_PATH + "piece.json")

    def __init__(self, values: dict):
        for key in Piece.schema:
            setattr(self, key, values.get(key))

    def __eq__(self, other):
        if (isinstance(other, Piece)):
            for key in Piece.schema:
                if not (getattr(self, key) == getattr(other, key)): return False
            return True

    def __str__(self):
        str_print = ''
        for key in Piece.schema:
            str_print += (key + ': ' + str(getattr(self, key)) + '\n')
        return str_print

    def update(self, values):
        for (key, value) in values.items():
            shema_attribute = Piece.schema.get(key)

            if not shema_attribute:
                print("Model Error - Attribute of Piece not existing in schema: ", key)

            if shema_attribute and Piece.schema.get(key).get("mutable"):
                setattr(self, key, value)
                print("Model Success - Attribute of Piece has been updated: ", key)

            if shema_attribute and not Piece.schema.get(key).get("mutable"):
                print("Model Error - Attribute of Piece is not mutable: ", key)

class Doc:

    schema = read_schema(SCHEMA_PATH + "doc.json")

    def __init__(self, values: dict):
        for key in Piece.schema:
            setattr(self, key, values.get(key))

    def __eq__(self, other):
        if (isinstance(other, Doc)):
            for key in Doc.schema:
                if not (getattr(self, key) == getattr(other, key)): return False
            return True

##
##  DB Access Layer
## 
import psycopg2

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
            print("DB Success - Connection to DB created")
        except (Exception, psycopg2.Error) as error:
            print("DB Error - Unable to connect: ", error)
            self.connection = None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("DB Success - Connection to DB closed")

    def create_piece(self, piece: Piece):
        current_timestamp = datetime.now(timezone.utc)
        sql = f"""
        INSERT INTO pieces VALUES (
            DEFAULT,
            '{piece.content}',
            '{current_timestamp}',
            '{current_timestamp}'
        );
        """
        if self.connection:
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

    def get_piece(self, id: int) -> Piece:

        sql = f"""
        SELECT *
        FROM pieces
        WHERE id = {str(id)}
        """

        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
                res = cursor.fetchone()
                self.connection.commit()
                print("DB Success - A piece has been retrieved")
                return Piece(pg_row_to_dict(res, Piece.schema))
            except (Exception) as error:
                print("DB Error - A piece insert has failed: ", error)
            finally:
                if cursor:
                    cursor.close()
            
        if not self.connection: return

    def save_piece(self, piece: Piece):

        prev_piece = self.get_piece(piece.id)

        if prev_piece and prev_piece != piece:
            sql = f"""
                UPDATE pieces SET content = '{piece.content}'
                WHERE id = {piece.id}
                """

        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
                self.connection.commit()
                print("DB Success - A piece has been updated")
            except (Exception) as error:
                print("DB Error - A piece update has failed: ", error)
            finally:
                if cursor:
                    cursor.close()

        if prev_piece and prev_piece == piece:
            print("Model Alert: Piece has not changed", piece)

        if not prev_piece:
            self.create_piece(piece)

    def create_doc(self, doc: Doc):
        current_timestamp = datetime.now(timezone.utc)
        sql = f"""
        INSERT INTO docs VALUES (
            DEFAULT,
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

    def get_doc(self, id: int) -> Piece:

        sql = f"""
        SELECT *
        FROM docs
        WHERE id = {str(id)}
        """

        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
                res = cursor.fetchone()
                self.connection.commit()
                print("DB Success - A doc has been retrieved")
                return Doc(pg_row_to_dict(res, Doc.schema))
            except (Exception) as error:
                print("DB Error - A piece insert has failed: ", error)
            finally:
                if cursor:
                    cursor.close()
        if not self.connection: return
