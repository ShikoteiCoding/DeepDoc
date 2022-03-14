import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)

    db_layer.connect()
    
    doc = Doc({"content": "First deep doc with this amazing piece: \@1"})

    db_layer.save_doc(doc)

    db_layer.close()