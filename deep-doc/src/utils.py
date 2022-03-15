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
## Declare classes
##
class Piece:
    pass
class Doc:
    pass
class PieceMapper:
    pass
class DocMapper:
    pass
class DBLayerAccess:
    pass
class Config:
    pass

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

    def __eq__(self, other: Piece):
        if (isinstance(other, Piece)):
            for key in Piece.schema:
                if not (getattr(self, key) == getattr(other, key)): return False
            return True

    def __str__(self):
        str_print = ''
        for key in Piece.schema:
            str_print += (key + ': ' + str(getattr(self, key)) + '\n')
        return str_print

class PieceMapper:

    def __init__(self, db_layer: DBLayerAccess):
        self.db_layer = db_layer

    def find(self, id: int) -> Piece:
        sql = f"SELECT * FROM pieces WHERE id={id} LIMIT 1"
        piece = self.db_layer.execute_fetch_one(sql)
        return self.map_row_to_obj(piece)

    def insert(self, piece: Piece) -> Piece:
        if piece:
            sql = f"INSERT INTO pieces (content) VALUES ('{piece.content}') RETURNING *;"
            piece = self.db_layer.execute_insert(sql)
            return self.map_row_to_obj(piece)

    def update(self, piece: Piece) -> Piece:
        if piece:
            if piece.id and piece.content:
                fetched_piece = self.find(piece.id)
                if fetched_piece == piece:
                    print("Model Warning - A record is not updated because has no changes")
                elif fetched_piece != piece:
                    sql = f"UPDATE pieces SET content = '{piece.content}' WHERE id = {piece.id} RETURNING *;"
                    return self.map_row_to_obj(self.db_layer.execute_update(sql))
            elif not piece.content:
                print("Model Error - A new record is empty")
            elif not piece.id:
                print("Model Error - A new record can't be updated")
        #for (key, value) in values.items():
        #    shema_attribute = Piece.schema.get(key)
        #    if not shema_attribute: print("Model Error - Attribute of Piece not existing in schema: ", key)
        #    elif shema_attribute and Piece.schema.get(key).get("mutable"):
        #        setattr(self, key, value)
        #        print("Model Success - Attribute of Piece has been updated: ", key)
        #    elif shema_attribute and not Piece.schema.get(key).get("mutable"):
        #        print("Model Error - Attribute of Piece is not mutable: ", key)

    def map_row_to_obj(self, row: tuple):
        new_dict = {}
        for index, key in enumerate(Piece.schema.keys()):
            new_dict[key] = row[index]
        return Piece(new_dict)


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

    def __str__(self):
        str_print = ''
        for key in Doc.schema:
            str_print += (key + ': ' + str(getattr(self, key)) + '\n')
        return str_print

    def insert(self, db_layer):
        sql = f"INSERT INTO pieces (content) VALUES ('{self.content}');"
        db_layer.insert(sql)

    def update(self, values):
        for (key, value) in values.items():
            shema_attribute = Doc.schema.get(key)
            if not shema_attribute: print("Model Error - Attribute of Doc not existing in schema: ", key)
            elif shema_attribute and Piece.schema.get(key).get("mutable"):
                setattr(self, key, value)
                print("Model Success - Attribute of Doc has been updated: ", key)
            elif shema_attribute and not Piece.schema.get(key).get("mutable"):
                print("Model Error - Attribute of Doc is not mutable: ", key)

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

    def execute_fetch_one(self, sql: str) -> tuple:
        if sql:
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    self.connection.commit()
                    print("DB Success - A record has been fetched")
                    return res
                except (Exception) as error:
                    print("DB Error - A record fetch has failed: ", error)
                finally:
                    if cursor:
                        cursor.close()
    
    def execute_insert(self, sql: str) -> tuple:
        if sql:
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    self.connection.commit()
                    print("DB Success - A record has been inserted")
                    return res
                except (Exception) as error:
                    print("DB Error - A record insert has failed: ", error)
                finally:
                    if cursor:
                        cursor.close()
    
    def execute_update(self, sql:str) -> tuple:
        if sql:
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    self.connection.commit()
                    print("DB Success - A record has been updated")
                    return res
                except (Exception) as error:
                    print("DB Error - A record update has failed: ", error)
                finally:
                    if cursor:
                        cursor.close

    def insert(self, sql: str):
        if sql:
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(sql)
                    self.connection.commit()
                    print("DB Success - Record inserted")
                except (Exception) as error:
                    print("DB Error - A record insert has failed: ", error)
                finally:
                    if cursor:
                        cursor.close()

    def create_piece(self, piece: Piece):

        if piece:
            sql = f"INSERT INTO pieces (content) VALUES ('{piece.content}');"
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
        
        if not piece: print("Model Error - Piece is empty", piece)

    def create_doc(self, doc: Doc):

        if doc:
            sql = f"INSERT INTO docs (content) VALUES ('{doc.content}');"
            if self.connection:
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
        
        if not doc: print("Model Error - Doc is empty", doc)

    def get_piece(self, id: int) -> Piece:

        if id:
            sql = f"SELECT * FROM pieces WHERE id = {str(id)}"

            if self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    self.connection.commit()
                    print("DB Success - A piece has been retrieved")
                    return Piece(pg_row_to_dict(res, Piece.schema))
                except (Exception) as error:
                    print("DB Error - A piece fetch has failed: ", error)
                finally:
                    if cursor:
                        cursor.close()
            
            if not self.connection: return
        
        return

    def get_doc(self, id: int) -> Piece:

        if id:
            sql = f"SELECT * FROM docs WHERE id = {str(id)}"

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

        return

    def save_piece(self, piece: Piece):
        
        if piece:
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
                print("Model Warning: A non existing piece is saved, creating a new entry")
                self.create_piece(piece)

    def save_doc(self, doc: Doc):

        if doc: 
            prev_doc = self.get_doc(doc.id)

            if prev_doc and prev_doc != doc:
                sql = f"""
                    UPDATE docs SET content = '{doc.content}'
                    WHERE id = {doc.id}
                    """

                if self.connection:
                    cursor = self.connection.cursor()
                    try:
                        cursor.execute(sql)
                        self.connection.commit()
                        print("DB Success - A doc has been updated")
                    except (Exception) as error:
                        print("DB Error - A doc update has failed: ", error)
                    finally:
                        if cursor:
                            cursor.close()

            if prev_doc and prev_doc == doc:
                print("Model Alert: Piece has not changed", doc)

            if not prev_doc:
                print("Model Warning: A non existing doc is saved, creating a new entry")
                self.create_doc(doc)