import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc, PieceMapper, DocMapper

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    
    piece_mapper = PieceMapper(db_layer)

    piece = Piece({"content": "new pattern piece test"})

    inserted_piece = piece_mapper.insert(piece)
    
    piece_updated = Piece({"id": piece.id, "content": "update this piece"})

    #piece_mapper.update(piece_updated)

    db_layer.close()