from dataclasses import dataclass
from datetime import datetime

from domain_types.piece import Piece
from domain_types.document import Document

import json
import psycopg2

from psycopg2.extensions import cursor as Cursor
from typing import ClassVar

SCHEMA_PATH = "../schema/"

def read_schema(path: str) -> dict:

    with open(path) as f:
        return json.load(f)

##
## Project config
##
@dataclass(frozen=True)
class Config:
    """ Dataclass to hold the DB configurations. Not mutable. """

    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "postgres"
    db_user: str = "admin"
    db_pwd:  str = "admin"

##
##  Classes for the Datbase Object Model
##
#class OldPiece:
#    """ Domain model of a Piece. """
#
#    schema: ClassVar[dict] = read_schema(SCHEMA_PATH + "piece.json")
#    schema_fields: ClassVar[list] = list(schema.keys())
#
#    def __init__(self, values: dict):
#        for key in OldPiece.schema:
#            setattr(self, key, None)
#        for (attribute, value) in values.items():
#            if not attribute in OldPiece.schema_fields: raise AttributeError("Attribute does not exist in Piece Schema.", attribute)
#            setattr(self, attribute, value)
#
#    def __eq__(self, other: 'OldPiece'):
#        if not (isinstance(other, Piece)): raise TypeError("A piece object is expected.")
#        
#        for key in OldPiece.schema:
#            if (getattr(self, key) != getattr(other, key)): return False
#        return True
#
#    def __str__(self):
#        str_print = ""
#        for key in OldPiece.schema:
#            str_print += (key + ": " + str(getattr(self, key)) + "\n")
#        return str_print
#
#    def __repr__(self) -> str:
#        str_repr = "Piece("
#        for (index, key) in enumerate(OldPiece.schema):
#            str_repr += f"\"{key}\": \"{str(getattr(self, key))}\"" + (", " if index + 1 < len(OldPiece.schema) else "")
#        return str_repr + ")"


class PieceMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer: 'DBLayerAccess'):
        self.db_layer = db_layer

    def find(self, id: int) -> Piece:
        if not id: raise TypeError("Expect an integer.")
        
        sql = f"SELECT * FROM pieces WHERE id={id} LIMIT 1"
        return self.map_row_to_obj(self.db_layer.execute_fetch_one(sql))

    def findall(self) -> list[Piece]:
        sql = f"SELECT * FROM pieces"
        return [self.map_row_to_obj(row) for row in self.db_layer.execute_fetch_all(sql)]

    def insert(self, piece: Piece) -> Piece:
        if not isinstance(piece, Piece): raise TypeError("A piece object is expected.")
        
        sql = f"INSERT INTO pieces (title, content) VALUES ('{piece.title}', '{piece.content}') RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_insert(sql))

    def update(self, piece: Piece) -> Piece:
        if not isinstance(piece, Piece): raise TypeError("A piece object is expected.")

        if not piece.id or not piece.content: raise AttributeError("Attribute of piece object does not exist.")
        
        fetched_piece = self.find(piece.id)

        if fetched_piece == piece:
            print("Model Warning - A record is not updated because has no changes") 
            return piece

        sql = f"UPDATE pieces SET title = '{piece.title}', content = '{piece.content}' WHERE id = {piece.id} RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_update(sql))

    def map_row_to_obj(self, row: tuple) -> Piece:
        # Might raise little too early, returning None and handling later might be better
        if not row: raise TypeError("A record tuple is expected.")

        new_dict = {}
        # Expected order of schema and rows / column. Might need fix one day
        #for index, key in enumerate(Piece.schema.keys()):
        #    new_dict[key] = row[index]
        # TODO: Create from db properly
        return Piece(**new_dict)


#class Doc:
#    """ Domain model of a doc. """
#
#    schema: ClassVar[dict] = read_schema(SCHEMA_PATH + "doc.json")
#    schema_fields: ClassVar[list] = list(schema.keys())
#
#    def __init__(self, values: dict):
#        for key in Doc.schema:
#            setattr(self, key, None)
#        for (attribute, value) in values.items():
#            if not attribute in Doc.schema_fields: raise AttributeError("Attribute does not exist in Doc Schema.", attribute)
#            setattr(self, attribute, value)
#
#    def __eq__(self, other: Doc):
#        if not (isinstance(other, Doc)): raise TypeError("Expect a Doc to compare with.")
#        
#        for key in Doc.schema:
#            if not (getattr(self, key) == getattr(other, key)): return False
#        return True
#
#    def __str__(self):
#        str_print = ''
#        for key in Doc.schema:
#            str_print += (key + ': ' + str(getattr(self, key)) + '\n')
#        return str_print
#
#    def __repr__(self) -> str:
#        str_repr = 'Doc('
#        for (index, key) in enumerate(Doc.schema):
#            str_repr += f"\"{key}\": \"{str(getattr(self, key))}\"" + (", " if index + 1 < len(Doc.schema) else "")
#        return str_repr + ')'


class DocMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer):
        self.db_layer = db_layer

    def find(self, id: int) -> Document:
        if not id: raise TypeError("Expect an integer.")

        sql = f"SELECT * FROM docs WHERE id={str(id)} LIMIT 1"
        return self.map_row_to_obj(self.db_layer.execute_fetch_one(sql))

    def findall(self) -> list[Document]:
        # Strong hypothesis : DB is light
        sql = f"SELECT * FROM docs"
        return [self.map_row_to_obj(row) for row in self.db_layer.execute_fetch_all(sql)]

    def insert(self, doc: Document) -> Document:
        if not isinstance(doc, Document): raise TypeError("A doc object is expected.")

        sql = f"INSERT INTO docs (title, content) VALUES ('{doc.title}', '{doc.content}') RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_insert(sql))

    def update(self, doc: Document) -> Document:
        if not isinstance(doc, Document): raise TypeError("A doc object is expected.")
        
        if not doc.id or not doc.content: raise AttributeError("Attribute of doc object does not exist.")
        
        fetched_doc = self.find(doc.id)

        if fetched_doc == doc:
            print("Model Warning - A record is not updated because has no changes")
            return doc
        
        sql = f"UPDATE docs SET content = '{doc.content}', title = '{doc.title}' WHERE id = {doc.id} RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_update(sql))

    def map_row_to_obj(self, row: tuple) -> Document:
        if not row: raise TypeError("A record tuple is expected.")

        new_dict = {}
        #for index, key in enumerate(Document.schema.keys()):
        #    new_dict[key] = row[index]
        # TODO: Create from db properly
        return Document(**new_dict)

##
#   Parser Functions
##

import re
class DocParser:
    """ Static class to hold parsing functions. """

    @staticmethod
    def read(doc: Document, piece_mapper: PieceMapper) -> str:
        if not isinstance(doc, Document) or not isinstance(piece_mapper, PieceMapper): raise TypeError("Expect a doc object and a piece mapper object.")

        piece_refs = DocParser.extract_piece_references(doc)
        doc_associated_pieces = [piece_mapper.find(piece_id) for piece_id in piece_refs]
        pieces = {str(piece.id): str(piece.content) for piece in doc_associated_pieces}
        return DocParser.replace_piece_references(doc, piece_refs, pieces)

    @staticmethod
    def extract_piece_references(doc: Document) -> list[str]:
        # Might not need to be called "on read" but "on save"
        # Because we can use a different relation table to track saved pieces associated to doc
        # Upsert to avoid adding already existing relations ?
        content = doc.content
        pattern = re.compile('@(.*?)@')
        matches = pattern.findall(content)
        return matches

    @staticmethod
    def replace_piece_references(doc: Document, piece_refs: list[str], pieces: dict[str, str]) -> str:
        content = doc.content
        for piece_ref in piece_refs:
            content = content.replace(f"@{str(piece_ref)}@", pieces.get(piece_ref))
        return content

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

    def fetch_one(self, cursor: Cursor, sql: str) -> tuple:
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
