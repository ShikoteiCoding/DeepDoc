from sqlite3 import Cursor
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
        if id:
            sql = f"SELECT * FROM pieces WHERE id={id} LIMIT 1"
            return self.map_row_to_obj(self.db_layer.execute_fetch_one(sql))

    def insert(self, piece: Piece) -> Piece:
        if piece:
            sql = f"INSERT INTO pieces (content) VALUES ('{piece.content}') RETURNING *;"
            return self.map_row_to_obj(self.db_layer.execute_insert(sql))

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

    def map_row_to_obj(self, row: tuple) -> Piece:
        if row:
            new_dict = {}
            # Expected order of schema and rows / column. Might need fix one day
            for index, key in enumerate(Piece.schema.keys()):
                new_dict[key] = row[index]
            return Piece(new_dict)


class Doc:

    schema = read_schema(SCHEMA_PATH + "doc.json")

    def __init__(self, values: dict):
        for key in Piece.schema:
            setattr(self, key, values.get(key))

    def __eq__(self, other: Doc):
        if (isinstance(other, Doc)):
            for key in Doc.schema:
                if not (getattr(self, key) == getattr(other, key)): return False
            return True

    def __str__(self):
        str_print = ''
        for key in Doc.schema:
            str_print += (key + ': ' + str(getattr(self, key)) + '\n')
        return str_print


class DocMapper:

    def __init__(self, db_layer: DBLayerAccess):
        self.db_layer = db_layer

    def find(self, id: int) -> Doc:
        if id:
            sql = f"SELECT * FROM docs WHERE id={id} LIMIT 1"
            return self.map_row_to_obj(self.db_layer.execute_fetch_one(sql))

    def insert(self, doc: Doc) -> Doc:
        if doc:
            sql = f"INSERT INTO docs (content) VALUES ('{doc.content}') RETURNING *;"
            return self.map_row_to_obj(self.db_layer.execute_insert(sql))

    def update(self, doc: Doc) -> Doc:
        if doc:
            if doc.id and doc.content:
                fetched_doc = self.find(doc.id)
                if fetched_doc == doc:
                    print("Model Warning - A record is not updated because has no changes")
                elif fetched_doc != doc:
                    sql = f"UPDATE docs SET content = '{doc.content}' WHERE id = {doc.id} RETURNING *;"
                    return self.map_row_to_obj(self.db_layer.execute_update(sql))
            elif not doc.content:
                print("Model Error - A new record is empty")
            elif not doc.id:
                print("Model Error - A new record can't be updated")

    def map_row_to_obj(self, row: tuple) :
        if row:
            new_dict = {}
            for index, key in enumerate(Piece.schema.keys()):
                new_dict[key] = row[index]
            return Piece(new_dict)

import re
class DocParser:

    def read(doc: Doc) -> str:
        full_doc = ""
        return full_doc

    def extract_piece_references(doc: Doc) -> list[str]:
        content = doc.content
        pattern = re.compile('\@(.*)@')
        matches = pattern.findall(content)
        return matches

    def replace_piece_references(doc: Doc):
        piece_refs = DocParser.extract_piece_references(doc)
        for piece_ref in piece_refs:
            print(piece_ref)
            # how to access pieces properly ?

    
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

    def fetch_one(self, cursor: Cursor, sql: str) -> tuple:
        cursor.execute(sql)
        res = cursor.fetchone()
        self.connection.commit()
        return res

    def execute_fetch_one(self, sql: str) -> tuple:
        if sql:
            if self.connection:
                cursor = self.connection.cursor()
                try:
                    print("DB Success - A record has been fetched")
                    return self.fetch_one(cursor, sql)
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
                    print("DB Success - A record has been inserted")
                    return self.fetch_one(cursor, sql)
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
                    print("DB Success - A record has been updated")
                    return self.fetch_one(cursor, sql)
                except (Exception) as error:
                    print("DB Error - A record update has failed: ", error)
                finally:
                    if cursor:
                        cursor.close