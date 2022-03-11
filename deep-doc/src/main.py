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
    # Create
    piece = Piece({"content": "Created piece"})
    db_layer.save_piece(piece)
    doc = Doc({"content": "Created doc"})
    db_layer.save_doc(doc)

    fetch_piece = db_layer.get_piece(1)
    fetch_piece.update({"content": "Edited content"})
    db_layer.save_piece(fetch_piece)

    fetch_doc = db_layer.get_doc(1)
    fetch_doc.update({"content": "Edited content"})
    db_layer.save_doc(fetch_doc)

    db_layer.close()