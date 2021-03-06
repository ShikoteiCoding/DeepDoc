from dataclasses import dataclass, field
from typing import Optional
from psycopg2 import sql #type: ignore
from .utils import NotFoundError, NotInsertedError, NoRecordsError
from db import DBLayerAccess

import datetime as dt

#from utils import read_schema, SCHEMA_PATH

@dataclass
class Piece:
    """
    Domain model of a Piece.
    Template instance of a Piece.
    """
    id:             Optional[int]           = field(init=True, default=None)
    title:          str                     = field(init=True, default="")
    content:        str                     = field(init=True, default="")
    create_date:    Optional[dt.datetime]   = field(init=True, default=None)
    modify_date:    Optional[dt.datetime]   = field(init=True, default=None)

@dataclass
class PieceVersion:
    """
    Domain model of a Piece Version.
    Actual instance of a Piece.
    """
    id:             Optional[int]           = field(init=True, default=None)
    piece_id:       Optional[int]           = field(init=True, default=None)
    title:          str                     = field(init=True, default="")
    content:        str                     = field(init=True, default="")
    create_date:    Optional[dt.datetime]   = field(init=True, default=None)
    modify_date:    Optional[dt.datetime]   = field(init=True, default=None)
    

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