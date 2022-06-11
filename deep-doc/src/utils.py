from domain_types.piece import Piece
from domain_types.document import Document

from db.db import DBLayerAccess

import json

from typing import Any, ClassVar

SCHEMA_PATH = "../schema/"

def read_schema(path: str) -> dict:

    with open(path) as f:
        return json.load(f)

class PieceMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer: DBLayerAccess):
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

    def map_row_to_obj(self, row: dict) -> Piece:
        # Might raise little too early, returning None and handling later might be better
        if not row: raise TypeError("A record tuple is expected.")

        new_dict = {}
        # Expected order of schema and rows / column. Might need fix one day
        #for index, key in enumerate(Piece.schema.keys()):
        #    new_dict[key] = row[index]
        # TODO: Create from db properly
        return Piece(**row)


class DocumentMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer):
        self.db_layer = db_layer

    def find(self, id: int) -> Document:
        if not id: raise TypeError("Expect an integer.")

        sql = f"SELECT * FROM documents WHERE id={str(id)} LIMIT 1"
        return self.map_row_to_obj(self.db_layer.execute_fetch_one(sql))

    def findall(self) -> list[Document]:
        # Strong hypothesis : DB is light
        sql = f"SELECT * FROM documents"
        return [self.map_row_to_obj(row) for row in self.db_layer.execute_fetch_all(sql)]

    def insert(self, doc: Document) -> Document:
        if not isinstance(doc, Document): raise TypeError("A doc object is expected.")

        sql = f"INSERT INTO documents (title, content) VALUES ('{doc.title}', '{doc.content}') RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_insert(sql))

    def update(self, doc: Document) -> Document:
        if not isinstance(doc, Document): raise TypeError("A doc object is expected.")
        
        if not doc.id or not doc.content: raise AttributeError("Attribute of doc object does not exist.")
        
        fetched_doc = self.find(doc.id)

        if fetched_doc == doc:
            print("Model Warning - A record is not updated because has no changes")
            return doc
        
        sql = f"UPDATE documents SET content = '{doc.content}', title = '{doc.title}' WHERE id = {doc.id} RETURNING *;"
        return self.map_row_to_obj(self.db_layer.execute_update(sql))

    def map_row_to_obj(self, row: tuple) -> Document:
        if not row: raise TypeError("A record tuple is expected.")

        new_dict = {}
        #for index, key in enumerate(Document.schema.keys()):
        #    new_dict[key] = row[index]
        # TODO: Create from db properly
        return Document(**row)

##
#   Parser Functions
##

import re
class DocumentParser:
    """ Static class to hold parsing functions. """

    @staticmethod
    def read(doc: Document, piece_mapper: PieceMapper) -> str:
        if not isinstance(doc, Document) or not isinstance(piece_mapper, PieceMapper): raise TypeError("Expect a doc object and a piece mapper object.")

        piece_refs = DocumentParser.extract_piece_references(doc)
        doc_associated_pieces = [piece_mapper.find(piece_id) for piece_id in piece_refs]
        pieces = {str(piece.id): str(piece.content) for piece in doc_associated_pieces}
        return DocumentParser.replace_piece_references(doc, piece_refs, pieces)

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