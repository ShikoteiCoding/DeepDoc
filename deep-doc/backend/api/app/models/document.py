from dataclasses import dataclass, field
from typing import Optional
import datetime as dt

from db import DBLayerAccess
from psycopg2 import sql #type: ignore

from .utils import NotFoundError, NotInsertedError, NoRecordsError

@dataclass
class Document:
    """
    Domain model of a Document.
    Template instance of a Document.
    """
    id:             Optional[int]           = field(init=True, default=None)
    title:          str                     = field(init=True, default="")
    content:        str                     = field(init=True, default="")
    create_date:    Optional[dt.datetime]   = field(init=True, default=None)
    modify_date:    Optional[dt.datetime]   = field(init=True, default=None)

@dataclass
class DocumentVersion:
    """
    Domain model of a Document Version.
    Actual instance of a Document.
    """
    id:             Optional[int]           = field(init=True, default=None)
    document_id:    Optional[int]           = field(init=True, default=None)
    title:          str                     = field(init=True, default="")
    content:        str                     = field(init=True, default="")
    create_date:    Optional[dt.datetime]   = field(init=True, default=None)
    modify_date:    Optional[dt.datetime]   = field(init=True, default=None)

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

        if not res or len(res) == 0: raise NoRecordsError()

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

        if not res: raise NotInsertedError()

        return Document(**res[0])