import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc

##
##  Database Interaction
##
def connect_db(c):
    try:
        connection = psycopg2.connect(
            user        = c.db_user,
            password    = c.db_pwd,
            host        = c.db_host,
            port        = c.db_port,
            database    = c.db_name
        )

        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to DB: ", error)

def cursor_db(connection):
    return connection.cursor()

def close_connection_db(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("DB Connection has been closed")


if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)

    db_layer.connect()

    piece = Piece({ "content": "Created today"})
    doc = Doc({"content": "First Document"})

    #db_layer.create_piece(piece)
    #db_layer.create_doc(doc)

    pieceFetch = db_layer.get_piece(1)

    print("Original Piece from DB: ", pieceFetch)
    pieceFetch.update({"content": "Update this piece of shit"})
    db_layer.save_piece(pieceFetch)
    print("Updated Piece, not saved yet: ", pieceFetch)
    pieceFetch2 = db_layer.get_piece(1)
    print("Original Piece after update: ", pieceFetch2)

    db_layer.close()