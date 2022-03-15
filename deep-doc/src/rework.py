import psycopg2
from utils import Config, DBLayerAccess, Piece, Doc, PieceMapper, DocMapper

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    
    piece_mapper = PieceMapper(db_layer)

    piece = Piece({"content": "new pattern piece test"})

    inserted_piece = piece_mapper.insert(piece)

    print(inserted_piece)
    
    piece_updated = Piece({
        "id": inserted_piece.id, 
        "content": "update this piece",
        "create_date": inserted_piece.create_date,
        "modify_date": inserted_piece.modify_date
    })
    
    print(piece_updated)

    #piece_updated = Piece({"id": piece.id, "content": "update this piece"})

    piece_updated_saved = piece_mapper.update(piece_updated)

    print(piece_updated_saved)

    db_layer.close()