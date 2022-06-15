from domain_types import Piece, Document
from db import DBLayerAccess

from psycopg2 import sql #type: ignore
import json

SCHEMA_PATH = "../schema/"

def read_schema(path: str) -> dict:

    with open(path) as f:
        return json.load(f)

class NotFoundError(Exception):
    pass
class NoRecordsError(Exception):
    pass
class NotInsertedError(Exception):
    pass

class PieceMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer: DBLayerAccess):
        self.db_layer = db_layer

        # SQL
        self.table = "pieces"
        self.pkey = "id"
        self.mutable_columns = ['title', 'content']

    def find(self, id: int | None) -> Piece:
        """ Return a specific item by primary key search. """

        if not id: raise TypeError("Expect an integer.")
        
        query = sql.SQL(
            "SELECT * FROM {table} WHERE {pkey} = %s"
        ).format(
            table = sql.Identifier(self.table),
            pkey = sql.Identifier(self.pkey)
        )

        res = self.db_layer.execute(query, (str(id),))

        if not res: raise NotFoundError()

        return Piece(**res[0])

    def find_all(self) -> list[Piece]:
        """ Return all items. """

        query = sql.SQL(
            "SELECT * FROM {table}"
        ).format(
            table = sql.Identifier(self.table)
        )

        res = self.db_layer.execute(query)

        if not res or len(res) == 0: raise NoRecordsError()

        return [Piece(**row) for row in res]

    def insert(self, piece: Piece | None) -> Piece:
        """ Insert one item. """

        if not isinstance(piece, Piece): raise TypeError("A piece object is expected.")

        query = sql.SQL(
            "INSERT INTO {table} ({mutable_columns}) VALUES ({place_holder}) RETURNING *;"
        ).format(
            table = sql.Identifier(self.table),
            mutable_columns = sql.SQL(', ').join(map(sql.Identifier, self.mutable_columns)),
            place_holder = sql.SQL(',').join(
                [sql.Placeholder(c) for c in self.mutable_columns]
            )
        )
        
        res = self.db_layer.execute(query, {str(col): str(getattr(piece, col)) for col in self.mutable_columns})

        if not res: raise NotInsertedError()

        return Piece(**res[0])

    def update(self, piece: Piece | None) -> Piece:
        """ Update an existing item. """

        if not isinstance(piece, Piece): raise TypeError("A piece object is expected.")

        if not piece.id or not piece.content: raise AttributeError("Attribute of piece object does not exist.")
        
        fetched_piece = self.find(piece.id)

        if fetched_piece == piece:
            print("Model Warning - A record is not updated because has no changes") 
            return piece

        query = sql.SQL(
            "UPDATE {table} SET {values} WHERE {pkey} = {id} RETURNING *;"
        ).format(
            table = sql.Identifier(self.table),
            values = sql.SQL(',').join(
                [
                    sql.Composed(
                        [
                            sql.Identifier(col),
                            sql.SQL(" = "),
                            sql.Placeholder(col)
                        ]
                    )
                    for col in self.mutable_columns
                ]
            ),
            pkey = sql.Identifier(self.pkey),
            id = sql.Placeholder(self.pkey)
        )

        res =  self.db_layer.execute(query, {**{str(col): str(getattr(piece, col)) for col in self.mutable_columns}, **{self.pkey: str(piece.id)}})

        if not res: raise NotInsertedError()

        return Piece(**res[0])


class DocumentMapper:
    """ Dataclass to map SQL Logic to Domain Logic for a Piece. """

    def __init__(self, db_layer: DBLayerAccess):
        self.db_layer = db_layer

        # SQL
        self.table = "documents"
        self.pkey = "id"
        self.mutable_columns = ['title', 'content']

    def find(self, id: int | None) -> Document:
        """ Return a specific item by primary key search. """

        if not id: raise TypeError("Expect an integer.")
        
        query = sql.SQL(
            "SELECT * FROM {table} WHERE {pkey} = %s"
        ).format(
            table = sql.Identifier(self.table),
            pkey = sql.Identifier(self.pkey)
        )

        res = self.db_layer.execute(query, (str(id),))

        if not res: raise NotFoundError()

        return Document(**res[0])

    def find_all(self) -> list[Document]:
        """ Return all items. """

        query = sql.SQL(
            "SELECT * FROM {table}"
        ).format(
            table = sql.Identifier(self.table)
        )

        res = self.db_layer.execute(query)

        if not res or len(res) == 0: raise NotFoundError()

        return [Document(**row) for row in res]

    def insert(self, document: Document | None) -> Document:
        """ Insert one item. """
        
        if not isinstance(document, Document): raise TypeError("A doc object is expected.")

        query = sql.SQL(
            "INSERT INTO {table} ({mutable_columns}) VALUES ({place_holder}) RETURNING *;"
        ).format(
            table = sql.Identifier(self.table),
            mutable_columns = sql.SQL(', ').join(map(sql.Identifier, self.mutable_columns)),
            place_holder = sql.SQL(',').join(
                [sql.Placeholder(c) for c in self.mutable_columns]
            )
        )
        
        res = self.db_layer.execute(query, {str(col): str(getattr(document, col)) for col in self.mutable_columns})


        if not res: raise NotFoundError()

        return Document(**res[0])

    def update(self, document: Document | None) -> Document:
        """ Update an existing item. """
        if not isinstance(document, Document): raise TypeError("A doc object is expected.")
        
        if not document.id or not document.content: raise AttributeError("Attribute of doc object does not exist.")
        
        fetched_doc = self.find(document.id)

        if fetched_doc == document:
            print("Model Warning - A record is not updated because has no changes")
            return document
        
        query = sql.SQL(
            "UPDATE {table} SET {values} WHERE {pkey} = {id} RETURNING *;"
        ).format(
            table = sql.Identifier(self.table),
            values = sql.SQL(',').join(
                [
                    sql.Composed(
                        [
                            sql.Identifier(col),
                            sql.SQL(" = "),
                            sql.Placeholder(col)
                        ]
                    )
                    for col in self.mutable_columns
                ]
            ),
            pkey = sql.Identifier(self.pkey),
            id = sql.Placeholder(self.pkey)
        )

        res =  self.db_layer.execute(query, {**{str(col): str(getattr(document, col)) for col in self.mutable_columns}, **{self.pkey: str(document.id)}})

        if not res: raise NotFoundError()

        return Document(**res[0])

##
#   Parser Functions
##

import re
class DocumentParser:
    """ Static class to hold parsing functions. """

    @staticmethod
    def read(doc: Document, piece_mapper: PieceMapper) -> str:
        if not isinstance(doc, Document) or not isinstance(piece_mapper, PieceMapper): 
            raise TypeError("Expect a doc object and a piece mapper object.")

        piece_refs = DocumentParser.extract_piece_ids(doc)

        # Regex match ids. Extract is type-safe. Cast the id to integer.
        doc_associated_pieces = [piece_mapper.find(int(piece_id)) for piece_id in piece_refs]
        pieces_dict = {str(piece.id): str(piece.content) for piece in doc_associated_pieces}
        return DocumentParser.replace_piece_ids(doc, pieces_dict)

    @staticmethod
    def extract_piece_ids(doc: Document) -> list[str]:
        # Might not need to be called "on read" but "on save"
        # Because we can use a different relation table to track saved pieces associated to doc
        # Upsert to avoid adding already existing relations ?
        content = doc.content
        pattern = re.compile('@(.*?)@')
        matches = pattern.findall(content)
        return matches

    @staticmethod
    def replace_piece_ids(doc: Document, pieces_dict: dict[str, str]) -> str:
        content = doc.content
        for key, value in pieces_dict.items():
            content = content.replace(f"@{str(key)}@", value)
        return content