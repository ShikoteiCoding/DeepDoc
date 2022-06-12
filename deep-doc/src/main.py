from utils import (
    DBLayerAccess, 
    PieceMapper, DocumentMapper
)

from domain_types import Piece, Document

from config import Config

def usecase_create_and_push(db_layer: DBLayerAccess):
    piece = Piece()

    piece_mapper = PieceMapper(db_layer)
    piece = Piece(**{"title": "Title", "content": "Content"})
    inserted_piece = piece_mapper.insert(piece)

    print(piece == inserted_piece)

def usecase_create_nested_document(db_layer: DBLayerAccess):
    PieceMapper(db_layer)
    DocumentMapper(db_layer)
    

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()

    usecase_create_and_push(db_layer)

    db_layer.close()