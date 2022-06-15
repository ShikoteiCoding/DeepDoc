from db import DBLayerAccess
from utils import PieceMapper
from domain_types import Piece
from config import Config

from psycopg2 import sql


if __name__ == "__main__":

    config = Config()

    db_layer = DBLayerAccess(config)
    db_layer.connect()

    piece_mapper = PieceMapper(db_layer)

    piece = Piece(title="title", content="content")

    table = 'pieces'
    mutable_columns = ['title', 'content']
    pkey = 'id'

    query = sql.SQL(
            "UPDATE {table} SET {values} WHERE {pkey} = {id} RETURNING *;"
        ).format(
            table = sql.Identifier(table),
            values = sql.SQL(',').join(
                [
                    sql.Composed(
                        [
                            sql.Identifier(col),
                            sql.SQL(" = "),
                            sql.Placeholder(col)
                        ]
                    )
                    for col in mutable_columns
                ]
            ),
            pkey = sql.Identifier(pkey),
            id = sql.Placeholder('value')
        )

        #sql = f"UPDATE pieces SET title = '{piece.title}', content = '{piece.content}' WHERE id = {piece.id} RETURNING *;"
        

    #res = db_layer.select(query)

    print(query.as_string(db_layer.connection))

    with db_layer.connection.cursor() as cur:
        res =  db_layer.execute(query, {**{str(col): str(getattr(piece, col)) for col in mutable_columns}, **{'value': value}})
        #res = cur.fetchall()
        #db_layer.connection.commit()

    #fetch_piece = piece_mapper.find(172)

    print(res)
    db_layer.close()
