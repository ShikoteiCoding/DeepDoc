from utils import (
    Config, DBLayerAccess, 
    DocumentParser, 
    PieceMapper, DocumentMapper
)

from domain_types import Piece, Document

if __name__ == '__main__':
    
    c = Config()
    db_layer = DBLayerAccess(c)
    db_layer.connect()
    piece_mapper = PieceMapper(db_layer)
    doc_mapper = DocumentMapper(db_layer)
    

    db_layer.close()